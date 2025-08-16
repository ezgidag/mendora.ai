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
        
        # Aggregate daily average intensity for the graph
        daily_avg_intensity = df.groupby(df['created_at'].dt.date)['ai_intensity'].mean().reset_index()
        daily_avg_intensity.columns = ['Date', 'Average Intensity']
        daily_avg_intensity['Date'] = pd.to_datetime(daily_avg_intensity['Date'])

        # Prepare data for display table
        df['Date'] = df['entry_date'].dt.strftime('%Y-%m-%d') # Use entry_date for consistency as per request
        df['Journal Entry'] = df['entry_text']
        df['AI Analysis Result'] = df.apply(lambda row: 
            f"Emotion: {row['ai_emotion']} (Intensity: {row['ai_intensity']}/10)\nSuggestion: {row['ai_recommendation']}", 
            axis=1
        )

        # Display AI Emotion Intensity graph (showing daily average)
        st.subheader("Daily Average Emotion Intensity Over Time")
        fig = px.line(daily_avg_intensity, x='Date', y='Average Intensity', title='Daily Average AI Emotion Intensity')
        st.plotly_chart(fig, use_container_width=True)

        # Display all journal entries in a clean table
        st.subheader("All Journal Entries")
        st.dataframe(df[['Date', 'Journal Entry', 'AI Analysis Result']], use_container_width=True)

    else:
        st.info("No journal entries yet. Start by writing in your journal!")
