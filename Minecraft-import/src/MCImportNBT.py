'''
Created on 29 sept. 2011

@author: cyr62110
'''

import struct

##Voici une liste des differentes structures d un NBT
TAG_END = 0 #indique la fin d'une liste ou d'un dictionnaire
TAG_BYTE = 1
TAG_SHORT = 2
TAG_INT = 3
TAG_LONG = 4
TAG_FLOAT = 5
TAG_DOUBLE = 6
TAG_BYTE_ARRAY = 7
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10

## Classe de base de tout objet NBT
class MCImportNBTTag(object):
    ##Nom de cette partie de la structure
    tagName = ""
    ##Donnees contenues par le tag
    tagData = None
    ##Type du tag
    tagType = 0
    ##Taille des donnees du tag 
    #@attention Ce champ est utilise par les algorithmes de calcul et ne peux etre exploite tel quel.
    tagSize = 0
    
    ##Initialise un Tag de type TAG_END
    def __init__(self,name):
        self.tagName = name
        self.tagSize = 0
        return
    
    ##Construit un nouveau tag a partir d'une sequence de bytes
    #@param self Pointeur vers la classe
    #@param nextS Sequence de byte pour construire le tag  
    def buildfromBytes(self,nextS):
        elt = None
        if (nextS[0] == 0):
            elt = None
        elif (nextS[0] == 1):
            elt = MCImportNBTTagByte()
        elif (nextS[0] == 2):
            elt = MCImportNBTTagShort()
        elif (nextS[0] == 3):
            elt = MCImportNBTTagInt()
        elif (nextS[0] == 4):
            elt = MCImportNBTTagLong()
        elif (nextS[0] == 5):
            raise ValueError("Element inconnu de type 5")
        elif (nextS[0] == 6):
            raise ValueError("Element inconnu de type 6")
        elif (nextS[0] == 7):
            elt = MCImportNBTTagByteArray()
        elif (nextS[0] == 8):
            raise ValueError("Element inconnu de type 8")
        elif (nextS[0] == 9):
            elt = MCImportNBTTagList()
        elif (nextS[0] == 10):
            elt = MCImportNBTTagCompound()
        else:
            raise ValueError("Element inconnu de type " + nextS[0])
        if (elt is None):
            return None
        elt.fromBytes(nextS)
        return elt
    
    ##Teste si il s'agit d'un tag de fin de sequence
    def isEndTag(self):
        return self.tagType == 0
    
    ##Importe les informations depuis une sequence de bytes
    #@param self Pointeur vers la classe
    #@param s Sequence de bytes a partir de laquel on importe les info.  
    def fromBytes(self, s):
        #Si la chaine fait moins de 3 c., il ne s'agit pas d'un tag
        if(len(s) < 3 or s[0] != self.tagType):
            return None
        nameL = struct.unpack_from(">h",s,1)[0]
        if nameL == 0:
            self.tagName = ""
        else:
            self.tagName = s[3:3+nameL].decode("latin")
        return [self.tagName,s[3+nameL:]]
    
    ##Exporte le tag sous la forme d'une sequence de bytes
    #@param self Pointeur vers l'instance 
    def toBytes(self):
        return chr(self.tagType) + chr(len(self.tagName)) + self.tagName
    
    ##Recupere les donnees contenues dans le tag
    #@param self Pointeur vers l'instance 
    def getValue(self):
        return self.tagData
    
    ##Recupere la taille en octet du tag
    #@param self Pointeur vers l'instance
    #@attention Utilise cette fonction plutot que d'essayer d'obtenir le resultat par l'acces a tagSize 
    def getTagSize(self):
        initial = 3 + len(self.tagName) + self.tagSize
        return initial

class MCImportNBTTagByte(MCImportNBTTag):
    def __init__(self):
        MCImportNBTTag.__init__(self, "")
        self.tagType = 1
        self.tagSize = 1
        return
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self,s)[1]
        if(i is None):
            return None
        self.tagData = struct.unpack_from(">c", i, 0)[0]
        return [self.tagName, ""]
    
    def toBytes(self):
        return chr(self.tagType) + chr(self.tagData)
    
