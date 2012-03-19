import bpy
from BlocksInfo import BlocksInfo
from MCImportBlocks.MCImportBlockAnvilCollection import MCImportBlockAnvilCollection
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
        clear()
        
        __BuildCubes()
        
        print("World built in %.4f sec" % (time.time() - time_start))
        
    def __BuildCubes(self):
        xmatrix = 7
        ymatrix = 7
        zmatrix = 7
        matrix = Create_3n_matrix(xmatrix,ymatrix,zmatrix)
        matrix2 = Create_3n_matrix(xmatrix,ymatrix,zmatrix)
        
        #Creating materials
        for id in self.blocksInfo :
            #TODO : Not only IDs, also Types
            self.blockMaterials[id] = __CreateBlockMaterial(BlockID = id)
        
        #We strip out ocluded cubes
        for i in range(1,xmatrix-1):
            for j in range (1,ymatrix-1):
                for k in range(1,zmatrix-1):
                    if ((matrix[i-1][j][k] == 1) and (matrix[i+1][j][k] == 1) and (matrix[i][j-1][k] == 1) and (matrix[i][j+1][k] == 1) and (matrix[i][j][k-1] == 1) and (matrix[i][j][k+1] == 1)):
                        matrix2[i][j][k]=0
                        
        #cube generation (takes lot of time if more than 15*15*15)    
        for i in range(0,xmatrix):
            for j in range (0,ymatrix):
                for k in range(0,zmatrix):
                    if (matrix2[i][j][k] == 1):
                        bpy.ops.mesh.primitive_plane_add(location = (i,j,k))
                        #bpy.context.scene.cursor_location = bpy.context.active_object.location
                        #bpy.context.scene.cursor_location.z -= 1
                        #bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                        ##
                        bpy.context.active_object.scale.x = 0.5
                        bpy.context.active_object.scale.y = 0.5
                        bpy.context.active_object.scale.z = 0.5
                        bpy.ops.object.transform_apply(scale = True)
            print(i)
            
    def Create_3n_matrix(self,x,y,z):
        return [[[1 for n in range(x)] for n in range(y)] for n in range(z)]
        
    def __ImportTexturePack(self):
        self.image = load_image(imagepath = self.texturePackPath)
        self.texture = bpy.data.textures.new(name = 'MincraftTexturePack', type = 'IMAGE')
        self.texture.image = self.image
        self.texture.use_interpolation = False
        self.texture.filter_type = 'BOX'
    
    def __CreateBlockMaterial(self, BlockID, BlockType = None):
        if BlockType is not None:
            material = bpy.data.materials.new(name='block' + str(BlockID) + str(BlockType))
        else:
            material = bpy.data.materials.new(name='block' + str(BlockID))
        #bpy.ops.object.material_slot_remove()
        slot = material.texture_slots.add()
        slot.texture = self.texture
        slot.texture_coords = 'UV'
        #bpy.data.objects['Cube'].data.materials.append(material)
        return material