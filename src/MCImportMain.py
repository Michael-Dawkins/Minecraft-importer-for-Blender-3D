'''
Created on 24 sept. 2011

@author: cyr62110
'''
import MCImportBetaMap
import MCImportProtocol

def main():
    proto = MCImportProtocol.MCImportProtocol()
    #proto.tryConnectionWith("192.168.1.157:25565")
    proto.etablishCommunicationWith("127.0.0.1:25565")
    return {"FINISHED"}

main()