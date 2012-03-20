import bpy
from BlocksInfo import BlocksInfo
from MCImportBlocks.MCImportBlockAnvilCollection import MCImportBlockAnvilCollection
from MCImportBlocks.MCImportBlock import MCImportBlock
import time
import os
from bpy_extras.image_utils import load_image
clear = lambda: os.system('cls')

class WorldBuilder:
    
    def __init__(self, blocksInfo, blocks, texturePackPath):
        self.blocks = blocks
        self.blocksInfo = blocksInfo
        self.texturePackPath = texturePackPath
        self.blockMaterials = {}
        
    def BuildWorld(self):
        time_start = time.time()
        self.__ImportTexturePack()
        self.__BuildCubes()
        print("World built in %.4f sec" % (time.time() - time_start))
        
    def __BuildCubes(self):
        #make one cube of each that is present in blocks and duplicate it instead of creating a new one each time
        xSize = 15
        ySize = 255
        zSize = 15
        #clone blocks in blocksCulled
        blocksCulled = self.blocks.copy()
        #Creating materials
        #TODO : Not only IDs, also Types
        for block in self.blocksInfo:
            mat = self.__CreateBlockMaterial(BlockID = self.blocksInfo[block].getBlockId()) 
            if mat is not None:
                self.blockMaterials[self.blocksInfo[block].getBlockId()] = mat
        
        #Little Fix, I dont want to replace everywhere :p
        blocks = self.blocks
        #We strip out ocluded cubes
        for i in range(1,xSize-1):
            for j in range (1,ySize-1):
                for k in range(1,zSize-1):
                    if blocks.hasBlock(i -1, j, k) and blocks.hasBlock(i + 1, j, k):
                        if blocks.hasBlock(i , j -1, k) and blocks.hasBlock(i , j +1, k) :
                            if blocks.hasBlock(i, j, k -1) and blocks.hasBlock(i, j, k +1):
                                blocksCulled.removeBlock(i,j,k)
                        
        #cube generation (takes lot of time if more than 15*15*15)    
        for i in range(0,xSize):
            for j in range (0,ySize):
                for k in range(0,zSize):
                    if blocksCulled.hasBlock(i,j,k):
                        bpy.ops.mesh.primitive_plane_add(location = (i,j,k))
                        ##
                        bpy.context.active_object.scale.x = 0.5
                        bpy.context.active_object.scale.y = 0.5
                        bpy.context.active_object.scale.z = 0.5
                        bpy.ops.object.transform_apply(scale = True)
            print(i)
        
    def __ImportTexturePack(self):
        self.image = load_image(imagepath = self.texturePackPath)
        self.texture = bpy.data.textures.new(name = 'MincraftTexturePack', type = 'IMAGE')
        self.texture.image = self.image
        self.texture.use_interpolation = False
        self.texture.filter_type = 'BOX'
    
    def __CreateBlockMaterial(self, BlockID, BlockType = None):
        if BlockType is not None:
            try:
                material = bpy.data.materials['block' + "%0.4d" % BlockID  + "%0.2d" % BlockType]
            except:
                material = bpy.data.materials.new(name='block' + "%0.4d" % BlockID  + "%0.2d" % BlockType)
        else:
            try:
                material = bpy.data.materials['block' + + "%0.4d" % BlockID]
            except:
                material = bpy.data.materials.new(name='block' + "%0.4d" % BlockID)
        #bpy.ops.object.material_slot_remove()
        slot = material.texture_slots.add()
        slot.texture = self.texture
        slot.texture_coords = 'UV'
        #bpy.data.objects['Cube'].data.materials.append(material)
        return material