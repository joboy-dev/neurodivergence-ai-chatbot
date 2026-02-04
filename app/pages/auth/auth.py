import streamlit as st
from db.database import load_db
from services.auth import AuthService


db = load_db()

st.markdown("## Welcome")
st.caption("Sign in or create an account to use the neurodiversity support chatbot.")

tab1, tab2 = st.tabs(["Sign in", "Create account"])

with tab1:
    st.markdown("**Sign in**")
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com").strip()
        password = st.text_input(
            "Password", type="password", placeholder="••••••••••"
        ).strip()
        submit = st.form_submit_button("Sign in", type="primary")
    if submit:
        AuthService.authenticate(db, email, password)

with tab2:
    st.markdown("**Create account**")
    with st.form("register_form"):
        name = st.text_input("Full name (optional)", placeholder="Your name").strip()
        email = st.text_input("Email", placeholder="you@example.com").strip()
        password = st.text_input(
            "Password", type="password", placeholder="Choose a password"
        ).strip()
        confirm_password = st.text_input(
            "Confirm password", type="password", placeholder="Confirm password"
        ).strip()
        submit = st.form_submit_button("Create account", type="primary")
    if submit:
        AuthService.register(db, name, email, password, confirm_password)
