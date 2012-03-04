
##Permet l'importation d'un fichier de region minecraft
class MCImportRegion(object):
    
    def __init__(self):
        return
    
    ##Test si le fichier de region est ouvert
    #@param self Pointeur vers la classe
    def isOpened(self):
        raise NotImplementedError("Not implemented")
    
    ##Verifie si un nom de fichier est un nom de region valide
    #@param self Pointeur vers la classe
    #@param fileName Nom du fichier a tester  
    def isValidMCRegionFilename(self, fileName):
        raise NotImplementedError("Not implemented")
    
    ##Ouvre un fichier region minecraft
    #@param self Pointeur vers la classe
    #@param filePath Chemin vers le fichier de region .mcr  
    def openMCRegion(self, filePath):
        raise NotImplementedError("Not implemented")
    
    ## Ferme le stream vers le fichier de la region
    #@param self Pointeur vers la classe 
    def closeMCRegion(self):
        raise NotImplementedError("Not implemented")
    
    ##Recupere un tableau de Byte contenant une structure NBT du chunk
    #@param self Pointeur vers la classe
    #@param x Position en X du chunk
    #@param z Position en Z du chunk
    def getChunk(self,x,z):
        raise NotImplementedError("Not implemented")

        