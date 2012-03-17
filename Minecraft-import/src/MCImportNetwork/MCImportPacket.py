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
    
class MCImportHandshake(MCImportPacket):
    
    needAuthentification = False
    connectionHash = ""
    username = ""
    host = ""
    
    def __init__(self):
        MCImportPacket.__init__(self,PACKET_HANDSHAKE)
        return
    
    def setUsername(self, us):
        self.username = us
        
    def setHost(self,serverIp,serverPort):
        self.host = serverIp + ":" + serverPort
    
    def readContentFromObjectStream(self,os):
        result = os.readString()
        if result == "+":
            self.needAuthentification = False
        else:
            self.needAuthentification = True
            self.connectionHash = result
        return False
    
    def writeContentOnObjectStream(self,os):
        os.writeString(self.username + ";" + self.host)
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
    
    