import streamlit as st
from db.database import load_db
from services.user import UserService
from utils.messages import generate_message
from services.auth import AuthService


AuthService.protect_page()

db = load_db()
current_user = st.session_state.current_user

st.markdown("## Profile")
st.caption("Manage your account and preferences.")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Profile", "Edit profile", "Photo", "Password"]
)

with tab1:
    user_data = {
        "name": st.session_state.current_user.name,
        "email": st.session_state.current_user.email,
        "profile_pic": st.session_state.current_user.profile_picture,
    }
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(user_data["profile_pic"], width=100)
    with col2:
        st.markdown(f"**{user_data['name']}**")
        st.caption(user_data["email"])

with tab2:
    st.markdown("**Edit profile**")
    with st.form("edit_profile"):
        name = st.text_input("Full name", value=current_user.name).strip()
        email = st.text_input("Email", value=current_user.email).strip()
        edit_profile_submit = st.form_submit_button("Save", type="primary")
    if edit_profile_submit:
        UserService.update_profile(
            db, name=name, email=email, profile_picture_file=None
        )

with tab3:
    st.markdown("**Profile photo**")
    st.image(st.session_state.current_user.profile_picture, width=120)
    uploaded_file = st.file_uploader(
        "Upload a new photo", type=["png", "jpg", "jpeg"]
    )
    if uploaded_file is not None:
        st.success(generate_message("File uploaded successfully"))
        if uploaded_file.type.startswith("image/"):
            st.image(uploaded_file, caption="Preview", width=120)
    else:
        st.caption("Choose an image to upload.")
    with st.form("change_profile_picture"):
        submit = st.form_submit_button("Save", type="primary")
        if submit and uploaded_file is not None:
            UserService.update_profile(
                db,
                name=None,
                email=None,
                profile_picture_file=uploaded_file,
            )
        elif submit and uploaded_file is None:
            st.warning("Please upload an image first.")

with tab4:
    st.markdown("**Change password**")
    with st.form("change_password"):
        st.text_input("Email", value=current_user.email, disabled=True)
        old_password = st.text_input(
            "Current password", type="password", placeholder="••••••••"
        ).strip()
        new_password = st.text_input(
            "New password", type="password", placeholder="••••••••"
        ).strip()
        confirm_password = st.text_input(
            "Confirm new password", type="password", placeholder="••••••••"
        ).strip()
        change_password_submit = st.form_submit_button("Save", type="primary")
    if change_password_submit:
        UserService.change_password(
            db,
            email=current_user.email,
            old=old_password,
            new=new_password,
            confirm=confirm_password,
        )
