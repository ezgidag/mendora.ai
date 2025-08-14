import streamlit as st

def show_home_page():
    st.title("Welcome to Mendora.AI")
    st.write("Your personal wellness companion.")

    st.markdown("## Choose your path:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 My Journal", help="Write your daily thoughts and feelings."):
            st.session_state.current_page = "journal"
            st.rerun()

    with col2:
        if st.button("✨ Affirmations", help="Receive positive daily messages."):
            st.session_state.current_page = "affirmations"
            st.rerun()

    with col3:
        if st.button("📈 My Measurements", help="View your historical data and insights."):
            st.session_state.current_page = "measurements"
            st.rerun()

    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    if st.session_state.current_page == "journal":
        from pages.journal import show_journal_page
        show_journal_page()
    elif st.session_state.current_page == "affirmations":
        from pages.affirmations import show_affirmations_page
        show_affirmations_page()
    elif st.session_state.current_page == "measurements":
        from pages.measurements import show_measurements_page
        show_measurements_page()
    elif st.session_state.current_page == "home":
        pass # Stay on the home page