class MCImportNBTTagShort(MCImportNBTTag):
    def __init__(self):
        MCImportNBTTag.__init__(self, "")
        self.tagType = 2
        self.tagSize = 2
        return
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if(i is None):
            return None
        self.tagData = struct.unpack_from(">h", i, 0)[0]
        return [self.tagName,""]
    
    def toBytes(self):
        return self.toBytes() + struct.pack(">h", self.tagData)

class MCImportNBTTagInt(MCImportNBTTag):
    def __init__(self):
        MCImportNBTTag.__init__(self, "")
        self.tagType = 3
        self.tagSize = 4
        return
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if(i == 0):
            return None
        self.tagData = struct.unpack_from(">i", i, 0)[0]
        return [self.tagName,""]
    
    def toBytes(self):
        return self.toBytes() + struct.pack(">i", self.tagData) 
    
class MCImportNBTTagLong(MCImportNBTTag):
    def __init__(self):
        MCImportNBTTag.__init__(self, "")
        self.tagType = 4
        self.tagSize = 8
        return
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if(i == 0):
            return None
        self.tagData = struct.unpack_from(">q", i, 0)[0]
        return [self.tagName,""]
    
    def toBytes(self):
        return self.toBytes() + struct.pack(">q", self.tagData)
    
class MCImportNBTTagByteArray(MCImportNBTTag):
    def __init__(self):
        MCImportNBTTag.__init__(self,"")
        self.tagType = 7
        self.tagSize = 4
        return
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if(i is None):
            return None
        length = struct.unpack_from(">l", i, 0)[0]
        self.tagData = bytearray(length)
        for j in range(0,length):
            self.tagData[j] = i[j+4]
        self.tagSize = 4 + length
        return [self.tagName,""]
    
    def toBytes(self):
        l = len(self.tagData)
        lstring = chr((l >> 24)) | chr((l >> 16) | 0xFF ) | chr((l >> 8) | 0xFF) | chr( l | 0xFF)
        arraystring = ""
        for i in range(0, l):
            arraystring += self.tagData[i] 
        return self.toBytes() + lstring + arraystring

class MCImportNBTTagList(MCImportNBTTag):
    tagDataId = 0
    tagDataLength = 0
    
    def __init__(self):
        MCImportNBTTag.__init__(self,"")
        self.tagType = 9
        self.tagSize = 5
        return
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if (i is None):
            return None
        ds = struct.unpack_from(">ci", i, 0)
        self.tagDataId = ds[0]
        self.tagDataLength = ds[1]
        self.tagDataId = []
        self.tagSize = 5
        
        nextByteRead = 3 + len(self.tagName) + 5
        for i in range(0,self.tagDataLength):
            elt = self.buildfromBytes(s[nextByteRead:])
            if (elt is None):
                break
            elif (elt.tagType != self.tagDataId):
                raise ValueError("Liste de type " + self.tagDataId + " contenant un element de type " + elt.tagType)
            else:
                self.tagSize += elt.getTagSize()
                nextByteRead += elt.getTagSize()
                self.tagData.append(elt)
        return [self.tagName,""]
    
class MCImportNBTTagCompound(MCImportNBTTag):
    def __init__(self):
        MCImportNBTTag.__init__(self, "")
        self.tagType = 10
        self.tagSize = 0
        return
    
    def getTagCount(self):
        return len(self.tagData)
    
    def getTagByName(self,name):
        result = []
        for i in range(0, len(self.tagData)):
            if (self.tagData[i].tagName == name):
                result.append(self.tagData[i])
        return result
    
    def getTagByType(self,typ):
        result = []
        for i in range(0, len(self.tagData)):
            if (self.tagData[i].tagType == typ):
                result.append(self.tagData[i])
        return result
    
    def containsTagWithName(self,name):
        result = 0
        for i in range(0, len(self.tagData)):
            if(self.tagData[i].tagName == name):
                result += 1
        if(result == 0):
            return False
        else:
            return True
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if(i is None):
            return None
        ## On vide la liste
        self.tagData = []
        self.tagSize = 0
        mustRead = True
        nextByteRead = 3 + len(self.tagName)
        while mustRead:
            elt = self.buildfromBytes(s[nextByteRead:])
            if (elt is None):
                mustRead = False
            else:
                self.tagSize += elt.getTagSize()
                nextByteRead = nextByteRead + elt.getTagSize()
                self.tagData.append(elt)
        return [self.tagName,""]
        
        