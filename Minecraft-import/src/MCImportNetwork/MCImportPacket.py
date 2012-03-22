PACKET_KEEP_ALIVE=0
PACKET_LOGIN=0x01
PACKET_HANDSHAKE=0x02
PACKET_PING = 0xFE
PACKET_KICK = 0xFF

class MCImportPacket(object):

    packetType = 0

    def __init__(self,packetId):
        self.packetType = packetId
        return
    
    def getPacketType(self):
        return self.packetType
    
    @staticmethod
    def instanciatePacket(packetType):
        packet = None
        if packetType == PACKET_HANDSHAKE:
            packet = MCImportHandshake()
        if packetType == PACKET_KICK :
            packet = MCImportKick()
        else:
            raise Exception("Unsupported packet type : " + str(packetType))
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
        unused = self.readByte()
        self.maxPlayers = self.readByte()
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
        if result == "+":
            self.__needAuthentification = False
        else:
            self.__needAuthentification = True
            self.__serverHash = result
        return False
    
    def writeContentOnObjectStream(self,os):
        os.writeString(self.__username + ";" + self.__host)
        return True
    
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
    
    