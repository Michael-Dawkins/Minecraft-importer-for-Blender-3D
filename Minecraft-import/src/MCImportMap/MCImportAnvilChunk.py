from MCImportMap.MCImportChunk import MCImportChunk
from MCImportMap.MCImportAnvilSection import MCImportAnvilSection
from MCImportBlocks.MCImportBlockAnvilCollection import MCImportBlockAnvilCollection
from MCImportNBT import *

class MCImportAnvilChunk(MCImportChunk):
    chunkDataStruct = None
    chunkTagCompound = None
    chunkSections = None
    
    regionX = 0
    regionZ = 0
    chunkX = 0
    chunkZ = 0
    
    def __init__(self):
        self.chunkSections = [];
        return
     
    def importChunkData(self, data):
        self.chunkDataStruct = data
        self.chunkTagCompound = MCImportNBTTagCompound()
        if (self.chunkTagCompound.fromBytes(data) == False):
            return False
        #On test si les sections sont presentes
        if not self.chunkTagCompound.containsTagWithName("Level"):
            return False
        level = self.chunkTagCompound.getTagByName("Level")[0]
        #On recupere la liste de Section contenue par le chunk
        if not level.containsTagWithName("Sections"):
            return False;
        sections = level.getTagByName("Sections")[0]
        for i in range(0, len(sections)):
            #On genere l'objet section
            s = MCImportAnvilSection()
            s.importSectionData(sections.get(i))
            #On les ajoutes a la liste
            self.chunkSections.append(s)
        return True
    
    def containsBlockAt(self,x,y,z):
        raise NotImplementedError("Not Implemented")
        
    def getBlocks(self):
        if self.chunkSections is None:
            return None
        blocks = MCImportBlockAnvilCollection()
        for s in self.chunkSections:
            y = s.getY()
            #On recupere les differentes parties ( Block, Data, AddBlock )
            #TODO: Simplifier le process ( fonction containsBlockDatas, containsBlockAddBlocks dans Section )
            blockIds = s.getBlockIds().getValue()
            cBlockDatas = s.getBlockDatas()
            if cBlockDatas is None:
                blockDatas = None
            else:
                blockDatas = cBlockDatas.getValue()
            cBlockAddBlocks = s.getBlockAddBlocks()
            if cBlockAddBlocks is None:
                blockAddBlocks = None
            else:
                blockAddBlocks = cBlockAddBlocks.getValue()
            #On ajoute la section dans la collection
            blocks.addSectionToCollection(y, blockIds, blockDatas, blockAddBlocks)
        return blocks
    
    def setRegionCoord(self,x,z):
        self.regionX = x
        self.regionZ = z
    
    def setChunkRelativeCoord(self,x,z):
        self.regionX = x
        self.regionZ = z
    
    def getChunkAbsoluteX(self):
        return self.chunkX + self.regionX * 32;
    
    def getChunkAbsoluteY(self):
        return self.chunkZ + self.regionZ * 32;
    
    @staticmethod
    def getChunkSizeX():
        return 16
    
    @staticmethod
    def getChunkSizeY():
        return 256
    
    @staticmethod
    def getChunkSizeZ():
        return 16