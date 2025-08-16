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
            response = self.model.generate_content(prompt, timeout=60) # Add timeout in seconds
            
            # Debugging: Print entire response object to logs
            print(f"Raw Gemini API response object: {response}")

            response_text = response.text
            
            # Debugging: Print raw response text to logs
            print(f"Raw Gemini API response text: {response_text}")
            
            if not response_text or not response_text.strip():
                raise ValueError("Empty or invalid response from Gemini API.")

            # Attempt to parse JSON response
            try:
                response_json = json.loads(response_text)
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e} - Response Text: {response_text}")
                raise ValueError(f"Invalid JSON response from AI: {e}")

            # Debugging: Print parsed JSON to logs
            print(f"Parsed Gemini API JSON: {response_json}")

            # Ensure intensity is an integer
            if 'intensity' in response_json:
                try:
                    response_json['intensity'] = int(response_json['intensity'])
                except ValueError:
                    print(f"Intensity conversion error: {response_json.get('intensity')} is not an integer. Defaulting to 5.")
                    response_json['intensity'] = 5 # Default to 5 if conversion fails
            else:
                print("Intensity field missing in AI response. Defaulting to 5.")
                response_json['intensity'] = 5 # Default if field is missing

            # Ensure themes is a list
            if 'themes' in response_json and not isinstance(response_json['themes'], list):
                print(f"Themes field not a list: {response_json.get('themes')}. Defaulting to empty list.")
                response_json['themes'] = []
            elif 'themes' not in response_json:
                print("Themes field missing in AI response. Defaulting to empty list.")
                response_json['themes'] = []

            return response_json
        except Exception as e:
            print(f"General AI Feedback Error: {e}") # Log general errors
            return {
                "primary_emotion": "neutral",
                "intensity": 0, # Default to 0 for intensity on error
                "themes": [],
                "suggestion": "AI analysis failed. Please try again later.",
                "error": str(e) # Pass the error message
            }
