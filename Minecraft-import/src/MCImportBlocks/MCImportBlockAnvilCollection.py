from MCImportBlocks.MCImportBlock import MCImportBlock
import copy

class MCImportBlockAnvilCollection(object):

    blockAddBlocks = None
    blockIds = None
    blockDatas = None

    def __init__(self):
        self.blockAddBlocks = dict()
        self.blockIds = dict()
        self.blockDatas = dict()
        return
    
    def copy(self):
        cpCollection = MCImportBlockAnvilCollection()
        cpCollection.blockAddBlocks = copy.deepcopy(self.blockAddBlocks)
        cpCollection.blockDatas = copy.deepcopy(self.blockDatas)
        cpCollection.blockIds = copy.deepcopy(self.blockIds)
        return cpCollection
    
    def addSectionToCollection(self,y,blockIds,blockDatas,blockAddBlocks):
        if y > 15:
            return;
        self.blockIds[y] = blockIds
        self.blockDatas[y] = blockDatas
        self.blockAddBlocks[y] = blockAddBlocks
        
    def hasBlock(self,x,y,z):
        pos = (y & 0x0F) + (z << 4 ) + (x << 8)
        posY = y >> 4
        blockIds = self.blockIds.get(posY)
        if blockIds is None:
            return False;
        return (blockIds[pos] != 0)
    
    def setBlock(self,x,y,z,block):
        pos = (y & 0x0F) + (z << 4 ) + (x << 8)
        posY = y >> 4
        
        #Test if the section exist
        blockIds = self.blockIds.get(posY)
        blockDatas = self.blockDatas.get(posY)
        blockAddBlocks = self.blockAddBlocks.get(posY)
        if blockIds is None:
            #If does not exist, we create the current section
            blockIds = bytearray(4096)
            blockDatas = bytearray(2048)
            #As the official client, we create the AddBlock only if necessary
            blockAddBlocks = None
            if (block.getId() >> 8) != 0:
                blockAddBlocks = bytearray(2048)
            self.addSectionToCollection(posY, blockIds, blockDatas, blockAddBlocks)
            
        #Then we modify the values
        #AddBlock
        blockAddBlock = block.getId() >> 8
        if not blockAddBlocks is None:
            if pos & 1:
                blockAddBlocks[pos >> 1] = ( blockAddBlock << 4 ) + ((blockAddBlocks[pos >> 1]) & 0x0F)
            else:
                blockAddBlocks[pos >> 1] = ((blockAddBlocks[pos >> 1]) & 0xF0) + blockAddBlock
        blockIds[pos] = block.getId()
        
        blockData = block.getData()
        if pos & 1:
            blockDatas[pos >> 1] = ( blockData << 4 ) + ((blockDatas[pos >> 1]) & 0x0F)
        else:
            blockDatas[pos >> 1] = ((blockDatas[pos >> 1]) & 0xF0) + blockData
        return
        
    def removeBlock(self,x,y,z):
        AIR_BLOCK = MCImportBlock()
        AIR_BLOCK.setId(0)
        AIR_BLOCK.setData(0)
        self.setBlock(x, y, z, AIR_BLOCK)
        return
    
    def getBlock(self,x,y,z):
        pos = (y & 0x0F) + (z << 4 ) + (x << 8)
        posY = y >> 4
        
        #On teste si la section existe
        blockIds = self.blockIds.get(posY)
        blockDatas = self.blockDatas.get(posY)
        blockAddBlocks = self.blockAddBlocks.get(posY)
        if blockIds is None:
            block = MCImportBlock()
            block.setId(0)
            return block
        
        #On recupere les information du block
        blockAddBlock = 0
        if not blockAddBlocks is None:
            if pos & 1:
                blockAddBlock = (blockAddBlocks[pos >> 1] >> 4) & 0x0F
            else:
                blockData = (blockAddBlocks[pos >> 1]) & 0x0F
        
        blockId = blockIds[pos] + (blockAddBlock << 8)
        
        blockData = 0
        if pos & 1:
            blockData = (blockDatas[pos >> 1] >> 4) & 0x0F
        else:
            blockData = (blockDatas[pos >> 1]) & 0x0F
        
        #On genere le bloc
        block = MCImportBlock()
        block.setId(blockId)
        block.setData(blockData)
        return block