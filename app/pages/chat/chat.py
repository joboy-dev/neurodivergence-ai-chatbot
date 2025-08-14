from datetime import datetime, timezone
import streamlit as st

from db.database import load_db
from services.auth import AuthService
from services.chat import ChatService
from db.models.chat import Chat, Message


AuthService.protect_page()

db = load_db()
current_user = st.session_state.current_user
selected_chat = st.session_state.get("selected_chat", None)

st.title('👤 Chat')

tab1, tab2 = st.tabs(['Chat', 'Chat History'])

with tab1:
    if selected_chat is None:
        st.write("Start a new chat")
        chat_name = st.text_input("Enter chat name. (Optional)", key="new_chat_message")
        new_message = st.text_input("Type your message...", key="new_chat_message")
        if st.button("Send", key="start_chat_btn") and new_message.strip():
            # Create a new chat and add the first user message
            chat_obj = Chat.create(
                db=db,
                name=chat_name if chat_name.strip() else "Untitled",
                last_message=new_message,
                last_active_at=datetime.now(timezone.utc),
                user_id=current_user.id
            )
            ChatService.create_chat_message(
                db=db, chat_id=chat_obj.id,
                user_id=current_user.id,
                user_message=new_message
            )
            st.session_state.selected_chat = chat_obj
            st.rerun()
    else:
        # Display chat messages
        _, messages, _ = Message.fetch_by_field(
            db=db,paginate=False,
            chat_id=selected_chat.id
        )
        
        for msg in messages:
            # Use HTML to design cards with different colors for user and assistant messages
            if msg.role == 'user':
                st.markdown(
                    f"""
                    <div style="
                        background-color: #e3f2fd;
                        border-radius: 10px;
                        padding: 12px 18px;
                        margin-bottom: 10px;
                        max-width: 70%;
                        margin-left: auto;
                        box-shadow: 0 2px 8px rgba(33,150,243,0.08);
                        border: 1px solid #90caf9;
                    ">
                        <strong style="color:#1565c0;">You:</strong> {msg.content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #f3e5f5;
                        border-radius: 10px;
                        padding: 12px 18px;
                        margin-bottom: 10px;
                        max-width: 70%;
                        margin-right: auto;
                        box-shadow: 0 2px 8px rgba(156,39,176,0.08);
                        border: 1px solid #ce93d8;
                    ">
                        <strong style="color:#6a1b9a;">Assistant:</strong> {msg.content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
        # Input for new message
        user_input = st.text_input("Type your message...", key="chat_input")
        if st.button("Send", key="send_msg_btn") and user_input.strip():
            ChatService.create_chat_message(
                db=db, chat_id=selected_chat.id,
                user_id=current_user.id,
                user_message=user_input
            )
            st.rerun()

with tab2:
    # Select a chat from history and load the chat

    st.title("💬 Your Chat History")

    # Fetch all chats for the current user
    _, user_chats, count = Chat.fetch_by_field(
        db=db, paginate=False,
        user_id=current_user.id,
        sort_by='last_active_at'
    )

    if not user_chats:
        st.info("No chats found. Start a new conversation!")
    else:
        for chat in user_chats:
            last_msg = chat.last_message or "No messages yet."
            last_active = chat.last_active_at.strftime("%Y-%m-%d %H:%M") if chat.last_active_at else "Never"
            st.markdown(
                f"""
                <div style="
                    border-radius: 12px;
                    background: linear-gradient(90deg, #e3f2fd 60%, #f3e5f5 100%);
                    padding: 18px 22px;
                    margin-bottom: 16px;
                    box-shadow: 0 2px 12px rgba(33,150,243,0.07);
                    border: 1px solid #90caf9;
                    display: flex;
                    flex-direction: column;
                ">
                    <div style="font-size: 1.1em; font-weight: 600; color: #1565c0;">
                        {chat.name or "Untitled Chat"}
                    </div>
                    <div style="color: #333; margin: 6px 0 4px 0;">
                        <span style="color:#6a1b9a; font-weight:500;">Last:</span> {last_msg}
                    </div>
                    <div style="font-size: 0.9em; color: #888;">
                        <span style="color:#1565c0;">Last active:</span> {last_active}
                    </div>
                    <form action="" method="post">
                        <button type="submit" style="
                            margin-top: 10px;
                            background: #6a1b9a;
                            color: #fff;
                            border: none;
                            border-radius: 6px;
                            padding: 6px 18px;
                            font-size: 1em;
                            cursor: pointer;
                        " onclick="window.location.search='?chat_id={chat.id}'">Open Chat</button>
                    </form>
                </div>
                """,
                unsafe_allow_html=True
            )