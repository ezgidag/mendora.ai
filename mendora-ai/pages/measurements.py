# pages/measurements.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db_manager import DatabaseManager

def show_measurements_page():
    st.header("📈 My Measurements")
    st.write("Here you can see your historical journal entries and analysis.")

    db_manager = DatabaseManager()
    user_id = st.session_state.user_id
    entries = db_manager.get_journal_entries_by_user(user_id)

    if entries:
        df = pd.DataFrame(entries, columns=[
            'entry_date', 'entry_text', 'detected_keywords', 'keyword_category',
            'ai_emotion', 'ai_intensity', 'ai_themes', 'ai_recommendation', 'created_at'
        ])
        df['created_at'] = pd.to_datetime(df['created_at'])
        # Ensure 'ai_intensity' is numeric, handling potential errors
        df['ai_intensity'] = pd.to_numeric(df['ai_intensity'], errors='coerce').fillna(0)
        
        # Prepare data for display table
        df['Date & Time'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['Journal Entry'] = df['entry_text']
        df['AI Analysis Result'] = df.apply(lambda row: 
            f"Emotion: {row['ai_emotion']} (Intensity: {row['ai_intensity']}/10)\nSuggestion: {row['ai_recommendation']}", 
            axis=1
        )

        # Display AI Emotion Intensity graph (using created_at for full timestamp)
        st.subheader("Emotion Intensity Over Time")
        fig = px.line(df, x='created_at', y='ai_intensity', title='AI Emotion Intensity')
        st.plotly_chart(fig, use_container_width=True)

        # Display all journal entries in a clean table
        st.subheader("All Journal Entries")
        st.dataframe(df[['Date & Time', 'Journal Entry', 'AI Analysis Result']], use_container_width=True)

    else:
        st.info("No journal entries yet. Start by writing in your journal!")
