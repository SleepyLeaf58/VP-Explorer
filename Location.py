# Location class to track location
class Location:
    __img = None
    __x = None
    __y = None
    __floor = None

    def __init__(self, img, x, y, floor):
        self.__img = f"static/locations/{img}.jpg"
        self.__x = x
        self.__y = y
        self.__floor = floor


    def get_img(self):
        return self.__img

    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_floor(self):
        return self.__floor