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

        prompt = f"""As an assistent working with an high school organizer to create scavenger hunt, you are tasked with creating
         riddles to hide to objects within a room. You will be given a description of the object and where it is hidden in the room  
        and you are to generate a 20-25 word riddle to hint at its location and identity. Do not include the name of the object in 
        the riddle and do not make up characteristics of the object that were not clearly specified in the description. 
        The riddle should focus on the identifying characteristics of the object, and clearly lead the player towards its 
        locaation in the room. The riddle can also be humourous. Following description is what you are to use to create
        the riddle: {riddle}"""

        response = self.model.generate_content(prompt) # Generate a riddle given the above prompt
        super()._set_riddle(response.text)