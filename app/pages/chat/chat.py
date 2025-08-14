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
tab_index = st.session_state.get("tab_index", 0)

st.title('👤 Chat')

tab1, tab2 = st.tabs(['Chat', 'Chat History'])

with tab1:
    if selected_chat is None:
        st.write("Start a new chat")
        chat_name = st.text_input("Enter chat name. (Optional)", key="chat_name")
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
                user_message=new_message
            )
            st.session_state.selected_chat = chat_obj
            # st.session_state["new_chat_message"] = ""
            st.rerun()
    else:
        # Display chat messages
        _, messages, _ = Message.fetch_by_field(
            db=db, paginate=False,
            chat_id=selected_chat.id,
            order='asc'
        )

        # Improved chat bubble colors for dark backgrounds
        user_bubble_bg = "#23272f"  # deep gray for user
        user_bubble_border = "#4f8cff"
        user_text_color = "#e3f2fd"
        user_label_color = "#90caf9"

        assistant_bubble_bg = "#2d223a"  # deep purple for assistant
        assistant_bubble_border = "#b388ff"
        assistant_text_color = "#f3e5f5"
        assistant_label_color = "#ce93d8"

        for msg in messages:
            if msg.role == 'user':
                st.markdown(
                    f"""
                    <div style="
                        background-color: {user_bubble_bg};
                        border-radius: 10px;
                        padding: 14px 20px;
                        margin-bottom: 12px;
                        max-width: 70%;
                        margin-left: auto;
                        box-shadow: 0 2px 8px rgba(33,150,243,0.10);
                        border: 1.5px solid {user_bubble_border};
                        color: {user_text_color};
                        word-break: break-word;
                    ">
                        <strong style="color:{user_label_color};">You:</strong> {msg.content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div style="
                        background-color: {assistant_bubble_bg};
                        border-radius: 10px;
                        padding: 14px 20px;
                        margin-bottom: 12px;
                        max-width: 70%;
                        margin-right: auto;
                        box-shadow: 0 2px 8px rgba(156,39,176,0.10);
                        border: 1.5px solid {assistant_bubble_border};
                        color: {assistant_text_color};
                        word-break: break-word;
                    ">
                        <strong style="color:{assistant_label_color};">Assistant:</strong> {msg.content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Input for new message
        user_input = st.text_input("Type your message...", key="chat_input")
        if st.button("Send", key="send_msg_btn") and user_input.strip():
            ChatService.create_chat_message(
                db=db, chat_id=selected_chat.id,
                user_message=user_input
            )
            # st.session_state["chat_input"] = ""
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
                    background: linear-gradient(90deg, #23272f 60%, #2d223a 100%);
                    padding: 18px 22px;
                    margin-bottom: 16px;
                    box-shadow: 0 2px 12px rgba(33,150,243,0.10);
                    border: 1.5px solid #4f8cff;
                    display: flex;
                    flex-direction: column;
                ">
                    <div style="font-size: 1.1em; font-weight: 600; color: #90caf9;">
                        {chat.name or "Untitled Chat"}
                    </div>
                    <div style="color: #e3f2fd; margin: 6px 0 4px 0;">
                        <span style="color:#ce93d8; font-weight:500;">Last:</span> {last_msg}
                    </div>
                    <div style="font-size: 0.9em; color: #bdbdbd;">
                        <span style="color:#90caf9;">Last active:</span> {last_active}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button("Select Chat", key=chat.id):
                st.session_state.selected_chat = chat
                st.session_state.tab_index = 0  # Set the tab index to 0 (tab1)
                st.rerun()  # Rerun to update the UI
            