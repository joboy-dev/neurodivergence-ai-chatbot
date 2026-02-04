from datetime import datetime, timezone
import streamlit as st

from db.database import load_db
from services.auth import AuthService
from services.chat import ChatService
from db.models.chat import Chat, Message
from app.components.ui import render_user_bubble, render_assistant_bubble, render_chat_history_item


AuthService.protect_page()

db = load_db()
current_user = st.session_state.current_user
selected_chat = st.session_state.get("selected_chat", None)

st.markdown("## Chat")
st.caption("Ask anything about neurodiversity support. Start a new chat or continue from history.")

tab1, tab2 = st.tabs(["Conversation", "History"])

with tab1:
    if selected_chat is None:
        st.markdown("**New conversation**")
        chat_name = st.text_input(
            "Chat name (optional)",
            key="chat_name",
            placeholder="e.g. Bedtime routines",
        )
        new_message = st.text_input(
            "Your message",
            key="new_chat_message",
            placeholder="Type your message here...",
        )
        if st.button("Start chat", key="start_chat_btn", type="primary") and new_message.strip():
            chat_obj = Chat.create(
                db=db,
                name=chat_name.strip() or "New chat",
                last_message=new_message,
                last_active_at=datetime.now(timezone.utc),
                user_id=current_user.id,
            )
            ChatService.create_chat_message(
                db=db, chat_id=chat_obj.id, user_message=new_message
            )
            st.session_state.selected_chat = chat_obj
            st.rerun()
    else:
        st.caption(f"Conversation: **{selected_chat.name or 'Untitled'}**")
        _, messages, _ = Message.fetch_by_field(
            db=db, paginate=False, chat_id=selected_chat.id, order="asc"
        )

        for msg in messages:
            if msg.role == "user":
                render_user_bubble(msg.content)
            else:
                render_assistant_bubble(msg.content)

        st.markdown("---")
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input(
                "Type your message",
                key="chat_input",
                placeholder="Message...",
                label_visibility="collapsed",
            )
        with col2:
            send_clicked = st.button("Send", key="send_msg_btn", type="primary")
        if send_clicked and user_input.strip():
            ChatService.create_chat_message(
                db=db, chat_id=selected_chat.id, user_message=user_input
            )
            st.rerun()

        if st.button("New chat", key="new_chat_btn"):
            st.session_state.selected_chat = None
            st.rerun()

with tab2:
    st.markdown("**Your conversations**")
    _, user_chats, _ = Chat.fetch_by_field(
        db=db, paginate=False, user_id=current_user.id, sort_by="last_active_at"
    )

    if not user_chats:
        st.info("No conversations yet. Start one from the **Conversation** tab.")
    else:
        for chat in user_chats:
            last_msg = chat.last_message or "No messages yet."
            last_active = (
                chat.last_active_at.strftime("%b %d, %H:%M")
                if chat.last_active_at
                else "—"
            )
            render_chat_history_item(
                chat.name or "Untitled", last_msg, last_active, str(chat.id)
            )
            if st.button("Open", key=chat.id):
                st.session_state.selected_chat = chat
                st.rerun()
