import streamlit as st
from db.database import load_db
from services.user import UserService
from utils.messages import generate_message
from services.auth import AuthService


db = load_db()

# st.title('👤 Chat')

tab1, tab2 = st.tabs(['Login', 'Register'])

with tab1:
    st.title('🔑 Login')

    # Registration form
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your@email.com").strip()
        password = st.text_input("Password", type="password", placeholder="Enter a secure password").strip()
        
        submit = st.form_submit_button("Login", type='primary')

    # Handle form submission
    if submit:
        AuthService.authenticate(db, email, password)


with tab2:
    st.title("🔐 Register")

    # Registration form
    with st.form("register_form"):
        name = st.text_input("Full Name (Optional)", placeholder="John Doe").strip()
        email = st.text_input("Email", placeholder="your@email.com").strip()
        password = st.text_input("Password", type="password", placeholder="Enter a secure password").strip()
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Enter a secure password").strip()

        submit = st.form_submit_button("Register", type='primary')

    # Handle form submission
    if submit:
        AuthService.register(db, name, email, password, confirm_password)