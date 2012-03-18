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
        
    def BuildWorld(self):
        time_start = time.time()
        clear()
        
        image = load_image(imagepath = self.texturePackPath)
        print(type(image))
        texture = bpy.data.textures.new(name = 'MincraftTexturePack', type = 'IMAGE')
        texture.image = image
        texture.use_interpolation = False
        texture.filter_type = 'BOX'
        material = bpy.data.materials.new(name='block')
        bpy.ops.object.material_slot_remove()
        slot = material.texture_slots.add()
        slot.texture = texture
        slot.texture_coords = 'UV'
        
        #create the blockInfo object automatically parses the file at the path given
        blocksInfo = BlocksInfo(path_xml)
        print(repr(blocksInfo))
        TextureDirtBlock(blocksInfo)
        
        bpy.data.objects['Cube'].data.materials.append(material)
        
        print("script execution finished in %.4f sec" % (time.time() - time_start))
        
        #TODO : move paths from blocksInfo to a better place
        #TODO : name material based on id (and type of block)
        #TODO : take old code to generate cube matrix
        #make sure new blocksINfo and parsing are working
        #Move material generation to private method
        #code matric generation in BuildWorld method
        
    def BuildCubes(self):
        pass