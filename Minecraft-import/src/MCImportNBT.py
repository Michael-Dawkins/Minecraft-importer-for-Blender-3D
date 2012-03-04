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
TAG_INTEGER_ARRAY = 11

## Classe de base de tout objet NBT
class MCImportNBTTag(object):
    ##Nom de cette partie de la structure
    tagName = ""
    ##Donnees contenues par le tag
    tagData = None
    ##Type du tag
    tagType = 0
    ##Un Tag unamed est un tag qui ne contient que sa partie data, on connait deja son type
    ##Et il ne possede pas de nom. Basiquement les tags contenues dans les listes.
    ##Autre exemple, le nom du tag peut etre considerer comme un TAG_String unamed
    #@attention Ne pas utiliser ni modifier ce champs
    _tagUnnamed = False
    ##Taille des donnees du tag 
    #@attention Ce champ est utilise par les algorithmes de calcul et ne peux etre exploite tel quel.
    tagSize = 0
    
    ##Initialise un Tag de type TAG_END
    def __init__(self,name):
        self.tagName = name
        self.tagSize = 0
        return
    
    ##Construit un nouveau tag unamed a partie d'une sequence de bytes
    #@param self Pointeur vers l'instance
    #@param type Type du tag
    #@param nextS Sequence de bytes composant le tag
    def buildUnamedfromBytes(self,type,nextS):
        elt = None
        if (type == 0):
            elt = MCImportNBTTag("") #Il s'agit en fait d'un tag end
        elif (type == 1):
            elt = MCImportNBTTagByte()
        elif (type == 2):
            elt = MCImportNBTTagShort()
        elif (type == 3):
            elt = MCImportNBTTagInt()
        elif (type == 4):
            elt = MCImportNBTTagLong()
        elif (type == 5):
            elt = MCImportNBTTagFloat()
        elif (type == 6):
            elt = MCImportNBTTagDouble()
        elif (type == 7):
            elt = MCImportNBTTagByteArray()
        elif (type == 8):
            elt = MCImportNBTTagString()
        elif (type == 9):
            elt = MCImportNBTTagList()
        elif (type == 10):
            elt = MCImportNBTTagCompound()
        elif nextS[0] == 11:
            elt = MCImportNBTTagIntegerArray()
        else:
            raise ValueError("Element inconnu de type " + str(type) )
        if (elt is None):
            return None
        #On le declare en temps que tag unamed
        elt._tagUnnamed = True
        elt.fromBytes(nextS)
        return elt
    
    ##Construit un nouveau tag a partir d'une sequence de bytes
    #@param self Pointeur vers la classe
    #@param nextS Sequence de byte pour construire le tag  
    def buildfromBytes(self,nextS):
        elt = None
        if (nextS[0] == 0):
            elt = MCImportNBTTag("") #Il s'agit en fait d'un tag end
        elif (nextS[0] == 1):
            elt = MCImportNBTTagByte()
        elif (nextS[0] == 2):
            elt = MCImportNBTTagShort()
        elif (nextS[0] == 3):
            elt = MCImportNBTTagInt()
        elif (nextS[0] == 4):
            elt = MCImportNBTTagLong()
        elif (nextS[0] == 5):
            elt = MCImportNBTTagFloat()
        elif (nextS[0] == 6):
            elt = MCImportNBTTagDouble()
        elif (nextS[0] == 7):
            elt = MCImportNBTTagByteArray()
        elif (nextS[0] == 8):
            elt = MCImportNBTTagString()
        elif (nextS[0] == 9):
            elt = MCImportNBTTagList()
        elif (nextS[0] == 10):
            elt = MCImportNBTTagCompound()
        elif nextS[0] == 11:
            elt = MCImportNBTTagIntegerArray()
        else:
            raise ValueError("Element inconnu de type " + str(nextS[0]) )
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
        #Si il s'agit d'un tag end
        if self.isEndTag():
            return ["",s[1:]]
        #Si il s'agit d'un tag unnamed, on ne fait pas de traitement
        if self._tagUnnamed:
            return ["",s]
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
    
    ##Recupere le nom du tag, si il s'agit d'un tag nommee
    #@param self Pointeur vers l'instance
    def getName(self):
        return self.tagName
    
    ##Recupere la taille en octet du tag
    #@param self Pointeur vers l'instance
    #@attention Utilise cette fonction plutot que d'essayer d'obtenir le resultat par l'acces a tagSize 
    def getTagSize(self):
        if self.isEndTag():
            return 1;
        if not self._tagUnnamed:
            initial = 3 + len(self.tagName) + self.tagSize
        else:
            initial = self.tagSize
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
        self.tagData = struct.unpack_from(">b", i, 0)[0]
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
    
