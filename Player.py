class Player:
    __id = None
    __name = None
    __current_object = None
    __start_time = None
    __current_time = None
    __finished = None

    def __init__(self, id, name, current_object, start_time, current_time, finished):
        self.__id = id
        self.__name = name
        self.__current_object = current_object
        self.__start_time = start_time
        self.__current_time = current_time
        self.__finished = finished

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name
    
    def get_current_object(self):
        return self.__current_object
    
    def set_current_object(self, current_object):
        self.__current_object = current_object
    
    def get_start_time(self):
        return self.__start_time
    
    def set_start_time(self, start_time):
        self.__start_time = start_time

    def get_current_time(self):
        return self.__current_time
    
    def set_current_time(self, current_time):
        self.__current_time = current_time
    
    def get_finished(self):
        return self.__finished
    
    def set_finished(self, finished):
        self.__finished = finished

    def __str__(self):
        return f"('{self.__name}', '{self.__current_object}', '{self.__start_time}', '{self.__current_time}', '{self.__finished}')"