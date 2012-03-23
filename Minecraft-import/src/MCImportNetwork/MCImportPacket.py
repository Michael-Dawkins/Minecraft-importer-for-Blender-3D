PACKET_KEEP_ALIVE=0
PACKET_LOGIN=0x01
PACKET_HANDSHAKE=0x02
PACKET_TIME_UPDATE = 0x04
PACKET_SPAWN=0X06
PACKET_SPAWN_MOB = 0x18
PACKET_PING = 0xFE
PACKET_KICK = 0xFF

class MCImportPacket(object):

    packetType = 0

    def __init__(self,packetId):
        self.packetType = packetId
        return
    
    def getPacketType(self):
        return self.packetType
    
    #Create a class variable to store the dictionary ( keep just one instance )
    packetTypes = None
    
    #Create a dictionary to have the same behavior as the switch instruction in other languaae
    @staticmethod
    def _init():
        MCImportPacket.packetTypes = {
        PACKET_LOGIN:MCImportLogin,
        PACKET_HANDSHAKE:MCImportHandshake,
        PACKET_LOGIN:MCImportLogin,
        PACKET_TIME_UPDATE:MCImportTimeUpdate,
        PACKET_SPAWN:MCImportSpawn,
        PACKET_SPAWN_MOB:MCImportSpawn,
        PACKET_KICK:MCImportKick
        }
    
    @staticmethod
    def instanciatePacket(packetType):
        if MCImportPacket.packetTypes is None:
            MCImportPacket._init()
        packet = None
        try:
            packet = MCImportPacket.packetTypes[packetType]()
        except:
            raise Exception("Unsupported packet type : %x" % (packetType))
        return packet
    
    @staticmethod
    def readFromObjectStream(os):
        packetType = os.readByte()
        packet = MCImportPacket.instanciatePacket(packetType)
        packet.readContentFromObjectStream(os)
        return packet
    
    def readContentFromObjectStream(self,os):
        return False
    
    def writeOnObjectStream(self,os):
        os.writeByte(self.packetType)
        return self.writeContentOnObjectStream(os)
    
    def writeContentOnObjectStream(self,os):
        return False
    
class MCImportLogin(MCImportPacket):
    
    def __init__(self):
        MCImportPacket.__init__(self,PACKET_LOGIN)
        return
    
    def setUsername(self,un):
        self.username = un
        
    def setProtocolVersion(self,pv):
        self.protocolVersion = pv
        
    def getPlayerEntityId(self):
        return self.playerEntityId
    
    def getLevelType(self):
        return self.levelType
    
    def getServerMode(self):
        return self.serverMode
    
    def getDimension(self):
        return self.dimension
    
    def getDifficulty(self):
        return self.difficulty
    
    def getMaxPlayers(self):
        return self.maxPlayers
    
    def readContentFromObjectStream(self,os):
        self.playerEntityId = os.readInt()
        unused = os.readString()
        self.levelType = os.readString()
        self.serverMode = os.readInt()
        self.dimension = os.readInt()
        self.difficulty = os.readByte()
        unused = os.readByte()
        self.maxPlayers = os.readByte()
        return False
    
    def writeContentOnObjectStream(self,os):
        os.writeInt(self.protocolVersion)
        os.writeString(self.username)
        os.writeString("")
        os.writeInt(0)
        os.writeInt(0)
        os.writeByte(0)
        os.writeByte(0)
        os.writeByte(0)
        return True  

class MCImportHandshake(MCImportPacket):
    def __init__(self):
        MCImportPacket.__init__(self,PACKET_HANDSHAKE)
        return
    
    def setUsername(self, us):
        self.__username = us
        
    def setHost(self,serverIp,serverPort):
        self.__host = serverIp + ":" + str(serverPort)
        
    def needAuthentification(self):
        return self.__needAuthentification
    
    def getServerHash(self):
        return self.__serverHash
    
    def readContentFromObjectStream(self,os):
        result = os.readString()
        if result[0] == '-':
            self.__needAuthentification = False
        else:
            self.__needAuthentification = True
            self.__serverHash = result
        return False
    
    def writeContentOnObjectStream(self,os):
        os.writeString(self.__username + ";" + self.__host)
        return True
    
class MCImportTimeUpdate(MCImportPacket):
    def __init__(self):
        MCImportPacket.__init__(self,PACKET_TIME_UPDATE)
        self.__time = 0
        return
    
    def getTime(self):
        return self.__time
    
    def readContentFromObjectStream(self,os):
        self.__time = os.readLong()
        return True
    
    def writeOnObjectStream(self,os):
        raise Exception("This packet is only server->client")
    
class MCImportSpawn(MCImportPacket):
    def __init__(self):
        MCImportPacket.__init__(self,PACKET_SPAWN)
        self.__x = 0
        self.__y = 0
        self.__z = 0
        return
    
    def getPosition(self):
        return (self.__x, self.__y, self.__z)
    
    def readContentFromObjectStream(self,os):
        self.__x = os.readInt()
        self.__y = os.readInt()
        self.__z = os.readInt()
    
    def writeOnObjectStream(self,os):
        raise Exception("This packet is only server->client")
    
class MCImportMobSpawn(MCImportPacket):
    def __init__(self):
        MCImportPacket.__init__(self,PACKET_SPAWN)
        self.__eid = 0
        self.__type = 0
        self.__x = 0
        self.__y = 0
        self.__z = 0
        self.__yaw = 0
        self.__pitch = 0
        self.__headYaw = 0
        self.__metadata = None
        return
    
    def readContentFromObjectStream(self,os):
        self.__x = os.readInt()
        self.__y = os.readInt()
        self.__z = os.readInt()
    
    def writeOnObjectStream(self,os):
        raise Exception("This packet is only server->client")
    
class MCImportPing(MCImportPacket):
    
    def __init__(self):
        MCImportPacket.__init__(self,PACKET_PING)
        return
    
    def readContentFromObjectStream(self,os):
        return False
    
    def writeOnObjectStream(self,os):
        os.writeByte(PACKET_PING)
        return False
    
class MCImportKick(MCImportPacket):

    kickMessage = ""

    def __init__(self):
        MCImportPacket.__init__(self, PACKET_KICK)
        return
    
    def readContentFromObjectStream(self,os):
        self.kickMessage = os.readString()
        return True
    
    def writeOnObjectStream(self,os):
        return False
    
    def getMessage(self):
        return self.kickMessage
    
    