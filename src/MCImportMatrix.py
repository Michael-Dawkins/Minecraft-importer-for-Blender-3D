## @package MCImportMatrix
# @author Vlaminck Cyril
# Classe de matrice pouvant contenir et organiser les blocs contenus dans un chunk.

## Classe pouvant contenir et/ou organiser les blocs dans un chunk
#
class MCImportMatrix(object):
    
    ##Definit la taille de la matrice en X
    chunkSizeX = 0
    ##Definit la taille de la matrice en Y
    chunkSizeY = 0
    ##Definit la taille de la matirce en Z
    chunkSizeZ = 0 
    
    ##Definit si on utilise un algorithme optimise
    fastAlg = False 
    ##Decalage des bit pour trouver la position en X
    fastX = 7 
    ##Decalage des bit pour trouver la position en Y
    fastZ = 11 
    
    ##ByteArray contenant les donnees de la matrice
    chunkData = None 
    
    ## Fonction permettant la creation du tableau de byte devant contenir la matrice
    #@param self Pointeur vers la classe
    #@param x Taille en X
    #@param y Taille en Y
    #@param z Taille en Z 
    def _createMatrix(self,x,y,z):
        l = x * y * z
        return bytearray(l)
    
    ## Initialise la matrice avec la taille choisie
    #@param self Pointeur vers la classe
    #@param x Taille en X
    #@param y Taille en Y
    #@param z Taille en Z 
    def __init__(self,x = 16,y = 128,z = 16):
        if(x == 0 or y == 0 or z == 0):
            return
        self.chunkData = self._createMatrix(x,y,z)
        self.chunkSizeX = x
        self.chunkSizeY = y
        self.chunkSizeZ = z
        #Si les dimensions le permettent, on utilise l'algo rapide
        if (x == 16 and y == 128 and z == 16):
            self.fastAlg = True
        return
    
    ##Importe les valeurs depuis une chaine de Bytes
    #@param self Pointeur vers la classe
    #@param array Tableau de byte 
    def importFromBytes(self,array):
        if (len(array) != self.chunkSizeX * self.chunkSizeY * self.chunkSizeZ):
            return False
        for i in range(0, len(array)):
            self.chunkData[i] = array[i]
        return True
    
    ##Recupere la valeur a la position choisie
    #@param self Pointeur vers la classe
    #@param x Position en X
    #@param y Position en Y
    #@param z Position en Z    
    def getValue(self,x,y,z):
        if( x >= self.chunkSizeX or y >= self.chunkSizeY or z >= self.chunkSizeZ):
            return None
        if (self.fastAlg):
            return self.chunkData[y | ( x << self.fastX ) | (z << self.fastZ)]
        else:
            return self.chunkData[y + x * self.chunkSizeY + z * self.chunkSizeY * self.chunkSizeX]
    
    ##Modifie la valeur a la position choisie
    #@param self Pointeur vers la classe
    #@param x Position en X
    #@param y Position en Y
    #@param z Position en Z 
    #@param value Valeur a integrer dans la matrice 
    def setValue(self,x,y,z,value):
        if( x >= self.chunkSizeX or y >= self.chunkSizeY or z >= self.chunkSizeZ):
            return None
        if (self.fastAlg):
            self.chunkData[y | ( x << 7 ) | (z << 11)] = value
        else:
            self.chunkData[y + x * self.chunkSizeY + z * self.chunkSizeY * self.chunkSizeX] = value
        return self
    