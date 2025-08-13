import streamlit as st
from services.auth import AuthService

def load_pages():
    pages = [
        {"page": "app/pages/auth/auth.py", "title": "Auth", "url_path": "/auth", "icon": "🔑"},
        {"page": "app/pages/chat/chat.py", "title": "Chat", "url_path": "/chat", "icon": "💬"},
        {"page": "app/pages/user/profile.py", "title": "Profile", "url_path": "/profile", "icon": "👤"},
        {"page": "app/pages/auth/logout.py", "title": "Logout", "url_path": "/logout", "icon": "🚪"},
    ]
    
     # Filter out login and register if the user is authenticated
    if AuthService.is_authenticated():
        pages = [
            p for p in pages 
            if p["url_path"] not in [
                "/auth"
            ]
        ]
    else:
        pages = [
            p for p in pages 
            if p["url_path"] not in [
                "/", "/logout", "/profile", 
                "/chat"
            ]
        ]

    # Convert to Streamlit Page objects
    st_pages = [
        st.Page(
            page=p["page"], 
            title=p["title"], 
            url_path=p["url_path"], 
            icon=p['icon']
        ) 
        for p in pages
    ]

    # Navigation
    pg = st.navigation(st_pages)
    pg.run()
