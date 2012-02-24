## @package MCImportBetaMap
# 

import zlib
import struct
import re
import MCImportNBT
import MCImportMatrix

## Representation d'un chunk.
# 
class MCImportBetaMapChunk(object):
    ##Contient un tableau de byte contenant les informations du chunk
    chunkDataStruct = None
    ##Structure NBT du chunk (TagCompound)
    chunkTagCompound = None
    
    ##Initialise les informations du chunk
    #@param self Pointeur vers la classe 
    def __init__(self):
        return
    
    ##Importe les donnees d'un chunk depuis un tableau de Byte
    #@param self Pointeur vers la classe
    #@param data Tableau contenant les informations  
    def importBetaChunkData(self, data):
        self.chunkDataStruct = data
        self.chunkTagCompound = MCImportNBT.MCImportNBTTagCompound()
        if (self.chunkTagCompound.fromBytes(data) == False):
            return False
        #Il s'agit d'un patch dans le cas ou Level n'est pas la racine de la structure
        if(self.chunkTagCompound.containsTagWithName("Level")):
            self.chunkTagCompound = self.chunkTagCompound.getTagByName("Level")[0]
        return True
    
    ##Recupere une matrice contenant les blocs
    #@param self Pointeur vers la classe
    def getBlocks(self):
        if(self.chunkTagCompound is None):
            return None
        blocks = self.chunkTagCompound.getTagByName("Blocks")
        if(blocks is None or len(blocks) == 0):
            return None
        block = blocks[0]
        matrix = MCImportMatrix.MCImportMatrix()
        if(matrix.importFromBytes(block.tagData) == False):
            return None
        return matrix
    
##Permet l'importation d'un fichier de region minecraft (.mcr)
class MCImportBetaMapFile(object):
    ##Indique si le stream est ouvert ou non
    isOpen = False
    ##Stream vers le fichier de region
    fileStream = None
    ##Chemin vers le fichier de region
    filePath = None
    
    def __init__(self):
        return
    
    ##Verifie si un nom de fichier est un nom de region valide
    #@param self Pointeur vers la classe
    #@param fileName Nom du fichier a tester  
    def isValidMCRegionFilename(self, fileName):
        pos = re.match('r\.[-0-9]*\.[-0-9]*\.mcr', fileName)
        if(type(pos).__name__ == 'NoneType'):
            return False
        return True
    
    ##Ouvre un fichier region minecraft
    #@param self Pointeur vers la classe
    #@param filePath Chemin vers le fichier de region .mcr  
    def openMCRegion(self, filePath):
        #On detecte le type de chemin utilise
        windows = True
        if (filePath.count("/") != 0):
            windows = False
        #Algo permettant de recuperer le nom du fichier dans le chemin
        fileName = filePath
        result = ['' , '' , filePath ]
        while( len(result[2]) != 0 ):
            fileName = result[2]
            if (windows):
                result = result[2].partition('\\')
            else:
                result = result[2].partition('/')
        
        #Verifie si le nom de fichier est un nom de region valide
        if(self.isValidMCRegionFilename(fileName) == False):
            return False 
        
        #Essaye d'ouvrir un stream vers le fichier
        try:
            if(self.isOpen == True):
                self.fileStream.close()
                self.fileStream = None
            self.fileStream = open(filePath, 'rb')
            self.isOpen = True
            return True
        except:
            self.isOpen = False
            return False
    
    ## Ferme le stream vers le fichier de la region
    #@param self Pointeur vers la classe 
    def closeMCRegion(self):
        if(self.isOpen == True):
            self.fileStream.close()
            return True
        else:
            return False
    
    ## Convertit la position du chunk en (x,z) en un offset dans la fichier.
    #L'axe Y represente une direction vers le ciel. Donc les positions des chunk sont en X,Z.
    #@param self Pointeur vers la classe
    #@param x Position du chunk en X
    #@param z Position du chunk en Z  
    def coordToOffset(self,x,z):
        if( x < 0 or z < 0 or x > 31 or z > 31):
            return [ -1 , -1]
        offset = [ 4 * ((x % 32) + (z % 32) * 32) , 0 ]
        offset[1] = offset[0] + 4096
        return offset
    
    ##Recupere les informations de l'header et les insere dans une structure
    #@param self Pointeur vers la classe
    #@param data Donnee de l'entete NBT
    def betaChunkDataToStruct(self,data):
        if(len(data) < 5):
            return None
        #[ taille des donnees du chunk, type de compression ]
        return [ (int(data[0]) << 24) + (int(data[1]) << 16) + (int(data[2]) << 8) + int(data[3]) - 1, data[4]]
    
    ##Transforme les donnees de l'entete du chunk en structure de Location
    #@param self Pointeur vers la classe
    #@param loc Donnee de la partie Location de l'entete  
    def locationToStruct(self, loc):
        if(len(loc) != 4):
            return None
        #La liste renvoyee est la suivant [ offset / 4096 , size / 4096 + 1 ]
        return [ (int(loc[0]) << 16) + (int(loc[1]) << 8) + int(loc[2]) , loc[3] ]
    
    ##Recupere un tableau de Byte contenant une structure NBT du chunk
    #@param self Pointeur vers la classe
    #@param x Position en X du chunk
    #@param z Position en Z du chunk
    def getChunk(self,x,z):
        if(self.isOpen == False):
            return None
        offset = self.coordToOffset(x, z)
        #On lit les information disponibles sur le trunk, comme sa taille et son offset dans le fichier
        self.fileStream.seek(offset[0])
        chunk_location = self.fileStream.read(4)
        chunk_loc_struct = self.locationToStruct(chunk_location)
        #Puis on recupere le timestamp du trunk
        self.fileStream.seek(offset[1])
        chunk_timestamp = self.fileStream.read(4)
        #Enfin si le trunk, n'existe pas
        if(chunk_loc_struct[1] == 0):
            return None
        #Sinon, on genere la structure a partir des donnees
        self.fileStream.seek(chunk_loc_struct[0] * 4096)
        chunk_data_info = self.fileStream.read(5)
        chunk_data_struct = self.betaChunkDataToStruct(chunk_data_info)
        if(chunk_data_struct is None or chunk_data_struct[1] != 2):
            return None
        cchunk_data = self.fileStream.read(chunk_data_struct[0])
        #On decompresse le chunk avec la zlib
        try:
            chunk_data = zlib.decompress(cchunk_data)
        except:
            return None
        #On genere le NBT a partir des donnees
        chunk = MCImportBetaMapChunk()
        #On charge a partir des donnees
        chunk.importBetaChunkData(chunk_data)
        return chunk

class MCImportBetaMap(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        return

    def supportedVersion(self):
        return [ (1.8), (1.9) ]
        