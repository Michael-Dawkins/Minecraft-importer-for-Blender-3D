import bpy
import bpy_extras

from MCImportBlockInfo import *
from bpy.props import (StringProperty, BoolProperty, IntProperty, EnumProperty)

MINECRAFT_TEXTURE_PACK = 'MinecraftTexturePack'
BLOCK_MATERIAL_BASENAME = 'block'

class MCImportTextureBlock(bpy.types.Operator):
    '''Tooltip'''
    bl_idname = "mcimport.texture_block"
    bl_label = "Texture a cube with a Minecraft block texture"
    
    blockId = IntProperty(
                          name = "blockId",
                          min=1,
                          max=4095
                          )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        keywords = self.as_keywords(ignore=())
        
        #We retrieve the qrgument of this operator from the dictionary keywords
        blockId = keywords.get("blockId")
        #
        self.texturePackPath = "/Volumes/Data/cyr62110/Documents/Python Projects/mcimport/test/terrain.png"
        self.texture = self.__getTexturePack()
        #Test
        self.__textureActiveCubeWithBlockTexture(blockId, 0)
        
        return {'FINISHED'}


    def __getCurrentBlockInfoCollection(self):
        xml_path = "/Volumes/Data/cyr62110/Documents/Python Projects/mcimport/test/test_blockscollection.xml"
        xmlreader = MCImportBlockInfoCollectionXMLReader(xml_path)
        return xmlreader.getBlockInfoCollection()
    
    def __getTexturePack(self):
        tp = None
        try:
            tp = bpy.data.textures[MINECRAFT_TEXTURE_PACK]
        except:
            tp = self.__importTexturePack()
        return tp
    
    def __importTexturePack(self):
        image = bpy_extras.image_utils.load_image(imagepath = self.texturePackPath)
        texture = bpy.data.textures.new(name = MINECRAFT_TEXTURE_PACK, type = 'IMAGE')
        texture.image = image
        texture.use_interpolation = False
        texture.filter_type = 'BOX'
        return texture
        
    def __cleanActiveObjectMaterial(self):
        current_object = bpy.context.active_object
        if current_object is None:
            return
        for i in range(len(current_object.material_slots)):
            bpy.ops.object.material_slot_remove()
        
    def __setActiveObjectMaterial(self, material):
        current_object = bpy.context.active_object
        self.__cleanActiveObjectMaterial()
        bpy.ops.object.material_slot_add()
        material_slot = current_object.material_slots[0]
        material_slot.material = material
        return
        
    def __getBlockMaterial(self, blockId, blockType = None):
        if blockType is not None:
            materialName = 'block' + "%0.4d" % blockId  + "%0.2d" % blockType
        else:
            materialName = 'block' + "%0.4d" % blockId
        material = None
        try:
            material = bpy.data.materials[materialName] 
        except:
            material = self.__createBlockMaterial(blockId, blockType)
        return material
        
    def __createBlockMaterial(self, blockId, blockType = None):
        if blockType is not None:
            material = bpy.data.materials.new(name=BLOCK_MATERIAL_BASENAME  + "%0.4d" % blockId  + "%0.2d" % blockType)
        else:
            material = bpy.data.materials.new(name=BLOCK_MATERIAL_BASENAME  + "%0.4d" % blockId)

        slot = material.texture_slots.add()
        slot.texture = self.texture
        slot.texture_coords = 'UV'

        return material
        
    def __textureActiveCubeWithBlockTexture(self, blockId, blockType):
        cubeMesh = bpy.context.active_object.data
        if cubeMesh is None:
            return False
        
        #Use the texture pack as an UV Map for the cube
        material = self.__getBlockMaterial(blockId, blockType)
        self.__setActiveObjectMaterial(material)
        
        #Get the texture map XML Mapping
        blockInfoCollection = self.__getCurrentBlockInfoCollection()
        #Then texture the cube
        #If the mesh has no UV Map, then create one first
        has_uv = (len(cubeMesh.uv_textures) > 0)
        if not has_uv :
            cubeMesh.uv_textures.new()
            
        #Then create a list containing all its uvs
        cubeFaces = MCImportTextureBlock.__defineUVMapLists(cubeMesh)
        
        #And set the UV Maps
        for key in cubeFaces:
            #Now, we use the new algotihm to texture the block
            blockInfo = blockInfoCollection[blockId]
            if not blockInfo.hasTypes():
                num = blockInfo[key]
            else:
                num = blockInfo[blockType][key]
            
            row = int(num / 16)
            column = int(num % 16)

            cubeFaces[key][0][:] = [column / 16, 1 - (row / 16)]
            cubeFaces[key][1][:] = [(column + 1) / 16, 1 - (row / 16)]
            cubeFaces[key][2][:] = [(column + 1) / 16, 1 - ((row / 16 + (1 /16)))]
            cubeFaces[key][3][:] = [column / 16, 1 - ((row / 16 + (1 /16)))]
    
    @staticmethod
    def __defineUVMapLists(cubeMesh):
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
        
        return cubeFaces

def register():
    bpy.utils.register_class(MCImportTextureBlock)


def unregister():
    bpy.utils.unregister_class(MCImportTextureBlock)


if __name__ == "__main__":
    register()

