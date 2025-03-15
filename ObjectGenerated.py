# Object with generated riddle
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

        prompt = f"""You are an assistant helping a scavenger hunt organizer create riddles to hide 
        objects within a room. You are given a description of the object and where it is hidden in the room  
        and you are tasked with generating a 20-25 word riddle. The riddle must be specific and unambiguous, 
        clearly directing the player to the item with unambiguous clues about the objects distinctive features 
        and exact location within the room. Make sure the object's name is not included in the riddle. The object 
        description given is {riddle}"""

        response = self.model.generate_content(prompt) # Generate a riddle given the above prompt
        super()._set_riddle(response.text)