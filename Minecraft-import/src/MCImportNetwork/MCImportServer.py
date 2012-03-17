import socket
from MCImportNetwork.MCImportObjectStream import MCImportObjectStream
from MCImportNetwork.MCImportPacket import *
from threading import Thread,Lock

SERVER_STATUS_NOT_CONNECTED = 0
SERVER_STATUS_HANDSHAKE = 1
SERVER_STATUS_MOJANG_LOGIN = 2
SERVER_STATUS_CAN_LOGIN = 3
SERVER_STATUS_CONNECTED = 4

PACKET_PRIORITY_HIGHT = 0
PACKET_PRIORITY_STANDART = 1

class MCImportPacketStack(object):
    #List containing received Packets from the server that can be handled with no time restriction
    receivedPacketPriorityStandart = None
    #List of packets to handle before all the other
    receivedPacketPriorityHight = None
    
    lockPriorityStandart = None
    lockPriorityHight = None
    
    def __init__(self):
        self.lockPriorityStandart = Lock()
        self.lockPriorityHight = Lock()
        self.receivedPacketPriorityHight = list()
        self.receivedPacketPriorityHight = list()
        return
    
    def pop(self):
        oResult = None
        if len(self.receivedPacketPriorityHight) != 0:
            self.lockPriorityHight.acquire()
            oResult = self.receivedPacketPriorityHight.pop()
            self.lockPriorityHight.release()
        else:
            self.lockPriorityStandart.acquire()
            oResult = self.receivedPacketPriorityStandart.pop()
            self.lockPriorityStandart.release()
        return oResult
    
    def push(self,obj,priority=PACKET_PRIORITY_STANDART):
        if priority == 0:
            self.lockPriorityHight.acquire()
            self.receivedPacketPriorityHight.append(obj)
            self.lockPriorityHight.release()
        else:
            self.lockPriorityStandart.acquire()
            self.receivedPacketPriorityStandart.append(obj)
            self.lockPriorityStandart.release()

class MCImportListenningProcess(Thread):
    packetStack = None
    serverSocket = None
        
    def __init__(self,serverSocket,packetStack):
        Thread.__init__()
        self.packetStack = packetStack
        self.serverSocket = serverSocket
        
    def run(self):
        if self.packetStack is None or self.serverSocket is None:
            raise Exception("The socket or the stack must be initialized before starting using this thread")
        try:
            os = MCImportObjectStream(self.serverSocket)
            packet = MCImportPacket.readFromObjectStream(os)
            #TODO
            print(packet.getPacketType())
        except socket.error as io:
            print(io) #debug
            return
        return
    

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
    
    
    def __init__(self, serverIp, serverPort):
        self.serverIpAddress = serverIp
        self.serverPort = serverPort
        return
    
    def setLogin(self,username,password):
        return
    
    #Start all the procedure to connect to this server
    def start(self):
        
        #Connect to the minecraft server
        if not self._connectToIPV4(self.serverIpAddress,self.serverPort):
            return False
        
        #Start the listenning thread
        self.serverListenningThread = Thread(target=self)
        self.serverListenningThread.start()
        
        #DEBUG: Test
        try:
            #Send a ping querry
            pingPacket = MCImportPing()
            os = MCImportObjectStream(self.serverSocket)
            pingPacket.writeOnObjectStream(os)
        except socket.error as se:
            return None
        
        #Start the worker thread
        self.serverListenningThread = Thread(target=self)
        self.serverListenningThread.start()
        
        return
    
    def ping(self):
        
        if self._connectToIPV4(self.serverIpAddress, self.serverPort) == False :
            return None
        pingPacket = MCImportPing()
        message = ""
        
        try:
            #Send a ping querry
            os = MCImportObjectStream(self.serverSocket)
            pingPacket.writeOnObjectStream(os)
            
            #And wait the kick
            kickPacket = MCImportPacket.readFromObjectStream(os)
            message = kickPacket.getMessage()
        except socket.error as se:
            return None
        
        if message is None:
            return None
        
        infos = message.split( b'\x00\xa7'.decode('utf_16be') )
        self.serverName = infos[0]
        self.serverCurrentNmtPlayer = int(infos[1])
        self.serverMaxPlayer = int(infos[2])
        
        self._close()
        return self.serverName
    
    #Fonction pour obtenir des infos sur le serveur
        
    #Fonctions pour le controle de la connexion
    
    def _close(self):
        if not self.serverSocket is None:
            return
        try:
            self.serverSocket.close()
        except socket.error as se:
            print(se) #Debug
            return
    
    def _connectToIPV6(self, serverIp, serverPort):
        return False
    
    def _connectToIPV4(self, serverIp, serverPort):
        af = socket.AF_INET
        
        #Si on n'as pas une ip, on essaye de recuperer une ip
        try:
            self.serverIpAddress = socket.gethostbyname(self.serverIpAddress)
        except socket.error as se:
            print(se) #TODO debug
            return False
        
        #On creer le socket pour communiquer avec le serveur
        self.serverSocket = socket.socket(af,socket.SOCK_STREAM,0)
        #On bind notre socket avec un port quelconque sur notre machine
        self.serverSocket.bind(("0.0.0.0", 0))
        #Puis on fait une tentative de connexion
        try:
            self.serverSocket.connect((self.serverIpAddress,self.serverPort))
        except socket.error as se:
            print(se) #TODO debug
            return False
        return True
        
    
    
    
    