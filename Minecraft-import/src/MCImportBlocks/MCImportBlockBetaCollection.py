from MCImportBlocks.MCImportBlockCollection import MCImportBlockCollection
from MCImportBlocks.MCImportBlock import MCImportBlock

class MCImportBlockBetaCollection(MCImportBlockCollection):
    
    blockIds = None
    blockDatas = None
    
    chunkSizeX = 0
    chunkSizeY = 0
    chunkSizeZ = 0
    
    def __init__(self):
        return
    
    def _createCollection(self):
        self.blockIds = bytearray( self.chunkSizeX * self.chunkSizeY * self.chunkSizeZ );
        self.blockDatas = bytearray( self.blockIds.__len__() / 2 )
        
    @staticmethod
    def fromBetaChunk(blockIds, blockDatas):
        collection = MCImportBlockBetaCollection()
        collection.blockDatas = blockDatas
        collection.blockIds = blockIds
        return collection
    
    @staticmethod
    def fromScratch():
        collection = MCImportBlockBetaCollection()
        collection._createCollection()
        return collection
    
    def getBlock(self,x,y,z):
        pos = x * 16 * 128 + z * 128 + y #Offset de l'id du bloc dans le tableau
        dpos = pos >> 1 #Offset des metadata du bloc
        s = pos & 1 #4 bit superieur ou inferieur
        
        #Creation du bloc
        block = MCImportBlock()
        blockID = self.blockIds[pos]
        block.setId(blockID)
        #Preparation des metadata
        if(s == 0):
            block.setData(self.blockDatas[dpos] & 0x0F)
        else:
            block.setData((self.blockDatas[dpos] >> 4) & 0x0F)
        return block
        