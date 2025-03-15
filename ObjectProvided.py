# Class for Objects with Provided riddle
from Object import *

class ObjectProvided(Object):
    def __init__(self, riddle, room, code):
        super().__init__(riddle, room, code)
    
    def set_riddle(self, riddle):
        super()._set_riddle(riddle)