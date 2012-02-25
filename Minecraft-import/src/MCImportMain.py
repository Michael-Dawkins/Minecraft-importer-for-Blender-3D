from MBImportMap import MCImportBetaRegion

def main():
    #Code d'example pour utiliser un fichier de region minecraft 1.1
    map = MCImportBetaRegion.MCImportBetaRegion()
    map.openMCRegion("/Volumes/Data/cyr62110/Documents/mcimport/test/r.-1.0.mcr")
    chunk = map.getChunk(4,3)
    blocks = chunk.getBlocks()
    block = blocks.getBlock(2, 65, 8)
    #Par exemple affiche le bloc
    print("BlockId : " + block.getId().__str__() + "\nData : " + block.getData().__str__())
    
    
    #Code d'example pour utiliser le protocole reseau
    #proto = MCImportProtocol.MCImportProtocol()
    #proto.tryConnectionWith("192.168.1.157:25565")
    #proto.etablishCommunicationWith("127.0.0.1:25565")
    return {"FINISHED"} 

main()