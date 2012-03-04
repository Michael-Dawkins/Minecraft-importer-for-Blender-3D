from MCImportBlocks.MCImportBlock import MCImportBlock


class MCImportBlockAnvilCollection(object):

    blockAddBlocks = None
    blockIds = None
    blockDatas = None

    def __init__(self):
        self.blockAddBlocks = dict()
        self.blockIds = dict()
        self.blockDatas = dict()
        return
    
    def addSectionToCollection(self,y,blockIds,blockDatas,blockAddBlocks):
        if y > 15:
            return;
        self.blockIds[y] = blockIds
        self.blockDatas[y] = blockDatas
        self.blockAddBlocks[y] = blockAddBlocks
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
        if blockAddBlocks is None:
            blockId = blockIds[pos]
        else:
            blockId = blockIds[pos] + blockAddBlocks[pos] << 8
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