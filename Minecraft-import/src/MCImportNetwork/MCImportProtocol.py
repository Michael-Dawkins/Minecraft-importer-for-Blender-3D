#On utilise un design pattern qui separe l'implementation de l'objet MCImportServer
#L'objet server n'est donc plus dependant de l'implementation du protocole et on peut
#changer le protocole en cour de route
from MCImportEntity import Player
from MCImportNetwork.MCImportPacket import *

NOP = 0
AUTHENTICATE_USER = 1
SPAWNING_PLAYER = 2


class MCImportProtocol28(object):
    
    def __init__(self, server):
        self.__protocolVersion = 28
        self.__player = Player()
        self.__server = server
        self.__isConnected = False
        self.__isAuthenticated = False
        self.__currentOp = NOP
        return
    
    ##All this part is about the current Minecraft user
    
    def setUsername(self,un):
        self.__username = un
        
    def setPassword(self,pwd):
        self.__password = pwd
        
    def getPlayer(self):
        return self.__player
        
    ##When we received this 
    def processPacket(self, packet):
        if self.__currentOp == AUTHENTICATE_USER:
            self.__processPacketInAuthentication(packet)
        else: #TODO
            return
        return
    
    def __processPacketInAuthentication(self, packet):
        if packet.getPacketType() == PACKET_HANDSHAKE:
            if not packet.needAuthentification():
                self.__isConnected = True
                #Send player packet
                self.__sendPlayer()
            else:
                raise Exception("Unsupported operation : Cannot login on official server for now")
        elif packet.getPacketType() == PACKET_LOGIN:
            #Got some information about the current World : TODO store this information
            self.__isAuthenticated = True
            #Send a spawn query
        elif packet.getPacketType() == PACKET_KICK:
            self.__isConnected = False
            self.__isAuthenticated = False
        else:
            raise Exception("Unsupported packet type received during authentification : " + str(packet.getPacketType()))
        
    
    ##All this part is about the authentication process
    
    def authenticate(self):
        self.__currentOp = AUTHENTICATE_USER
        return self.__sendHandshake()
    
    def __sendHandshake(self):
        handPacket = MCImportHandshake()
        handPacket.setUsername(self.__player.getName())
        handPacket.setHost(self.__server.getServerIp(), self.__server.getServerPort())
        return self.__server._send(handPacket)
    
    def __sendLogin(self,User):
        if not self.__isConnected or self.__server is None:
            return False
        loginPacket = MCImportLogin()
        loginPacket.setUsername(self.__player.getName())
        loginPacket.setProtocolVersion(self.__protocolVersion)
        return self.__server._send(loginPacket)
