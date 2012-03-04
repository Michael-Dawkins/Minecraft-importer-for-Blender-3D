from MCImportMap.MCImportBetaRegion import MCImportBetaRegion
from MCImportMap.MCImportAnvilRegion import MCImportAnvilRegion

def main():
    #Code d'example pour utiliser un fichier de region minecraft 1.1
    map = MCImportBetaRegion()
    map.openMCRegion("/Volumes/Data/cyr62110/Documents/Python Projects/mcimport/test/r.-1.0.mcr")
    chunk = map.getChunk(4,3)
    map.closeMCRegion()
    blocks = chunk.getBlocks()
    block = blocks.getBlock(2, 9, 8)
    #Par exemple affiche le bloc
    print("BlockId : " + str(block.getId()) + "\nData : " + str(block.getData()) + "\n")
    
    #Code d'example pour utiliser un fichier de region minecraft 1.2
    map = MCImportAnvilRegion()
    map.openMCRegion("/Volumes/Data/cyr62110/Documents/Python Projects/mcimport/test/r.-1.0.mca")
    chunk = map.getChunk(16,23)
    map.closeMCRegion()
    blocks = chunk.getBlocks()
    block = blocks.getBlock(2, 16, 8)
    #Par exemple affiche le bloc
    print("BlockId : " + str(block.getId()) + "\nData : " + str(block.getData()) + "\n")
    
    #Code d'example pour utiliser le protocole reseau
    #proto = MCImportProtocol.MCImportProtocol()
    #proto.tryConnectionWith("192.168.1.157:25565")
    #proto.etablishCommunicationWith("127.0.0.1:25565")
    return {"FINISHED"} 

main()