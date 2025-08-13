from services.auth import AuthService
import streamlit as st

AuthService.protect_page()

st.title("🚪 Logout")
st.write("Are you sure you want to log out?")

col1, col2 = st.columns(2)
with col1:
    if st.button("Yes, log me out", type="primary"):
        AuthService.logout()
with col2:
    if st.button("Cancel"):
        st.switch_page(st.Page('app/pages/chat/chat.py'))
