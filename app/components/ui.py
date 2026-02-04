"""Shared UI components and global styles for the chatbot app."""

import streamlit as st


def inject_global_styles():
    """Inject global CSS for a modern chatbot look. Call once per page (e.g. from run.py)."""
    st.markdown(
        """
        <style>
        /* Hide Streamlit branding and reduce padding for chat-first layout */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        .stDeployButton { display: none; }
        div[data-testid="stToolbar"] { display: none; }

        /* Tighter, cleaner main block */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 900px;
        }

        /* Modern tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: transparent;
            border-bottom: 1px solid rgba(99, 102, 241, 0.2);
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.6rem 1.2rem;
            border-radius: 8px 8px 0 0;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(99, 102, 241, 0.15);
            color: #a5b4fc;
        }

        /* Input and button consistency */
        .stTextInput input, .stTextInput textarea {
            border-radius: 12px;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        .stButton > button {
            border-radius: 10px;
            font-weight: 500;
        }

        /* Form cards */
        .chatbot-card {
            background: linear-gradient(145deg, #1a1a24 0%, #16161d 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_user_bubble(content: str) -> None:
    """Render a user message bubble (right-aligned, distinct color)."""
    escaped = content.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #2d2d3a 0%, #252532 100%);
            border: 1px solid rgba(99, 102, 241, 0.35);
            border-radius: 18px 18px 4px 18px;
            padding: 14px 18px;
            margin: 10px 0;
            max-width: 78%;
            margin-left: auto;
            margin-right: 0;
            color: #e4e4e7;
            font-size: 0.95rem;
            line-height: 1.5;
            word-break: break-word;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
        ">{escaped}</div>
        """,
        unsafe_allow_html=True,
    )


def render_assistant_bubble(content: str) -> None:
    """Render an assistant message bubble (left-aligned)."""
    escaped = content.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #1e1e2a 0%, #252532 100%);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 18px 18px 18px 4px;
            padding: 14px 18px;
            margin: 10px 0;
            max-width: 78%;
            margin-right: auto;
            margin-left: 0;
            color: #e4e4e7;
            font-size: 0.95rem;
            line-height: 1.5;
            word-break: break-word;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
        ">{escaped}</div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_history_item(name: str, last_msg: str, last_active: str, chat_id: str) -> None:
    """Render a single chat history card (caller still adds the button)."""
    name_esc = name.replace("<", "&lt;").replace(">", "&gt;")
    msg_esc = (last_msg or "No messages yet.")[:80].replace("<", "&lt;").replace(">", "&gt;")
    st.markdown(
        f"""
        <div style="
            border-radius: 14px;
            background: linear-gradient(145deg, #1a1a24 0%, #16161d 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            padding: 1rem 1.25rem;
            margin-bottom: 12px;
            transition: border-color 0.2s;
        ">
            <div style="font-weight: 600; color: #a5b4fc; font-size: 1rem;">{name_esc}</div>
            <div style="color: #94a3b8; font-size: 0.875rem; margin-top: 4px;">{msg_esc}</div>
            <div style="color: #64748b; font-size: 0.8rem; margin-top: 4px;">{last_active}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
