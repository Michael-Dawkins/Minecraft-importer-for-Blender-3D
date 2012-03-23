import socket
import sys
from MCImportNetwork.MCImportObjectStream import MCImportObjectStream
from MCImportNetwork.MCImportPacket import *
from threading import Thread,Lock
from MCImportNetwork.MCImportProtocol import MCImportProtocol28

SERVER_STATUS_NOT_CONNECTED = 0
SERVER_STATUS_HANDSHAKE = 1
SERVER_STATUS_MOJANG_LOGIN = 2
SERVER_STATUS_CAN_LOGIN = 3
SERVER_STATUS_CONNECTED = 4

PACKET_PRIORITY_HIGHT = 0
PACKET_PRIORITY_STANDART = 1

class MCImportPacketStack(object):
    
    def __init__(self):
        self.__lock = Lock()
        self.__receivedPacketPriorityStandart = list()
        self.__receivedPacketPriorityHight = list()
        return
    
    def pop(self):
        oResult = None
        self.__lock.acquire()
        if len(self.__receivedPacketPriorityHight) != 0:
            oResult = self.__receivedPacketPriorityHight.pop(0)
        elif len(self.__receivedPacketPriorityStandart) != 0:
            oResult = self.__receivedPacketPriorityStandart.pop(0)
        self.__lock.release()
        return oResult
    
    def push(self,obj,priority=PACKET_PRIORITY_STANDART):
        self.__lock.acquire()
        if priority == 0:
            self.__receivedPacketPriorityHight.append(obj)
        else:
            self.__receivedPacketPriorityStandart.append(obj)
        self.__lock.release()

class MCImportWorkerProcess(Thread):
    
    debug = True
    
    def __init__(self,server,packetStack):
        Thread.__init__(self)
        self.__server = server
        self.__packetStack = packetStack
    
    def run(self):
        if self.__packetStack is None:
            raise Exception("The stack must be initialized before starting using this thread")
        
        #TODO
        while True:
            nextPacket = self.__packetStack.pop()
            if nextPacket is None:
                continue
            else:
                if MCImportWorkerProcess.debug:
                    print("@Worker : Processing packet ( type : %x )" % nextPacket.getPacketType())
                self.__server._getProtocol().processPacket(nextPacket)
        return

class MCImportListenningProcess(Thread):
        
    def __init__(self,server,packetStack):
        Thread.__init__(self)
        self.__packetStack = packetStack
        self.__server = server
        
    def run(self):
        if self.__packetStack is None or self.__server is None:
            raise Exception("The server and the stack must be initialized before starting using this thread")
        while True:
            packet = self.__server._recv()
            if packet is None:
                break
            print("@Listenning - Received : " + str(packet.getPacketType())) #DEBUG
            #Add the new packet in the stack
            self.__packetStack.push(packet)
            #TODO Take care of the priority


