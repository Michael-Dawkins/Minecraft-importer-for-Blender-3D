#This class represents the current World where all the players evolved
#Store time, chunks, entities, etc...
class World(object):
    
    def __init__(self):
        self.__time = 0
        
    def setTime(self,time):
        self.__time = time % 24000
        
    def getTime(self):
        return self.__time

#This class represents the current connected player
#For now, this only use is to store all the informations
#Maybe i will extend its functionnalities later...
class Player(object):
    
    def __init__(self):
        self.__name = "JeanKevin"
        return
        
    def setName(self,name):
        self.__name = name
        
    def getName(self):
        return self.__name
        
    def setEntityId(self,eid):
        self.__entityId = eid
        
    def setDimension(self,dimension):
        self.__dimension = dimension
        
    def setPosition(self,position):
        self.__x = position[0]
        self.__y = position[1]
        self.__z = position[2]        
