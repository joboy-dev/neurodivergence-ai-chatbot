import time
from typing import Any, Optional
from sqlalchemy.orm import Session
import streamlit as st

from db.models.user import User
from services.auth import AuthService
from utils.firebase import FirebaseService
from utils.messages import generate_message


class UserService:
    
    @classmethod
    def change_password(cls, db: Session, email: str, old: str, new: str, confirm: str):
        user = User.fetch_one_by_field(db, error_message="Invalid credentials", email=email)
        # user = db.query(User).filter(User.email == email).first()  
        
        if not AuthService.verify_password(old, user.password):
            st.error(generate_message("Invalid credentials", "error"))
            return

        if old == new:
            st.error(generate_message("New password cannot be the same as the old one", "error"))
            return
        
        if new != confirm:
            st.error(generate_message("New passwords do not match", "error"))
            return

        user.password = AuthService.hash_password(new)
        db.commit()
        db.refresh(user)
        
        st.success(generate_message("Password updated successfully", "success"))
        time.sleep(0.5)
        st.rerun()
    
    
    @classmethod
    def update_profile(
        cls, 
        db: Session, 
        name: Optional[str], 
        email: Optional[str], 
        profile_picture_file: Optional[Any]
    ):
        user = User.fetch_one_by_field(
            db, error_message="User not found", 
            email=st.session_state.current_user.email
        )
        # user = db.query(User).filter(User.email == st.session_state.current_user.email).first()
        
        if not user:
            st.error(generate_message("User not found", "error"))
            return
        
        if name:
            user.name = name
            user.profile_picture = f"https://ui-avatars.com/api/?name={user.name}"
        
        if email:
            existing_user = User.fetch_one_by_field(db, throw_error=False, email=email)
            # existing_user = db.query(User).filter(User.email == email).first()
            
            if existing_user and existing_user.id != user.id:
                st.error(generate_message("Email already exists", "error"))
                return
            
            user.email = email
        
        if profile_picture_file:
            user.profile_picture = FirebaseService.upload_file(
                file=profile_picture_file,
                upload_folder='users',
                model_id=user.id
            )
        
        db.commit()
        db.refresh(user)
        
        # Update session state with the updated user
        st.session_state['current_user'] = user
        
        st.success(generate_message("Profile updated successfully", "success"))
        time.sleep(0.5)
        st.rerun()


user_service = UserService()
