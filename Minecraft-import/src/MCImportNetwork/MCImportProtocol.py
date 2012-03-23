#On utilise un design pattern qui separe l'implementation de l'objet MCImportServer
#L'objet server n'est donc plus dependant de l'implementation du protocole et on peut
#changer le protocole en cour de route
from MCImportEntity import Player,World
from MCImportNetwork.MCImportPacket import *

NOP = 0
AUTHENTICATE_USER = 1
IN_GAME = 2


class MCImportProtocol28(object):
    
    verbose = True
    
    def __init__(self, server):
        self.__protocolVersion = 28
        self.__player = Player()
        self.__world = World()
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
    
    def getWorld(self):
        return self.__world
        
    ##When we received a packet from the server, we process it with this function
    def processPacket(self, packet):
        if self.__currentOp == AUTHENTICATE_USER:
            self.__processPacketInAuthentication(packet)
        else:
            self.__processPacketInGame(packet)
        return
    
    _processesInGame = None
    @staticmethod
    def _initProcessesInGame():
        MCImportProtocol28._processesInGame = {
           PACKET_TIME_UPDATE:MCImportProtocol28.__processTimeUpdate,
           PACKET_SPAWN:MCImportProtocol28.__processSpawn
        }
    
    def __processPacketInGame(self,packet):
        if MCImportProtocol28._processesInGame is None:
            MCImportProtocol28._initProcessesInGame()
        try:
            MCImportProtocol28._processesInGame[packet.getPacketType()](self, packet)
        except:
            raise Exception("Unsupported packet type received (Type : %x)" % packet.getPacketType())
        return
    
    #Processus concerning all Minecraft Packets in game
    
    def __processTimeUpdate(self, packet):
        if MCImportProtocol28.verbose:
            print("Time world updated to %ld" % packet.getTime())
        self.__world.setTime(packet.getTime())
    
    def __processSpawn(self,packet):
        if MCImportProtocol28.verbose:
            print("Player spawned at : " + str(packet.getPosition()))
        self.__player.setPosition(packet.getPosition())
    
    #Processus concering the authentification to a Minecraft server
    
    def __processPacketInAuthentication(self, packet):
        if packet.getPacketType() == PACKET_HANDSHAKE:
            if not packet.needAuthentification():
                self.__isConnected = True
                #Send player packet
                self.__sendLogin()
            else:
                #TODO support official server authentification
                raise Exception("Unsupported operation : Cannot login on official server for now")
        elif packet.getPacketType() == PACKET_LOGIN:
            #Got some information about the current World : TODO store this information
            if MCImportProtocol28.verbose:
                print("Player %s logged in" % (self.__player.getName()))
            self.__isAuthenticated = True
            self.__currentOp = IN_GAME
        elif packet.getPacketType() == PACKET_KICK:
            if MCImportProtocol28.verbose:
                print(packet.getMessage())
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
    
    def __sendLogin(self):
        if not self.__isConnected or self.__server is None:
            return False
        loginPacket = MCImportLogin()
        loginPacket.setUsername(self.__player.getName())
        loginPacket.setProtocolVersion(self.__protocolVersion)
        return self.__server._send(loginPacket)
