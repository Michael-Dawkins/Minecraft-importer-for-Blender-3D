import bpy
import os
from xml.dom.minidom import parse, parseString
import time
clear = lambda: os.system('cls')
time_start = time.time()

path_xml = "C:\\Users\\mike\\Documents\\Blender\\python-dev\\pydev-blender\\workspaces\\Minecraft-import\\Minecraft-import\\src\\blockscollection.xml"

path_texture_pack = "C:\\Users\\mike\\Documents\\Blender\\python-dev\\pydev-blender\\workspaces\\Minecraft-import\\Minecraft-import\\src\\terrain.png"

bpy.ops.image.open(filepath="C:\\Users\\mike\\Documents\\Blender\\python-dev\\pydev-blender\\workspaces\\Minecraft-import\\Minecraft-import\\src\\terrain.png", relative_path=False)

def ParseXML():
    dom1 = parse(path_xml)
    print(dom1.toxml())
    blocks = dom1.getElementsByTagName("Blocks")
    blockElements = blocks[0].getElementsByTagName("Block")
    print("elements in blocks are :")
    i = 0
    
    for elem in blockElements:
        faces = blockElements[i].getElementsByTagName("Faces")[0]
        faceIter = int(len(faces.childNodes) /2) -1
        print(str(faceIter))
        for j in range(0,faceIter):
            print(str(j))
            faceElem = faces.getElementsByTagName("F" + str(j))[0]
            print("Face :" + str(faceElem.firstChild.nodeValue))
        print(str(i))
        i = i+1
    #print("len = " + len(blocks))

clear()
ParseXML()
print("script execution finished in %.4f sec" % (time.time() - time_start))
