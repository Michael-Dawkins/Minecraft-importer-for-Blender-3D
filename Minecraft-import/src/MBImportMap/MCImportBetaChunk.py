## Representation d'un chunk.
from MCImportNBT import *
from MBImportMap.MCImportChunk import MCImportChunk
from MCImportBlocks.MCImportBlockBetaCollection import MCImportBlockBetaCollection

class MCImportBetaMapChunk(MCImportChunk):
    ##Contient un tableau de byte contenant les informations du chunk
    chunkDataStruct = None
    ##Structure NBT du chunk (TagCompound)
    chunkTagCompound = None
    
    #Information sur la position du chunk
    regionX = 0 #Coord en X de la region contenant le chunk
    regionZ = 0 #Coord en Z de la region contenant le chunk
    chunkX = 0 #Coord en X du chunk dans la region
    chunkZ = 0 #Coord en Z du chunk dans la region
    
    def __init__(self):
        return
    
    def importChunkData(self, data):
        self.chunkDataStruct = data
        self.chunkTagCompound = MCImportNBTTagCompound()
        if (self.chunkTagCompound.fromBytes(data) == False):
            return False
        #Il s'agit d'un patch dans le cas ou Level n'est pas la racine de la structure
        if(self.chunkTagCompound.containsTagWithName("Level")):
            self.chunkTagCompound = self.chunkTagCompound.getTagByName("Level")[0]
        return True
    
    def containsBlockAt(self,x,y,z):
        if(y < 0 or y >= self.getChunkSizeY()):
            return False
        if(x < self.getChunkSizeX() * self.getChunkAbsoluteX() or x >= self.getChunkSizeX() * (self.getChunkAbsoluteX() + 1)):
            return False
        if(z < self.getChunkSizeZ() * self.getChunkAbsoluteZ() or z >= self.getChunkSizeZ() * (self.getChunkAbsoluteZ() + 1)):
            return False
        return True
    
    def getBlocks(self):
        if(self.chunkTagCompound is None):
            return None
        blocks = self.chunkTagCompound.getTagByName("Blocks")
        datas = self.chunkTagCompound.getTagByName("Data")
        if(blocks is None or len(blocks) == 0):
            return None
        block = blocks[0]
        data = datas[0]
        collection = MCImportBlockBetaCollection.fromBetaChunk(block.tagData, data.tagData)
        return collection
    
    def setRegionCoord(self,x,z):
        self.chunkX = x
        self.chunkZ = z
        return
    
    def setChunkRelativeCoord(self,x,z):
        self.chunkX = x
        self.chunkZ = z
        return
    
    def getChunkAbsoluteX(self):
        return self.chunkX + self.regionX * 32;
    
    def getChunkAbsoluteY(self):
        return self.chunkZ + self.regionZ * 32;
    
    @staticmethod
    def getChunkSizeX():
        return 16
    
    @staticmethod
    def getChunkSizeY():
        return 16
    
    @staticmethod
    def getChunkSizeZ():
        return 128