import bpy
import os
from xml.dom.minidom import parse, parseString
import time
clear = lambda: os.system('cls')

path_texture_pack = "C:\\Users\\mike\\Documents\\Blender\\python-dev\\pydev-blender\\workspaces\\Minecraft-import\\Minecraft-import\\src\\terrain.png"
    
bpy.ops.image.open(filepath = "C:\\Users\\mike\\Documents\\Blender\\python-dev\\pydev-blender\\workspaces\\Minecraft-import\\Minecraft-import\\src\\terrain.png", relative_path=False)

path_xml = "C:\\Users\\mike\\Documents\\Blender\\python-dev\\pydev-blender\\workspaces\\Minecraft-import\\Minecraft-import\\src\\blockscollection.xml"

'''Class responsible for parsing and accessing parsed data (info about face texturing for a given block ID)'''
class BlocksInfo:
    
    def __init__(self, xmlPath):
        self.path_xml = xmlPath
        self.parsedData = dict()
        self.ParseXML(self.parsedData)
   
    '''Parses blockscollection.xml and fill in a dictionary'''
    def ParseXML(self, parsedData):
        verbose = False
        dom1 = parse(path_xml)
        if verbose:
            print(dom1.toxml())
        blocks = dom1.getElementsByTagName("Blocks")
        blockElements = blocks[0].getElementsByTagName("Block")
        if verbose:
            print("elements in blocks are :")
        i = 0
        
        for elem in blockElements:
            if verbose:
                print("ID : " + blockElements[i].attributes["ID"].value)
            id = blockElements[i].attributes["ID"].value
            faceList = list()
            faces = blockElements[i].getElementsByTagName("Faces")[0]
            faceIter = int(len(faces.childNodes) /2) -1
            if verbose:
                print("Number : " + str(faceIter))
            for j in range(0,faceIter):
                if verbose :
                    print(str(j))
                faceElem = faces.getElementsByTagName("F" + str(j))[0]
                if verbose:
                    print("Face :" + str(faceElem.firstChild.nodeValue))
                faceList.append(int(faceElem.firstChild.nodeValue))
            if verbose:    
                print(str(i))
            parsedData[id] = faceList
            i = i+1
            
    def __getitem__(self, index):
        return parsedData[index]
    
    def __repr__(self):
        return repr(self.parsedData)
    
if __name__ == "__main__" :
    time_start = time.time()
    clear()
    
    #create the blockInfo object automatically parses the file at the path given
    blocksInfo = BlocksInfo(path_xml)
    print(repr(blocksInfo))
    
    print("script execution finished in %.4f sec" % (time.time() - time_start))