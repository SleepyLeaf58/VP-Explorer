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

        prompt = f"""You are an assistant working with an high school organizer to create scavenger hunt riddles to hide 
        objects within a room. You are given a description of the object and where it is hidden in the room  
        and you are to generate riddle about 20-25 words long. Do not include the name of the object in the riddle and do
        not make up unspecified characteristics of the object. The riddle should focus on the identifying characteristics 
        of the object, and clearly lead the player towards its locaation in the room. The riddle can also be humourous. 
        The description you have been given to work with is {riddle}"""

        response = self.model.generate_content(prompt) # Generate a riddle given the above prompt
        super()._set_riddle(response.text)