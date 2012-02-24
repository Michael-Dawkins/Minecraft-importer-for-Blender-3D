import socket
import threading
from struct import (pack_into)

VERSION_1_8 = 17
VERSION_1_9_PRE4 = 20

def toString16(buffer, offset, str):
    l = len(str)
    pack_into(">h", buffer, offset, l)
    for i in range(0,l):
        buffer[ offset + 2 + i*2 ] = 0
        buffer[ offset + 3 + i*2 ] = ord(str[i])
    return
    
class MCImportProtocol(object):    
    _proto_connection = None
    _proto_username = "JeanKevin"
    _proto_version = VERSION_1_8
    
    def __init__(self):
        return
    
    def setUserId(self,username):
        self._proto_username = username
        return
    
    def setVersion(self,version):
        #On limite l'utilisation sur les serveurs 1.8 et 1.9
        if(version > 16 and version < 21):
            self._proto_version = version
        else:
            self._proto_version = VERSION_1_8
        return self._proto_version
    
    def etablishCommunicationWith(self,serverAddr):
        #On coupe la communication precedente
        if not (self._proto_connection is None):
            self._proto_connection.shutdown()
        #Puis on tente de se connecter selon le protocole
        self._proto_connection = MCImportProtocolConnection()
        if not self._proto_connection.connectTo(serverAddr, False):
            return False
        
        #Enfin, on lance la procedure de connexion
        #On lance un handshake
        hand = MCImportProtocolHandshake()
        hand.setUserName(self._proto_username)
        self._proto_connection.send(hand)
        i = self._proto_connection.recv()
        print(i)
        login = MCImportProtocolLogin()
        login.setUserName(self._proto_username)
        login.setMCVersion(self._proto_version)
        self._proto_connection.send(login)
        i = self._proto_connection.recv()
        print(i)
        return True
    
    def tryConnectionWith(self,serverAddr):
        #On coupe la communication precedente
        if not (self._proto_connection is None):
            self._proto_connection.shutdown()
        #Puis on tente de se connecter selon le protocole
        self._proto_connection = MCImportProtocolConnection()
        if not self._proto_connection.connectTo(serverAddr, False):
            return False
        
        #Enfin, on lance la procedure de connexion
        #On lance un handshake
        ping = MCImportProtocolPing()
        self._proto_connection.send(ping)
        i = self._proto_connection.recv()
        print(i)
        return True

LOGIN_PACKET = 0x01
HANDSHAKE_PACKET = 0x02
PING_PACKET = 0xFE
KICK_PACKET = 0xFF
    
class MCImportProtocolPacket(object):
    
    _packet_id = 0
    _packet_data = None
    
    def __init__(self):
        return
    
    def build(self):
        return None
    
    def fromBytes(self,b):
        return False
    
class MCImportProtocolHandshake(MCImportProtocolPacket):
    _handshake_user = ""
    _handshake_return = ""
    
    def __init__(self):
        self._packet_id = 2
        return
    
    def build(self):
        if len(self._handshake_user) == 0:
            return None
        self._packet_data = bytearray(1 + 2 + len(self._handshake_user) * 2)
        self._packet_data[0] = self._packet_id
        toString16(self._packet_data, 1, self._handshake_user)
        return self._packet_data
    
    def fromBytes(self,b):
        if b is None or len(b) <= 1:
            return False
        if b[0] != self._packet_id:
            return False
        self._packet_data = b
        self._handshake_return = b[1:]
        return True
    
    def setUserName(self,user):
        self._handshake_user = user
        return   
    
    def serverNeedsAuthentification(self):
        if(len(self._handshake_return) == 0):
            return False
        if self._handshake_return[0] == "+":
            return True
        return False
    
class MCImportProtocolLogin(MCImportProtocolPacket):
    _login_username = ""
    _login_mcversion = VERSION_1_8
    
    def __init__(self):
        self._packet_id = 1
        return
    
    def build(self):
        if len(self._login_username) == 0:
            return None
        self._packet_data = bytearray(23 + len(self._login_username) * 2)
        self._packet_data[0] = self._packet_id
        pack_into(">i",self._packet_data,1,self._login_mcversion)
        toString16(self._packet_data,5,self._login_username)
        return self._packet_data
    
    def fromBytes(self,b):
        return False
    
    def setUserName(self,user):
        if(user is None or len(user) == 0):
            self._login_username = "JeanKevin"
        else:
            self._login_username = user
        return self._login_username
    
    def setMCVersion(self,v):
        if v > 16 and v < 21:
            self._login_mcversion = v
        else:
            self._login_mcversion = VERSION_1_8
        return self._login_mcversion
    
