#On utilise un design pattern qui separe l'implementation de l'objet MCImportServer
#L'objet server n'est donc plus dependant de l'implementation du protocole et on peut
#changer le protocole en cour de route

class MCImportProtocol28(object):
    
    def __init__(self):
        return
    
    def sendHandshake(self,User):
        return
    
    def sendPlayer(self,User):
        return
