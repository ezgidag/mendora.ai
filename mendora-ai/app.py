import streamlit as st
from pages import home
from utils import auth, db_manager

def main():
    st.set_page_config(page_title="Mendora.AI", page_icon="🧠", initial_sidebar_state="collapsed")
    
    # Initialize database
    db = db_manager.DatabaseManager()
    db.init_database()
    
    # Authentication
    if not auth.check_authentication():
        auth.show_login_page()
        return
    
    # Temporary user_id for demonstration until auth is fully implemented
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 1 # Assuming a default user with ID 1 for now

    # Display home page after successful login
    home.show_home_page()

if __name__ == "__main__":
    main()
