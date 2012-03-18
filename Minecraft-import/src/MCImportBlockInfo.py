from xml.dom import *
from xml.dom.minidom import parse

UNDEFINED_FACE_ID = -1
STONE_FACE_ID = 1
DEFAULT_TYPE = 0
    
FACE_NORTH = 0
FACE_EAST = 1
FACE_SOUTH = 2
FACE_WEST = 3
FACE_TOP = 4
FACE_BOTTOM = 5

class MCImportTypedBlockInfo(object):
    
    __blockTypeName = None
    __blockType = 0
    __blockFace = [UNDEFINED_FACE_ID] * 6
    __blockDefaultFace = UNDEFINED_FACE_ID
    
    def __init__(self,type):
        self.__blockType = type
        return
    
    @staticmethod
    def copy(typedBlock):
        copiedTBlock = MCImportBlockInfo(typedBlock.__blockType)
        copiedTBlock.__blockDefaultFace = typedBlock.__blockDefaultFace
        copiedTBlock.__blockName = typedBlock.__blockName
        copiedTBlock.__blockFace = []
        copiedTBlock.__blockFace[:] = copiedTBlock.__blockFace[:]
    
    def __getitem__(self, key):
        if(key < 0 or key > 15):
            return None
        if(self.__blockFace[key] == UNDEFINED_FACE_ID):
            return self.__blockFace[key]
        else:
            return self.__blockDefaultFace
        
    def __setitem__(self, key, value):
        if(key < 0 or key > 15):
            return
        self.__blockFace[key] = value
        
    def setDefaultFaceId(self, faceId):
        self.__blockDefaultFace = faceId
        
    def getDefaultFaceId(self):
        return self.__blockDefaultFace
    
    def setName(self,name):
        self.__blockTypeName = name
        
    def getName(self):
        return self.__blockTypeName
    
    def getType(self):
        return self.__blockType
    
    def __str__(self):
        if(self.__blockTypeName == None):
            return "[ (%d) %d, %d, %d, %d, %d, %d ]" % (self.__blockType, self[0], self[1], self[2], \
                                                        self[3], self[4], self[5])
        else:
            return "[ (%d,'%s') %d, %d, %d, %d, %d, %d ]" % (self.__blockType, self.__blockTypeName,self[0], self[1], self[2], \
                                                        self[3], self[4], self[5])
        
    
class MCImportBlockInfo(MCImportTypedBlockInfo):
    
    __blockId = 0
    __blockClass = 0
    __blockName = None
    __blockTypes = None
    
    def __init__(self,blockName, id):
        self.__blockName = blockName
        self.__blockId = id
        return
    
    def getBlockName(self):
        return self.__blockName
    
    def getBlockId(self):
        return self.__blockId
    
    def hasTypes(self):
        return (self.__blockTypes is None)
    
    def getName(self,type):
        if(type == DEFAULT_TYPE and not self.hasTypes()):
            return self.getName()
        else:
            return self.__blockTypes[type].getName()
        
    def getType(self,type):
        if type < 0 or type > 15:
            return None
        if type == DEFAULT_TYPE and not self.hasTypes():
            return self
        elif not self.hasTypes():
            return None
        else:
            return self.__blockType[type]
    
    def createType(self,type):
        if type < 0 or type > 15:
            return
        if not self.hasTypes():
            self.__createTypeCollection()
        self.__blockTypes[type] = MCImportTypedBlockInfo(type)
        return self.__blockTypes[type]
    
    def __createTypeCollection(self):
        if self.__blockTypes is None:
            self.__blockTypes = {}
        self.__blockTypes[ self.__blockType ] = MCImportTypedBlockInfo.copy(self)
        
    def __getitem__(self, key):
        if not self.hasTypes():
            return MCImportTypedBlockInfo.__getitem__(self, key)
        else:
            return self.__blockTypes[key]
        
    def __str__(self):
        if not self.hasTypes():
            return "[ <%d>'%s'{%d} : %s ]" % ( self.__blockId, self.__blockName, self.__blockClass, MCImportTypedBlockInfo.__str__(self) )
        else:
            s = "[ <%d>'%s'{%d} : \n" % ( self.__blockId, self.__blockName, self.__blockClass)
            for b in self.__blockTypes:
                s += self.__blockTypes[b] + "\n"
            return s + "]"

class MCImportBlockInfoCollection(object):
    
    __blocks = {}
    
    def __init__(self):
        return
    
    def __getitem__(self,key):
        return self.__blocks[key]
    
    def __setitem(self,key,value):
        self.__blocks[key] = value
        
    def __iter__(self):
        return self.__blocks.__iter__()
    
class MCImportBlockInfoCollectionXMLReader(object):
    
    __file = None
    
    def __init__(self,file):
        self.__file = file
        
    def getBlockInfoCollection(self):
        
        blockInfoCollection = parse(self.__file)
        
        bic = MCImportBlockInfoCollection()
        blocksElement = bic.getElementsByTagName("Blocks")[0]
        
        for elt in blocksElement.childNodes:
            if blocksElement.childNodes[elt].nodeType != Node.ELEMENT_NODE:
                continue
            blockInfo = self.__parseBlockInfoFromNode(blocksElement.childNodes[elt])
            if not blockInfo is None:
                bic[blockInfo.getId()] = blockInfo
        
        return bic
    
    def __parseBlockInfoFromNode(self,node):
        attributes = node.attributes
        idAttribute = attributes.item("id")
        nameAttribute = attributes.item("name")
        classAttribute = attributes.item("class")
        
        if(idAttribute is None or nameAttribute is None):
            return None
        
        return None
        
