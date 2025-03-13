from Object import *
from dotenv import load_dotenv
import google.generativeai as genai
import os

class ObjectGenerated(Object):
    def __init__(self, riddle, room, code):
        super().__init__(riddle, room, code)
    
    def set_riddle(self, riddle):
        load_dotenv()
        genai.configure(api_key=os.environ['API_KEY'])
        self.model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""You are an AI assistant helping a game organizer create riddles to hide 
        objects within a room. Given a description of the object and its location, generate a 
        concise and specific riddle (around 20-25 words). Emphasize the object's distinctive 
        features and its exact location, ensuring the riddle clearly directs players to the item. 
        Make sure the clues are specific and unambiguous. Absolutely do not say the object in question. 
        The object description given is {riddle}"""

        response = self.model.generate_content(prompt)
        super()._set_riddle(response.text)