class MCImportNBTTagFloat(MCImportNBTTag):
    def __init__(self):
        MCImportNBTTag.__init__(self, "")
        self.tagType = 5
        self.tagSize = 4
        return
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if(i == 0):
            return None
        self.tagData = struct.unpack_from(">f", i, 0)[0]
        return [self.tagName,""]
    
    def toBytes(self):
        return self.toBytes() + struct.pack(">f", self.tagData)
    
class MCImportNBTTagDouble(MCImportNBTTag):
    def __init__(self):
        MCImportNBTTag.__init__(self, "")
        self.tagType = 6
        self.tagSize = 8
        return
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if(i == 0):
            return None
        self.tagData = struct.unpack_from(">d", i, 0)[0]
        return [self.tagName,""]
    
    def toBytes(self):
        return self.toBytes() + struct.pack(">d", self.tagData)
    
class MCImportNBTTagString(MCImportNBTTag):
    def __init__(self):
        MCImportNBTTag.__init__(self, "")
        self.tagType = 8
        self.tagSize = 2
        return
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if(i == 0):
            return None
        stringLength = struct.unpack_from(">h", i, 0)[0]
        self.tagSize = 2 + stringLength
        self.tagData = str( s[5 + len(self.tagName):stringLength + 5 + len(self.tagName)] );
        return [self.tagName,""]
    
    def toBytes(self):
        return self.toBytes() + struct.pack(">h", self.tagData) + self.tagData
    
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
        self.tagData = []
        return
    
    def __len__(self):
        return self.tagDataLength
    
    def getContentTagId(self):
        return self.tagDataId
    
    def get(self,i):
        if self.tagData is None or len(self.tagData) <= i:
            return None
        return self.tagData[i]
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if (i is None):
            return None
        ds = struct.unpack_from(">bi", i, 0)
        self.tagDataId = ds[0]
        self.tagDataLength = ds[1]
        self.tagSize = 5
        
        nextByteRead = 3 + len(self.tagName) + 5
        for i in range(0,self.tagDataLength):
            #Un TAG_List contient des unnamed Tags
            elt = self.buildUnamedfromBytes(self.tagDataId,s[nextByteRead:])
            if (elt is None):
                break
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
    
    def __len__(self):
        return len(self.tagData)
    
    def getTagCount(self):
        return len(self.tagData)
    
    def getTagByName(self,name):
        result = []
        for i in range(0, len(self.tagData)):
            if (self.tagData[i].tagName == name):
                result.append(self.tagData[i])
        return result
    
    def getTagByType(self,type):
        result = []
        for i in range(0, len(self.tagData)):
            if (self.tagData[i].tagType == type):
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
        nextByteRead = 0
        while mustRead:
            elt = self.buildfromBytes(i[nextByteRead:])
            if (elt is None or elt.isEndTag() ):
                mustRead = False
            else:
                self.tagSize += elt.getTagSize()
                nextByteRead = nextByteRead + elt.getTagSize()
                self.tagData.append(elt)
        self.tagSize += 1 #On n'oublie pas de compter le byte de TAG_End
        return [self.tagName,""]

class MCImportNBTTagIntegerArray(MCImportNBTTag):
    def __init__(self):
        MCImportNBTTag.__init__(self,"")
        self.tagType = 11
        self.tagSize = 4
        return
    
    def fromBytes(self,s):
        i = MCImportNBTTag.fromBytes(self, s)[1]
        if(i is None):
            return None
        length = struct.unpack_from(">l", i, 0)[0]
        self.tagData = []
        nextByte = 0
        for j in range(0,length):
            self.tagData.append(struct.unpack_from(">i",i,nextByte))
            nextByte += 4
        self.tagSize = 4 + length * 4
        return [self.tagName,""]
    
    def toBytes(self):
        raise NotImplementedError("Not Implemented")
