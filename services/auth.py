import re
import time
from typing import Optional
import streamlit as st
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db.models.user import User
from utils.messages import generate_message


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    
    @classmethod
    def is_authenticated(cls):
        return st.session_state.get("current_user", None)
    
    @classmethod
    def protect_page(cls):
        if not cls.is_authenticated():
            st.error(generate_message("You need to be logged in to access this page.", "error"))
            time.sleep(1)
            st.switch_page(st.Page('app/pages/auth/login.py'))
    
    @classmethod
    def hash_password(cls, password: str):
        return pwd_context.hash(password)
    
    @classmethod
    def verify_password(cls, password: str, hash: str):
        return pwd_context.verify(password, hash)
    
    @classmethod
    def is_valid_email(cls, email):
        """Validate email using regex."""
        
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email)

    @classmethod
    def authenticate(cls, db: Session, email: str, password: str):
        st.session_state['current_user'] = None
        
        if not cls.is_valid_email(email):
            st.error(generate_message("Invalid email format!", "error"))
            return
        
        # user = User.fetch_one_by_field(db, email=email)
        user = User.fetch_one_by_field(
            db=db, error_message="Invalid credentials", 
            email=email,
        )
        
        if not user:
            return
        
        if not cls.verify_password(password, user.password):
            print('Password validation failed')
            st.error(generate_message("Invalid credentials", "error"))
            return
        
        st.session_state['current_user'] = user
        time.sleep(0.5)
        st.switch_page(st.Page('app/pages/chat/chat.py'))
    
    @classmethod
    def register(
        cls, 
        db: Session, 
        name: Optional[str], 
        email: str, 
        password: str, 
        confirm_password: str
    ):
        st.session_state['current_user'] = None
        
        if not email or not password:
            st.error(generate_message("Both email and password are required!", "error"))
            return

        if not cls.is_valid_email(email):
            st.error(generate_message("Invalid email format!", "error"))
            return
        
        if password != confirm_password:
            st.error(generate_message("Passwords do not match!", "error"))
            return
        
        if User.fetch_one_by_field(db, throw_error=False, email=email):
            st.error(generate_message("User with email already exists!", 'error'))
            return
        
        hashed_password = cls.hash_password(password)
        
        user = User.create(
            db=db, 
            name=name, 
            email=email, 
            password=hashed_password
        )
        
        st.session_state['current_user'] = user
        st.success(generate_message(f"Successfully registered with {email}!"))
        time.sleep(0.5)
        st.switch_page(st.Page('app/pages/chat/chat.py'))
    
    @classmethod
    def logout(cls):
        st.session_state.pop('current_user', None)
        st.success(generate_message("Logged out successfully!"))
        
        time.sleep(0.5)
        st.rerun()