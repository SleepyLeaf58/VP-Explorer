# Object class to track objects
from abc import ABC, abstractmethod

class Object:
    __riddle = None
    __room = None
    __code = None

    def __init__(self, riddle, room, code):
        self.__riddle = riddle
        self.__room = room
        self.__code = code

    # Getters and Setters
    def get_riddle(self):
        return self.__riddle
    
    @abstractmethod
    def _set_riddle(self, riddle):
        self.__riddle = riddle

    def get_room(self):
        return self.__room
    
    def set_room(self, room):
        self.__room = room

    def get_code(self):
        return self.__code
    
    def set_code(self, code):
        self.__code = code

    def __str__(self):
        return f"('{self.__riddle}', '{self.__room}', '{self.__code})"