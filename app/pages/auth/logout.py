import streamlit as st
from services.auth import AuthService

AuthService.protect_page()

st.markdown("## Sign out")
st.caption("Are you sure you want to sign out?")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Yes, sign me out", type="primary"):
        AuthService.logout()
    if st.button("Cancel"):
        st.switch_page(st.Page("app/pages/chat/chat.py"))
