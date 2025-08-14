import json
import re

class KeywordAnalyzer:
    def __init__(self):
        self.keywords = {
            "stress": {
                "keywords": ["worried", "overwhelmed", "nervous", "stressed", "pressure"],
                "weight": 2
            },
            "low_mood": {
                "keywords": ["sad", "down", "tired", "unmotivated"],
                "weight": 2
            },
            "positive": {
                "keywords": ["happy", "grateful", "excited", "proud"],
                "weight": 1
            }
        }
    
    def analyze_text(self, text):
        text_lower = text.lower()
        results = {}
        
        for category, data in self.keywords.items():
            found_keywords = []
            for keyword in data["keywords"]:
                if re.search(rf'\b{keyword}\b', text_lower):
                    found_keywords.append(keyword)
            
            if found_keywords:
                results[category] = {
                    "keywords": found_keywords,
                    "score": len(found_keywords) * data["weight"]
                }
        
        # Determine primary category
        if results:
            primary_category = max(results.keys(), 
                                 key=lambda x: results[x]["score"])
            return {
                "category": primary_category,
                "keywords": results[primary_category]["keywords"],
                "score": results[primary_category]["score"],
                "all_results": results
            }
        else:
            return {
                "category": "neutral",
                "keywords": [],
                "score": 0,
                "all_results": {}
            }
