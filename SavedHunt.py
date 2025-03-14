class SavedHunt:
    __id = None
    __name = None
    __organizer = None
    objects = None

    def __init__(self, id, name, organizer, objects):
        self.__id = id
        self.__name = name
        self.__organizer = organizer
        self.objects = objects

    def get_id(self):
        return self.__id
    
    def set_id(self, name):
        self.__name = id

    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name
    
    def get_organizer(self) :
        return self.__organizer

    def set_organizer(self, organizer):
        self.__organizer = organizer