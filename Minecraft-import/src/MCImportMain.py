from MCImportMap.MCImportBetaRegion import MCImportBetaRegion
from MCImportMap.MCImportAnvilRegion import MCImportAnvilRegion
from MCImportNetwork.MCImportServer import MCImportServer
from MCImportBlocks import MCImportBlockCollection, MCImportBlock
from MCImportBlockInfo import MCImportBlockInfoCollectionXMLReader
import readline

def main():
    
    X=2
    Y=64
    Z=8
    
    #Code d'exemple pour le parseur XML
    #TODO
    xmlReader = MCImportBlockInfoCollectionXMLReader("/Volumes/Data/cyr62110/Documents/Python Projects/mcimport/test/test_blockscollection.xml")
    blocks = xmlReader.getBlockInfoCollection()
    for i in blocks:
        print( str(blocks[i]) + "\n" )
    
    #Code d'example pour utiliser un fichier de region minecraft 1.1
    map = MCImportBetaRegion()
    map.openMCRegion("/Volumes/Data/cyr62110/Documents/Python Projects/mcimport/test/r.-1.0.mcr")
    chunk = map.getChunk(4,3)
    map.closeMCRegion()
    blocks = chunk.getBlocks()
    
    block = blocks.getBlock(X, Y, Z)
    #Par exemple affiche le bloc
    print("BlockId : " + str(block.getId()) + "\nData : " + str(block.getData()) + "\n")
    
    #Code d'example pour utiliser un fichier de region minecraft 1.2
    map = MCImportAnvilRegion()
    map.openMCRegion("/Volumes/Data/cyr62110/Documents/Python Projects/mcimport/test/r.-1.0.mca")
    chunk = map.getChunk(16,23)
    map.closeMCRegion()
    blocks = chunk.getBlocks()
    block = blocks.getBlock(X, Y, Z)
    #Par exemple affiche le bloc
    print("BlockId : " + str(block.getId()) + "\nData : " + str(block.getData()) + "\n")
    
    #Test de l'operateur de copy et de modification de block
    redWoolBlock = MCImportBlock.MCImportBlock()
    redWoolBlock.setId(35)
    redWoolBlock.setData(14)
    
    cpBlocks = blocks.copy()
    cpBlocks.setBlock(X, Y, Z, redWoolBlock)
    #original
    block = blocks.getBlock(X, Y, Z)
    print("Original : %d\n Data: %d\n" % (block.getId(), block.getData()))
    #modified
    block = cpBlocks.getBlock(X, Y, Z)
    print("Modified : %d\n Data: %d\n" % (block.getId(), block.getData()))
    #So copy really creates a full copy of the collection
    #TODO add the same for MCImportBlockBetaCollection
    
    #Code d'example pour utiliser un serveur minecraft 1.2
    server = MCImportServer("127.0.0.1",25565)
    server.setProtocolVersion(28)
    server.start()
    
    input("Test:")
    print("Finished")
    return {"FINISHED"} 

main()