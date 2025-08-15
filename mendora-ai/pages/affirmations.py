# pages/affirmations.py
import streamlit as st
import json
from datetime import date
import random
from utils.db_manager import DatabaseManager
import os # Added for path manipulation

def show_affirmations_page():
    st.header("✨ Daily Affirmations")

    db = DatabaseManager()
    user_id = st.session_state.user_id

    # Construct the path to affirmations.json robustly
    affirmations_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "affirmations.json")

    # Load affirmations from JSON file
    try:
        with open(affirmations_file_path, "r", encoding="utf-8") as f:
            affirmations = json.load(f)
    except FileNotFoundError:
        st.error(f"Affirmations data file not found at: {affirmations_file_path}") # Added path to error
        return

    today = date.today()

    # Check if an affirmation has been shown today
    if "daily_affirmation_date" not in st.session_state or st.session_state.daily_affirmation_date != today:
        # Get last displayed affirmation date for the user
        last_displayed_date = db.get_last_affirmation_date(user_id)

        if last_displayed_date and last_displayed_date == str(today):
            # If already displayed today, retrieve from session state (should not happen if logic is correct)
            selected_affirmation = {
                "id": st.session_state.daily_affirmation_id,
                "text": st.session_state.daily_affirmation_text
            }
        else:
            # Select a new affirmation
            # For simplicity, just pick a random one for now. 
            # In a more advanced version, we'd avoid recent repetitions.
            selected_affirmation = random.choice(affirmations)
            
            # Save to session state
            st.session_state.daily_affirmation_date = today
            st.session_state.daily_affirmation_id = selected_affirmation["id"]
            st.session_state.daily_affirmation_text = selected_affirmation["text"]
            
            # Log the display
            db.save_affirmation_log(user_id, selected_affirmation["id"], today)
    else:
        # Affirmation already selected for today
        selected_affirmation = {
            "id": st.session_state.daily_affirmation_id,
            "text": st.session_state.daily_affirmation_text
        }

    st.info(selected_affirmation["text"])

    st.markdown("--- unskilled")

    if st.button("Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()
