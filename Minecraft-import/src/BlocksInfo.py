import bpy
#import bmesh
import os
from xml.dom.minidom import parse, parseString

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
    #meshUVLoops = cubeMesh.uv_loop_layers[0].data
    #has_uv = (len(cubeMesh.tessface_uv_textures) > 0)
    
    has_uv = (len(cubeMesh.uv_textures) > 0)
    if not has_uv :
        cubeMesh.uv_textures.new()
    
    cubeFaces = dict()
    faceNorth = list()
    faceSouth = list()
    faceEast = list()
    faceWest = list()
    faceTop = list()
    faceBottom = list()
    uvText = cubeMesh.uv_textures.active.data
    #west
    faceWest.append(uvText[4].uv3)
    faceWest.append(uvText[4].uv2)
    faceWest.append(uvText[4].uv1)
    faceWest.append(uvText[4].uv4)
    #bottom
    faceBottom.append(uvText[0].uv4)
    faceBottom.append(uvText[0].uv2)
    faceBottom.append(uvText[0].uv1)
    faceBottom.append(uvText[0].uv3)
    #top
    faceTop.append(uvText[1].uv2)
    faceTop.append(uvText[1].uv1)
    faceTop.append(uvText[1].uv4)
    faceTop.append(uvText[1].uv3)
    #east
    faceEast.append(uvText[2].uv3)
    faceEast.append(uvText[2].uv2)
    faceEast.append(uvText[2].uv1)
    faceEast.append(uvText[2].uv4)
    #north
    faceNorth.append(uvText[5].uv1)
    faceNorth.append(uvText[5].uv4)
    faceNorth.append(uvText[5].uv3)
    faceNorth.append(uvText[5].uv2)
    #south
    faceSouth.append(uvText[3].uv3)
    faceSouth.append(uvText[3].uv2)
    faceSouth.append(uvText[3].uv1)
    faceSouth.append(uvText[3].uv4)
    
    cubeFaces[0] = faceNorth
    cubeFaces[2] = faceSouth
    cubeFaces[3] = faceWest
    cubeFaces[1] = faceEast
    cubeFaces[4] = faceTop
    cubeFaces[5] = faceBottom
    
    id = 1
    
    for key in cubeFaces:
        num = blocksInfo[str(id)][key]
        row = int(num / 16)
        column = int(num % 16)
        print("row : " + str(row) + "  column : " + str(column))
        
        print(str(num))
        print(key)
        cubeFaces[key][0][:] = [column / 16, 1 - (row / 16)]
        cubeFaces[key][1][:] = [(column + 1) / 16, 1 - (row / 16)]
        cubeFaces[key][2][:] = [(column + 1) / 16, 1 - ((row / 16 + (1 /16)))]
        cubeFaces[key][3][:] = [column / 16, 1 - ((row / 16 + (1 /16)))]
    