class MCImportServer(object):
    
    receivedChunk = None
    
    userLogin = "JeanKevin"
    userPassword = ""
    
    #Informations about the server
    serverIpAddress = "127.0.0.1"
    serverPort = 25565
    
    serverSocket = None
    serverSocketAddr = None
    
    serverKeepAlive = True #indique si le serveur doit essayer a tout pris de conserver la connexion
    serverIsInOnlineMode = False
    serverMaxPlayer = 0
    serverCurrentNmtPlayer = 0
    serverName = ""
    
    #Packet Stack and thread
    serverListenningThread = None
    serverWorkerThread = None
    serverConnection = None
    serverStatus = SERVER_STATUS_NOT_CONNECTED
    
    #List containing received Packets from the server that can be handled with no time restriction
    receivedPacketPriorityStandart = None
    #List of packets to handle before all the other
    receivedPacketPriorityHight = None
    
    
    def __init__(self, serverIp, serverPort = 25565):
        #Informations about the world
        
        
        #Information about the server
        self.__serverIpAddress = serverIp
        self.__serverPort = serverPort
        self.__serverSocket = None
        self.__serverStream = None
        self.__isConnected = False
        self.__protocol = None #Link to the current protocol implementation ( According the design pattern Implementation )
        return
    
    def setProtocolVersion(self, pv):
        if pv == 28:
            self.__protocol = MCImportProtocol28(self)
        else:
            raise Exception("Unsupported protocol version specified.")
        
    def _getProtocol(self):
        return self.__protocol
    
    def getUrl(self):
        return "%s:%d" % (self.__serverIpAddress, self.__serverPort)
    
    def getServerIp(self):
        return self.__serverIpAddress
    
    def getServerPort(self):
        return self.__serverPort
    
    def _send(self,packet):
        if self.__serverSocket is None or not self.__isConnected or self.__serverStream is None:
            return False
        try:
            packet.writeOnObjectStream(self.__serverStream)
            return True
        except Exception as ex:
            print("@Server : Sending socket closed ( error : %s )" % str(ex))
            self.__isConnected = False
            self._close()
            return False
        
    def _recv(self):
        if self.__serverSocket is None or not self.__isConnected or self.__serverStream is None:
            return None
        try:
            packet = MCImportPacket.readFromObjectStream(self.__serverStream)
            return packet
        except Exception as ex:
            print("@Server : Receiving socket closed ( error : %s )" % str(ex))
            self.__isConnected = False
            self._close()
            return None
    
    def isConnected(self):
        return self.__isConnected
    
    #Start all the procedure to connect to this server
    def start(self):
        #Verify that we have a specified version of the protocol to communicate with the server
        if self.__protocol is None:
            return False
        
        #Connect to the minecraft server
        if not self._connectToIPV4(self.serverIpAddress,self.serverPort):
            return False
        
        #Create the poll for the incoming packets
        self.serverPacketStack = MCImportPacketStack()
        
        #Start the listenning thread
        self.serverListenningProcess = MCImportListenningProcess(self, self.serverPacketStack)
        self.serverListenningProcess.start()
        
        #Start the worker thread
        self.serverWorkerProcess = MCImportWorkerProcess(self, self.serverPacketStack)
        self.serverWorkerProcess.start()
        
        #Launch the authentication process
        self.__protocol.authenticate()
        
        return
    
    def ping(self):
        if self._connectToIPV4(self.serverIpAddress, self.serverPort) == False :
            return None
        pingPacket = MCImportPing()
        
        if not self._send(pingPacket):
            return None
        
        kickPacket = self._recv()
        if kickPacket is None:
            return None
        
        message = kickPacket.getMessage()
        
        if message is None:
            return None
        
        infos = message.split( b'\x00\xa7'.decode('utf_16be') )
        self.serverName = infos[0]
        self.serverCurrentNmtPlayer = int(infos[1])
        self.serverMaxPlayer = int(infos[2])
        
        self._close()
        return self.serverName
    
    def _close(self):
        #If we are no more connected to the server, we clean all ressources used
        #Else we closed the socket then we clean all ressouces used
        try:
            self.__serverSocket.close()
        except Exception as ex:
            print("@Server : Close socket failed ( error : %d )" % str(ex))

        self.__serverSocket = None
        self.__serverStream = None
        self.__isConnected = False
            
    
    def _connectToIPV6(self, serverIp, serverPort):
        return False
    
    def _connectToIPV4(self, serverIp, serverPort):
        af = socket.AF_INET
        
        #Si on n'as pas une ip, on essaye de recuperer une ip
        try:
            self.__serverIpAddress = socket.gethostbyname(self.serverIpAddress)
        except socket.error as se:
            print(se) #TODO debug
            return False
        
        #On creer le socket pour communiquer avec le serveur
        self.__serverSocket = socket.socket(af,socket.SOCK_STREAM,0)
        #On bind notre socket avec un port quelconque sur notre machine
        self.__serverSocket.bind(("0.0.0.0", 0))
        #Puis on fait une tentative de connexion
        try:
            self.__serverSocket.connect((self.__serverIpAddress,self.__serverPort))
            self.__serverStream = MCImportObjectStream(self.__serverSocket)
            self.__isConnected = True
        except socket.error as se:
            print(se) #TODO debug
            return False
        return True
        
    
    
    
    