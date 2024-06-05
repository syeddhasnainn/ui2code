from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

class LLMConfig():
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
    def gemini_config(self):
        genai.configure(api_key=self.gemini_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    

