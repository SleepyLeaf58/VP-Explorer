class ScoreEntry:
    __name = None
    __score = None
    __time = None

    def __init__(self, name, score, time):
        self.__name = name
        self.__score = score
        self.__time = time

    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name

    def get_score(self):
        return self.__score
    
    def set_score(self, score):
        self.__score= score

    def get_time(self):
        return self.__time
    
    def set_time(self, time):
        self.__time = time

    def get_time_string(self):
        total_seconds = int(self.__time)
        hours = int(total_seconds // 3600)
        total_seconds %= 3600
        minutes = int(total_seconds // 60)
        total_seconds %= 60
        seconds = int(total_seconds)

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

