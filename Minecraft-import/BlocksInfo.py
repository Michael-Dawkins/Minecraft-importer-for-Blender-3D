import bpy
import bmesh
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
            faceIter = int(len(faces.childNodes) /2) 
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
        return self.parsedData[index]
    
    def __repr__(self):
        return repr(self.parsedData)
    
def TextureDirtBlock(blocksInfo):
    
    cubeMesh = bpy.context.selected_objects[0].data
    if not cubeMesh.uv_textures:
        cubeMesh.uv_textures.new()
    meshUVLoops = cubeMesh.uv_loop_layers[0].data
    cubeFaces = dict()
    faceNorth = list()
    faceSouth = list()
    faceEast = list()
    faceWest = list()
    faceTop = list()
    faceBottom = list()
    
    uvs = bpy.context.selected_objects[0].data.uv_loop_layers[0].data

    #west
    faceWest.append(meshUVLoops[18].uv)
    faceWest.append(meshUVLoops[17].uv)
    faceWest.append(meshUVLoops[16].uv)
    faceWest.append(meshUVLoops[19].uv)
    #bottom
    faceBottom.append(meshUVLoops[2].uv)
    faceBottom.append(meshUVLoops[1].uv)
    faceBottom.append(meshUVLoops[0].uv)
    faceBottom.append(meshUVLoops[3].uv)
    #top
    faceTop.append(meshUVLoops[5].uv)
    faceTop.append(meshUVLoops[4].uv)
    faceTop.append(meshUVLoops[7].uv)
    faceTop.append(meshUVLoops[6].uv)
    #east
    faceEast.append(meshUVLoops[10].uv)
    faceEast.append(meshUVLoops[9].uv)
    faceEast.append(meshUVLoops[8].uv)
    faceEast.append(meshUVLoops[11].uv)
    #north
    faceNorth.append(meshUVLoops[20].uv)
    faceNorth.append(meshUVLoops[23].uv)
    faceNorth.append(meshUVLoops[22].uv)
    faceNorth.append(meshUVLoops[21].uv)
    #south
    faceSouth.append(meshUVLoops[14].uv)
    faceSouth.append(meshUVLoops[13].uv)
    faceSouth.append(meshUVLoops[12].uv)
    faceSouth.append(meshUVLoops[15].uv)
    
    cubeFaces[0] = faceNorth
    cubeFaces[2] = faceSouth
    cubeFaces[3] = faceWest
    cubeFaces[1] = faceEast
    cubeFaces[4] = faceTop
    cubeFaces[5] = faceBottom
    
    id = 98
    
    for key in cubeFaces:
        num = blocksInfo[str(id)][key]
        row = int(num / 16)
        column = int(num % 16)
        print("row : " + str(row) + "  column : " + str(column))
        
        print(str(num))
        cubeFaces[key][0] = [column / 16, 1 - (row / 16)]
        print(cubeFaces[key][0])
        cubeFaces[key][1] = [(column + 1) / 16, 1 - (row / 16)]
        print(cubeFaces[key][1])
        cubeFaces[key][2] = [(column + 1) / 16, 1 - ((row / 16 + (1 /16)))]
        print(cubeFaces[key][2])
        cubeFaces[key][3] = [column / 16, 1 - ((row / 16 + (1 /16)))]
        print(cubeFaces[key][3])
    
    
    #get a bmesh
    #bm = bmesh.new()
    #fill the bmesh with mesh data
    #bm.from_mesh(cubeMesh)
    #bm.to_mesh(cubeMesh)
    
    
if __name__ == "__main__" :
    time_start = time.time()
    clear()
    #create the blockInfo object automatically parses the file at the path given
    blocksInfo = BlocksInfo(path_xml)
    print(repr(blocksInfo))
    TextureDirtBlock(blocksInfo)
    
    print("script execution finished in %.4f sec" % (time.time() - time_start))


    