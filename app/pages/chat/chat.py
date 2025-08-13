import streamlit as st
from db.database import load_db
from services.user import UserService
from utils.messages import generate_message
from services.auth import AuthService


AuthService.protect_page()

db = load_db()
current_user = st.session_state.current_user
selected_chat = st.session_state.get("selected_chat", None)

st.title('👤 Chat')

tab1, tab2 = st.tabs(['Chat', 'Chat History'])

with tab1:
    pass    

with tab2:
    # Select a chat from history and load the chat
    
    pass