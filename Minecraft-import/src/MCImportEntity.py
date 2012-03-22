class Player(object):
    
    def __init__(self):
        self.__name = "JeanKevin"
        return
        
    def setName(self,name):
        self.__name = name
        
    def getName(self):
        return self.__name
        
    def setEntityId(self,id):
        self.__entityId = id
        
    def setDimension(self,dimension):
        self.__dimension = dimension
        
    def setPosition(self,x,y,z):
        self.__x = x
        self.__y = y
        self.__z = z 