class MCImportProtocolPing(MCImportProtocolPacket):
    
    def __init__(self):
        self._packet_id = 0xFE
        
    def build(self):
        self._packet_data = bytearray(1)
        self._packet_data[0] = self._packet_id
        return self._packet_data
    
class MCImportProtocolKick(MCImportProtocolPacket):
    
    _kick_reason = ""
    
    def __init__(self):
        self._packet_id = 0xFF
        
    def fromBytes(self,b):
        if b is None or len(b) <= 1:
            return False
        if b[0] != self._packet_id:
            return False
        self._packet_data = b
        self._kick_reason = b[1:].decode("unicode_internal")
        return True
    
    def getReason(self):
        return self._kick_reason
    
class MCImportProtocolConnection(threading.Thread):
    _server_addr = ""
    _server_port = ""
    
    _server_socket = None
    _server_sockaddr = None
    _server_thread = False
    
    _connection_rcvbuffer = []
    _connection_sendbuffer = []
    
    _client_name = ""
    
    _last_error = ""
    
    def connectTo(self,server,useIPv6=False):
        _server_name = server
        
        if(useIPv6):
            return False #Pour le moment, l'ip v6 n'est pas pris en charge
        else:
            s = server.split(":")
            self._server_addr = s[0]
            self._server_port = int(s[1])
        
        af = socket.AF_INET
        if(useIPv6):
            af = socket.AF_INET6
        
        #On translate la chaine en adresse IP
        try:
            addr = socket.getaddrinfo(self._server_addr, self._server_port)
        except socket.error as se:
            self._last_error = se
            print(se) #TODO Debug Msg
            return False
        #Puis on teste si on peut utiliser IPv6
        for i in range(0,len(addr)):
            if addr[i][0] == socket.AF_INET and not useIPv6:
                self._server_sockaddr = addr[i][4]
            elif addr[i][0] == socket.AF_INET6 and useIPv6:
                self._server_sockaddr = addr[i][4]          
        print(self._server_sockaddr)      
        #On creer le socket pour communiquer avec le serveur
        self._server_socket = socket.socket(af,socket.SOCK_STREAM,0)
        #On active differente option pour le rendre capable de communiquer
        #self._server_socket.setblocking(False)
        #self._server_socket.settimeout(0.050)
        #On connecte le socket avce le serveur
        self._server_socket.bind(("0.0.0.0", 0))
        try:
            self._server_socket.connect(self._server_sockaddr)
        except socket.error as se:
            print(se) #TODO debug
            return False
        return True
    
    def start(self):
        self._server_thread = True
        
        #Si on utilise la connexion dans le cardre d'un thread, on utilise certaines options
        self._server_socket.setblocking(False)
        self._server_thread.settimeout(0.05) #On met un timeout de 50 ms
        
        return threading.Thread.start(self)
    
    def run(self):
    #On recupere les variables dont on a besoin
        connection = self
        sock = connection._server_socket
        server = connection._server_sockaddr
        input = connection._connection_rcvbuffer
        output = connection._connection_sendbuffer
    #output = connection._connection_sendbuffer
    #On creer la boucle infini
        while True:
            try:
                #Si le socket a des information a envoye au server
                while len(output) > 0:
                    msg = output.pop()
                    print(msg)
                    sock.send(msg)
                    #On attend la reception d'un packet
                buffer = sock.recv(4096)
                if len(buffer) > 0:
                    print(buffer) #TODO debug
                    output.append(buffer)
            except socket.error as se:
                print(se)
                #se = se
        return
    
    def send(self,protoPacket): #TODO Ajouter les procedures de lock
        if(protoPacket is None):
            return False
        packet = protoPacket.build()
        print("Send :") #TODO debug
        print(packet) #TODO debug
        if packet is None:
            return False
        #Si on utilise un thread, on utilise les listes pour communiquer
        if(self._server_thread == True):
            self._connection_sendbuffer.append(packet)
        else:
            self._server_socket.send(packet)
        return True
    
    def recv(self):
        #Si on utilise le thread pour communiquer avec le serveur
        if(self._server_thread == True):
            return self._connection_rcvbuffer.pop()
        else:
            try:
                return self._server_socket.recv(4096)
            except socket.error as se:
                print(se) #TODO gerer les erreurs de transmission
        return None
    
    def sendBytes(self,bytes):
        self._connection_sendbuffer.append(bytes)
        return False