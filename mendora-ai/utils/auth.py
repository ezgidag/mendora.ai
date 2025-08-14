import streamlit as st
import hashlib
from utils.db_manager import DatabaseManager

db = DatabaseManager()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_authentication():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    return st.session_state.logged_in

def show_login_page():
    st.title("Mendora.AI Login / Register")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_button"):
            if login_user(username, password):
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with register_tab:
        st.subheader("Register")
        new_username = st.text_input("New Username", key="register_username")
        new_email = st.text_input("New Email", key="register_email")
        new_password = st.text_input("New Password", type="password", key="register_password")
        if st.button("Register", key="register_button"):
            if register_user(new_username, new_email, new_password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Registration failed. Username or email might already exist.")

def login_user(username, password):
    conn = db.get_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username = ? AND password_hash = ?", (username, hashed_password))
    user = cursor.fetchone()
    db.close_connection()
    if user:
        st.session_state.user_id = user[0]
        return True
    return False

def register_user(username, email, password):
    conn = db.get_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                       (username, email, hashed_password))
        conn.commit()
        db.close_connection()
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        db.close_connection()
        return False
