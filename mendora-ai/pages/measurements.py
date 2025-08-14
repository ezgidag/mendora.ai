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
            'ai_emotion', 'ai_intensity', 'ai_themes', 'ai_recommendation'
        ])
        df['entry_date'] = pd.to_datetime(df['entry_date'])
        df = df.sort_values(by='entry_date')

        # Ensure 'ai_intensity' is numeric, handling potential errors
        df['ai_intensity'] = pd.to_numeric(df['ai_intensity'], errors='coerce').fillna(0)

        # Debugging: Display the DataFrame
        st.write("Debug: DataFrame content for Emotion Intensity")
        st.write(df)

        st.subheader("Emotion Intensity Over Time")
        fig = px.line(df, x='entry_date', y='ai_intensity', title='AI Emotion Intensity')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("All Journal Entries")
        for index, row in df.iterrows():
            st.markdown(f"**Date: {row['entry_date'].strftime('%Y-%m-%d')}**")
            st.write(f"Entry: {row['entry_text']}")
            st.write(f"Keyword Analysis: {row['keyword_category']} (Keywords: {row['detected_keywords']})")
            st.write(f"AI Emotion: {row['ai_emotion']} (Intensity: {row['ai_intensity']}/10)")
            st.info(f"AI Recommendation: {row['ai_recommendation']}")
            st.markdown("--- unskilled")

    else:
        st.info("No journal entries yet. Start by writing in your journal!")
