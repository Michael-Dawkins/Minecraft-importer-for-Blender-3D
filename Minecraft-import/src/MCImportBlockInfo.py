from xml.dom import *
from xml.dom.minidom import parse
import re
import struct

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
    __blockFace = None
    __blockDefaultFace = UNDEFINED_FACE_ID
    
    def __init__(self, btype):
        self.__blockType = btype
        self.__blockFace = [UNDEFINED_FACE_ID] * 6
        self.__blockDefaultFace = UNDEFINED_FACE_ID
        return
    
    @staticmethod
    def copy(typedBlock):
        copiedTBlock = MCImportTypedBlockInfo(typedBlock.__blockType)
        copiedTBlock.__blockDefaultFace = typedBlock.__blockDefaultFace
        copiedTBlock.__blockTypeName = typedBlock.__blockTypeName
        copiedTBlock.__blockFace = bytearray(6)
        for i in range(6):
            copiedTBlock.__blockFace[i] = copiedTBlock.__blockFace[i]
    
    def __getitem__(self, key):
        if(key < 0 or key > 15):
            return None
        if(self.__blockFace[key] != UNDEFINED_FACE_ID):
            return self.__blockFace[key]
        else:
            return self.__blockDefaultFace
        
    def __setitem__(self, key, value):
        if(key < 0 or key > 15):
            return
        self.__blockFace[key] = value
        
    def setFaceId(self,key,value):
        self[key] = value
        
    def getFaceId(self,key):
        return self[key]
        
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
        MCImportTypedBlockInfo.__init__(self, DEFAULT_TYPE)
        self.__blockName = blockName
        self.__blockId = id
        return
    
    def setInstanciatedClass(self,className):
        classId = bytearray(4)
        rangeMax = 4
        if len(className) < 4:
            rangeMax = len(className)
        try:
            for i in range(rangeMax):
                classId[i] = ord(className[i])
            self.__blockClass = struct.unpack(">i", classId)[0]
        except:
            return        
    
    def setInstanciatedClassId(self,classId):
        self.__blockClass = classId
        
    def getInstanciatedClassId(self):
        return self.__blockClass
    
    def getBlockName(self):
        return self.__blockName
    
    def getBlockId(self):
        return self.__blockId
    
    def hasTypes(self):
        return not (self.__blockTypes is None)
    
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
            try:
                return self.__blockTypes[type]
            except:
                return None
    
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
        self.__blockTypes[ MCImportTypedBlockInfo.getType(self) ] = MCImportTypedBlockInfo.copy(self)
        
    def __getitem__(self, key):
        if not self.hasTypes():
            return MCImportTypedBlockInfo.__getitem__(self, key)
        else:
            return self.__blockTypes[key]
        
    def __str__(self):
        if not self.hasTypes():
            return "[ <%d>'%s'{%x} : %s ]" % ( self.__blockId, self.__blockName, self.__blockClass, MCImportTypedBlockInfo.__str__(self) )
        else:
            s = "[ <%d>'%s'{%x} : \n" % ( self.__blockId, self.__blockName, self.__blockClass)
            for b in self.__blockTypes:
                s += str(self.__blockTypes[b]) + "\n"
            return s + "]"

class MCImportBlockInfoCollection(object):
    
    __blocks = {}
    
    def __init__(self):
        return
    
    def __getitem__(self,key):
        return self.__blocks[key]
    
    def __setitem__(self,key,value):
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
        blocksElement = blockInfoCollection.getElementsByTagName("Blocks")[0]
        
        for node in blocksElement.childNodes:
            if node.nodeType != Node.ELEMENT_NODE:
                continue
            blockInfo = self.__parseBlockInfoFromNode(node)
            if not blockInfo is None:
                bic[blockInfo.getBlockId()] = blockInfo
        
        return bic
    
    def __parseBlockInfoFromNode(self,node):
        idAttribute = node.getAttribute("id")
        nameAttribute = node.getAttribute("name")
        classAttribute = node.getAttribute("class")
        
        if(idAttribute == "" or nameAttribute == ""):
            return None
        
        name = nameAttribute
        id = int(idAttribute)
        classId = None
        if classAttribute != "":
            classId = classAttribute
        else:
            classId = "Block"
            
        blockInfo = MCImportBlockInfo(name, id)
        blockInfo.setInstanciatedClass(classId)
        
        self.__parseTypedBlockInfoFromNodeList(blockInfo, node.childNodes)
        
        return blockInfo
    
    def __parseTypedBlockInfoFromNodeList(self ,bi, nodes ):
        
        for node in nodes:
            if node.nodeType != Node.ELEMENT_NODE:
                continue
            
            nameAttribute = node.getAttribute("name")
            typeAttribute = node.getAttribute("type")
            
            name = None
            type = 0
            if typeAttribute != "" :
                type = int(typeAttribute)
            if nameAttribute != "":
                name = nameAttribute
            
            tbi = bi.getType(type)
            if tbi is None:
                tbi = bi.createType(type)
            tbi.setName(name)
            
            self.__parseBlockInfoFacesFromNodeList(tbi, node.childNodes)
            
        return False
    
    def __parseBlockInfoFacesFromNodeList(self ,tbi, nodes):
        
        for node in nodes:
            if node.nodeType != Node.ELEMENT_NODE:
                continue
            if not re.match("^F[0-5]?$",node.tagName):
                continue
            if node.firstChild is None:
                continue
            
            if len(node.tagName) == 1:
                tbi.setDefaultFaceId(int(node.firstChild.data))
            else:
                face = int(node.tagName[1:])
                tbi.setFaceId(face,int(node.firstChild.data))
            
        return False
        
