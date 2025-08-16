import streamlit as st
from utils.keyword_analyzer import KeywordAnalyzer
from utils.ai_feedback import AIFeedback
from utils.db_manager import DatabaseManager

def show_journal_page():
    st.header("📝 My Daily Journal")
    
    keyword_analyzer = KeywordAnalyzer()
    ai_feedback = AIFeedback()
    db_manager = DatabaseManager()

    # Text input
    user_text = st.text_area("How are you feeling today?", 
                            height=200, 
                            placeholder="Share your thoughts...")
    
    if st.button("Analyze Entry"):
        if user_text.strip():
            # Rule-based analysis
            keyword_result = keyword_analyzer.analyze_text(user_text)
            
            # AI analysis
            try:
                ai_result = ai_feedback.analyze_emotion(user_text)
            except Exception as e:
                st.error(f"AI Analysis failed. Please try again later. Error: {e}")
                return # Stop execution if AI analysis fails
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Keyword Analysis")
                st.write(f"Category: {keyword_result['category']}")
                st.write(f"Keywords found: {', '.join(keyword_result['keywords'])}")
            
            with col2:
                st.subheader("AI Insights")
                st.write(f"Emotion: {ai_result['primary_emotion']}")
                st.write(f"Intensity: {ai_result['intensity']}/10")
                st.info(ai_result['suggestion'])
            
            # Save to database
            db_manager.save_journal_entry(
                user_id=st.session_state.user_id,
                text=user_text,
                keyword_result=keyword_result,
                ai_result=ai_result
            )
            
            st.success("Entry saved successfully!")
