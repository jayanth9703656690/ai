import streamlit as st
import json
import os
import hashlib
from datetime import date
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# ---------- CONFIG ----------
icon = "LOGO.jpeg" if os.path.exists("LOGO.jpeg") else "🔍"
st.set_page_config(page_title="REAIL", page_icon=icon, layout="centered")
USERS_FILE = "users.json"
DAILY_LIMIT = 5
ADMIN_USERNAME = "admin"

# ---------- DARK THEME ----------
st.markdown("""
<style>
.stApp { background-color: #0e1117; color: #fafafa; }
.stButton>button { background-color: #ff4b4b; color: white; border-radius: 8px; }
.stTextInput>div>div>input { background-color: #262730; color: white; }
</style>
""", unsafe_allow_html=True)

# ---------- CACHED MODEL LOADER ----------
@st.cache_resource
def load_detector_model():
    if os.path.exists('detector1.h5'):
        return load_model('detector1.h5')
    return None

# ---------- USER STORAGE ----------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# ---------- LANDING / AUTH ----------
def show_landing():
    if os.path.exists("LOGO.jpg"):
        st.image("LOGO.jpg", width=200)
    st.markdown("<h1 style='text-align:center;'>REAIL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>AI Image Detector — tell real from AI-generated, instantly.</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    **About this project:** REAIL uses a MobileNetV2-based transfer learning model trained on the CIFAKE dataset to classify images as real or AI-generated.

    **Disclaimer:** This tool is a demonstration project and not intended for forensic, legal, or production use. Predictions may not always be accurate.
    """)
    st.markdown("---")

    tab1, tab2 = st.tabs(["Login", "Register"])
    users = load_users()

    with tab1:
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if login_user in users and users[login_user]["password"] == hash_password(login_pass):
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        reg_user = st.text_input("Choose a username", key="reg_user")
        reg_pass = st.text_input("Choose a password", type="password", key="reg_pass")
        if st.button("Register"):
            if reg_user in users:
                st.error("Username already exists.")
            elif reg_user and reg_pass:
                users[reg_user] = {
                    "password": hash_password(reg_pass),
                    "uploads_today": 0,
                    "last_upload_date": str(date.today()),
                    "premium": False
                }
                save_users(users)
                st.success("Registered! Please log in.")
            else:
                st.error("Please fill both fields.")

# ---------- MAIN APP ----------
def show_main_app():
    users = load_users()
    username = st.session_state.username
    user_data = users.get(username, {
        "uploads_today": 0,
        "last_upload_date": str(date.today()),
        "premium": False
    })

    # Reset daily count if it's a new day
    if user_data.get("last_upload_date") != str(date.today()):
        user_data["uploads_today"] = 0
        user_data["last_upload_date"] = str(date.today())
        save_users(users)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### Welcome, {username}")
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

    is_admin = (username == ADMIN_USERNAME)
    remaining = "Unlimited" if is_admin else max(0, DAILY_LIMIT - user_data.get("uploads_today", 0))
    st.info(f"Uploads remaining today: {remaining}")

    if not is_admin and user_data.get("uploads_today", 0) >= DAILY_LIMIT:
        st.warning("You have hit your daily limit of 5 uploads.")
        st.markdown("### Upgrade to Premium for unlimited uploads")
        if st.button("Upgrade to Premium (Demo)"):
            st.success("This is a demo — real payment integration coming soon!")
        return

    model = load_detector_model()
    if model is None:
        st.error("Model file `detector1.h5` not found. Please ensure `detector1.h5` is in the project directory.")
        return

    file = st.file_uploader("Upload an image", type=['jpg', 'png', 'jpeg'])

    if file:
        img = Image.open(file).convert('RGB').resize((96, 96))
        arr = np.expand_dims(np.array(img) / 255.0, axis=0)

        with st.spinner("Analyzing..."):
            pred = model.predict(arr)[0][0]

        label = "AI-Generated" if pred > 0.5 else "Real"
        confidence = pred if pred > 0.5 else 1 - pred

        c1, c2 = st.columns([1, 1])
        with c1:
            try:
                st.image(Image.open(file), use_container_width=True)
            except TypeError:
                st.image(Image.open(file), use_column_width=True)
        with c2:
            if label == "Real":
                st.success(f"Result: {label}")
            else:
                st.error(f"Result: {label}")
            st.metric("Confidence", f"{confidence:.1%}")
            st.progress(float(confidence))

        if not is_admin:
            user_data["uploads_today"] = user_data.get("uploads_today", 0) + 1
            save_users(users)

# ---------- ROUTING ----------
if st.session_state.logged_in:
    show_main_app()
else:
    show_landing()
