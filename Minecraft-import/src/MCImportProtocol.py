import socket
import threading
from struct import (pack_into, unpack_from)

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
        #On lance le socket d'ecoute dans un thread
        self._proto_connection.start()
        #On lance un handshake
        hand = MCImportProtocolHandshake()
        hand.setUserName(self._proto_username)
        self._proto_connection.send(hand)
        
        login = MCImportProtocolLogin()
        login.setUserName(self._proto_username)
        login.setMCVersion(self._proto_version)
        self._proto_connection.send(login)
        
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
CHAT_PACKET = 0x03
PRECHUNK_PACKET = 0x32
CHUNK_PACKET = 0x33

PING_PACKET = 0xFE
KICK_PACKET = 0xFF
    
def buildPacketFromBytes(b):
    if b is None or len(b) == 0:
        return None
    packet = None
    if b[0] == LOGIN_PACKET:
        packet = MCImportProtocolLogin()
    elif b[0] == HANDSHAKE_PACKET:
        packet = MCImportProtocolHandshake()
    #TODO inserer autre paquet ici
    elif b[0] == KICK_PACKET:
        packet = MCImportProtocolKick()
    if not packet.fromBytes(b):
        return None
    return packet

undefined_packet = []

def getPacketSizeFromBytes(buffer):
    if buffer[0] == LOGIN_PACKET:
        return 23 + unpack_from(">h",buffer,5)[0]
    elif buffer[0] == HANDSHAKE_PACKET:
        return 3 + unpack_from(">h",buffer,1)[0]
    elif buffer[0] == KICK_PACKET:
        return 3 + unpack_from(">h",buffer,1)[0]
    else: #TODO code de debuggage qui log les paquet non implemente
        for i in range(0,len(undefined_packet)):
            if buffer[0] == undefined_packet[i]:
                return len(buffer)
        print("Packet inconnue : " + hex(buffer[0]))
        undefined_packet.append(buffer[0])
        return len(buffer) 
    return
    
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
            return True
        if not self._handshake_return[0] == "-":
            return False
        return False
    
class MCImportProtocolLogin(MCImportProtocolPacket):
    _login_username = ""
    _login_mcversion = VERSION_1_8
    
    def __init__(self):
        self._packet_id = LOGIN_PACKET
        return
    
    def build(self):
        if len(self._login_username) == 0:
            return None
        self._packet_data = bytearray(23 + len(self._login_username) * 2)
        self._packet_data[0] = self._packet_id
        pack_into(">i",self._packet_data,1,self._login_mcversion)
        toString16(self._packet_data,5,self._login_username)
        return self._packet_data
    
    def fromBytes(self,b): #TODO il doit etre fait pour pouvoir continuer a utiliser le protocole
        if b is None or len(b) == 0:
            return False
        
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
    
class MCImportProtocolPreChunk(MCImportProtocolPacket):
    def __init__(self):
        return
    
class MCImportProtocolChunk(MCImportProtocolPacket):
    def __init__(self):
        return
    
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
        #On bind le socket avec le port : On ecoute toutes les connexions exterrieurs
        self._server_socket.bind(("0.0.0.0", 0))
        try:
            self._server_socket.connect(self._server_sockaddr)
        except socket.error as se:
            print(se) #TODO debug
            return False
        return True
    
    def start(self):
        self._server_thread = True
        self._server_socket.setblocking(True)
        return threading.Thread.start(self)
    
    def run(self):
    #On recupere les variables dont on a besoin
        connection = self
        sock = connection._server_socket
        output = connection._connection_rcvbuffer
        
        accumulate_buffer = bytearray(65000) #Ce buffer contient les paquets qui sont lu de maniere sequentiel dans le socket
        accumulate_pos = 0 #Position a partir de laquel on commence a recopier les bytes
        accumulate_remain = 0 #Nombre d'octet manquant pour finir le paquet
        
        buffer_len = 0
        packet_len = 0
        #On creer la boucle infini
        while True:
            try:
                #On attend la reception d'un packet
                buffer = sock.recv(4096)
                buffer_len = len(buffer)
                while buffer_len > 0:  #tant que le buffer n'est pas vide, on traite les paquets
                    #Voici l'algorithme pour choisir si le paquet
                    if accumulate_remain > 0:
                        if (accumulate_remain - buffer_len) == 0: #Il y'as juste suffisament pour remplir le paquet en cour
                            accumulate_buffer[accumulate_pos:accumulate_pos + buffer_len - 1] = buffer #On rempli le buffer ave le contenu recu
                            output.append(accumulate_buffer[0:accumulate_pos + buffer_len - 1]) #On enregistre le paquet dans la liste
                            accumulate_remain = 0 #On signale que l'on peut recevoir un nouveau paquet
                        elif (accumulate_remain - buffer_len) < 0:
                            accumulate_buffer[accumulate_pos:accumulate_pos + accumulate_remain - 1] = buffer[0:accumulate_remain - 1]
                            output.append(accumulate_buffer[0:accumulate_pos + accumulate_remain - 1])
                            buffer = buffer[accumulate_remain:]
                            buffer_len = len(buffer)
                            accumulate_remain = 0
                        else:
                            accumulate_buffer[accumulate_pos : accumulate_pos + buffer_len - 1] = buffer
                            accumulate_pos += buffer_len
                            buffer_len = 0
                    else:
                        packet_len = getPacketSizeFromBytes(buffer)
                        print("Recv : " + hex(buffer[0]) + " " + hex(packet_len))
                        if packet_len > buffer_len:
                            accumulate_buffer[0:buffer_len - 1] = buffer #Si le paquet est segmente, on le sauvegarde dans l'accumulate
                            accumulate_pos = buffer_len 
                            accumulate_remain = packet_len - buffer_len
                            buffer_len = 0
                        elif packet_len < buffer_len:
                            output.append(buffer[0:packet_len - 1])
                            buffer = buffer[packet_len - 1:]
                            buffer_len = len(buffer)
                        else:
                            output.append(buffer)
                            buffer_len = 0
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
    