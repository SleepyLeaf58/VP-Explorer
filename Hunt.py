# Storing Hunt information
class Hunt:
    __name = None
    __organizer = None
    objects = None
    players = None
    __start_time = None

    def __init__(self, name, organizer, objects, players, start_time):
        self.__name = name
        self.__organizer = organizer
        self.objects = objects
        self.players = players
        self.__start_time = start_time

    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name
    
    def get_organizer(self) :
        return self.__organizer

    def set_organizer(self, organizer):
        self.__organizer = organizer
    
    def get_start_time(self):
        return self.__start_time
    
    def set_start_time(self, start_time):
        self.__start_time = start_time
    
    def get_num_objects(self):
        return len(self.objects)