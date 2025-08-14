import google.generativeai as genai
import json
import os

class AIFeedback:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_emotion(self, text):
        prompt = f"""
        Analyze this journal entry for emotional content:
        
        Text: "{text}"
        
        Provide analysis in JSON format:
        {{
            "primary_emotion": "happiness|sadness|stress|frustration|neutral",
            "intensity": 1-10,
            "themes": ["theme1", "theme2"],
            "suggestion": "Brief helpful suggestion"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_json = json.loads(response.text)
            # Ensure intensity is an integer
            if 'intensity' in response_json:
                try:
                    response_json['intensity'] = int(response_json['intensity'])
                except ValueError:
                    response_json['intensity'] = 5 # Default to 5 if conversion fails
            return response_json
        except Exception as e:
            return {
                "primary_emotion": "neutral",
                "intensity": 5,
                "themes": [],
                "suggestion": "Thank you for sharing your thoughts."
            }
