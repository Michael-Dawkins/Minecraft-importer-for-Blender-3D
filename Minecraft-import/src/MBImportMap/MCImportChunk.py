##Definit un chunk dans un fichier minecraft
class MCImportChunk(object):
    ##Initialise les informations du chunk
    #@param self Pointeur vers la classe 
    def __init__(self):
        return
    
    ##Importe les donnees d'un chunk depuis un tableau de Byte
    #@param self Pointeur vers la classe
    #@param data Tableau contenant les informations  
    def importChunkData(self, data):
        raise NotImplementedError("Not Implemented")
    
    ##Test si le bloc contient le bloc ayant pour coord absolue x, y, z
    #@param self Pointeur vers la classe
    #@param x
    #@param y
    #@param z
    def containsBlockAt(self,x,y,z):
        raise NotImplementedError("Not Implemented")
        
    ##Recupere une matrice contenant les blocs
    #@param self Pointeur vers la classe
    def getBlocks(self):
        raise NotImplementedError("Not Implemented")
    
    ##Set les coordonnees de la region contenant le chunk
    #@param self Pointeur vers la classe
    #@param x Coord en X de la region
    #@param z Coord en Z de la region
    def setRegionCoord(self,x,z):
        raise NotImplementedError("Not Implemented")
    
    ##Definit les coordonnees du chunk dans la region
    #@param self Pointeur vers la classe
    #@param x Coord en X du chunk dans la region
    #@param z Coord en Z du chunk dans la region  
    def setChunkRelativeCoord(self,x,z):
        raise NotImplementedError("Not Implemented")
    
    ##Recupere la position absolue du chunk en X
    def getChunkAbsoluteX(self):
        raise NotImplementedError("Not Implemented")
    
    ##Recupere la position absolue du chunk en Z
    def getChunkAbsoluteY(self):
        raise NotImplementedError("Not Implemented")
    
    @staticmethod
    def getChunkSizeX():
        raise NotImplementedError("Not Implemented")
    
    @staticmethod
    def getChunkSizeY():
        raise NotImplementedError("Not Implemented")
    
    @staticmethod
    def getChunkSizeZ():
        raise NotImplementedError("Not Implemented")
