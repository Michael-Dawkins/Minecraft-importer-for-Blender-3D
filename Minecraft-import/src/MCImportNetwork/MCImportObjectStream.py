from socket import socket
from struct import pack, unpack

class MCImportObjectStream(object):
    
    currentSocket = None
    
    def __init__(self,sock):
        self.currentSocket = sock
        
    def readByte(self):
        value = self.currentSocket.recv(1);
        return unpack("!B", value)[0]
    
    def readShort(self):
        value = self.currentSocket.recv(2);
        return unpack("!h", value)[0]
    
    def readInt(self):
        value = self.currentSocket.recv(4);
        return unpack("!i", value)[0]
    
    def readString(self):
        value = self.currentSocket.recv(2);
        sLength = unpack("!h", value)[0]
        if sLength == 0:
            return ""
        value = self.currentSocket.recv(sLength * 2)
        return str(value,"utf-16be")
    
    def writeByte(self,value):
        fValue = pack("!B",value)
        self.currentSocket.send(fValue)
        return True
    
    def writeShort(self,value):
        fValue = pack("!h",value)
        self.currentSocket.send(fValue)
        return True
    
    def writeInt(self,value):
        fValue = pack("!i",value)
        self.currentSocket.send(fValue)
        return True
    
    def writeString(self,value):
        fValue = pack("!hs",len(value),value)
        self.currentSocket.send(fValue)
        return True