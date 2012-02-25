

class MCImportBlock(object):
    
    blockId = 0
    blockData = 0
    
    ##Initialise un nouveau bloc
    def __init__(self):
        self.blockId = 0
        self.blockData = 0
        return
    
    ##Recupere l'id du bloc
    def getId(self):
        return self.blockId
    
    
    ##Recupere les metadonnees du bloc dans l'ancien systeme minecraft
    def getData(self):
        return self.blockData

    ##Set l'id du bloc
    #@param self
    #@param id Id du bloc
    def setId(self, blockId):
        self.blockId = blockId 
        return
    
    #Set les metadonnees du bloc
    def setData(self,data):
        self.blockData = data
        return
        