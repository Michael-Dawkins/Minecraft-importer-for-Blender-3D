class MCImportAnvilSection(object):
    
    sectionTagCompound = None
    sectionY = 0
    
    def __init__(self):
        return
    
    def importSectionData(self,sectionTagCompound):
        if not sectionTagCompound.containsTagWithName("Blocks") or not sectionTagCompound.containsTagWithName("Y"):
            return False
        self.sectionY = sectionTagCompound.getTagByName("Y")[0].getValue()
        self.chunkTagCompound = sectionTagCompound
        return True
        
    def setY(self,y):
        self.sectionY = y
        
    def getY(self):
        return self.sectionY
    
    def getBlockAddBlocks(self):
        if self.chunkTagCompound is None:
            return None
        if not self.chunkTagCompound.containsTagWithName("AddBlocks"):
            return None
        return self.chunkTagCompound.getTagByName("AddBlocks")[0]
    
    def getBlockIds(self):
        if self.chunkTagCompound is None:
            return None
        if not self.chunkTagCompound.containsTagWithName("Blocks"):
            return None
        return self.chunkTagCompound.getTagByName("Blocks")[0]
    
    def getBlockDatas(self):
        if self.chunkTagCompound is None:
            return None
        if not self.chunkTagCompound.containsTagWithName("Data"):
            return None
        return self.chunkTagCompound.getTagByName("Data")[0]
    
    
