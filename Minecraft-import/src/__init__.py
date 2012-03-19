import sys
sys.path.append(r'/Applications/Blender/blender.app/Contents/MacOs/2.60/scripts/addons/mcimport')

import bpy
from bpy_extras.io_utils import (ImportHelper)
import bpy.utils
from bpy.props import (StringProperty, BoolProperty, IntProperty, EnumProperty)
from MCImportMap.MCImportAnvilRegion import MCImportAnvilRegion
import BlocksInfo

bl_info = {
    "name": "Minecraft Chunk Format",
    "author": "Michael Dawkins, Cyril Vlaminck",
    "version": (0, 1, 1),
    "blender": (2, 5, 7),
    "api": 35622,
    "location": "File > Import-Export",
    "description": ("Import Minecraft Chunk from Region File (*.mca)"),
    "warning": "",
    "wiki_url": "",
    "tracker_url": "http://bug.cvlaminck.fr",
    "support": 'OFFICIAL',
    "category": "Import-Export"}

## Classe principale pour l'importation depuis les fichiers de minecraft
class MCImport(bpy.types.Operator, ImportHelper):
    ''' Import from Minecraft Region File '''
    #On surcharge les prop de l'Operator pour configurer notre propre operateur
    bl_idname = 'import_mesh.mcimport' #En python : bpy.ops.import_mesh.mcimport
    bl_label = 'MCImport' #Nom de notre module ( afficher sur le bouton ainsi que dans les menus de la fenetre import )
    bl_description= 'Import Chunk from Minecraft Region File' #Description de l'operateur pour l'aide
    
    #On surcharge les proprietes de l'ImportHelper pour le configurer
    ##Extension des fichiers supportes par l'importeur
    filename_ext = ".mca"
    ##Filtre pour le'explorateur de fichier
    filter_glob = StringProperty( 
            default="*.mca",
            options={'HIDDEN'},
            )
    
    ##Propriete entiere representate le plancher d'importation ( Les blocs ayant un Z en dessous ne seront pas importes)
    z_min = IntProperty(name = "Zmin", description = "Minimum Z coord of imported blocks", default = 0, soft_min = 0, soft_max = 126)
    ##Propriete entiere represente le plafon d'importation (Tout les blocs ayant un Z superieur ne seront pas importes)
    z_max = IntProperty(name = "Zmax", description = "Maximum Z coord of imported blocks", default = 127, soft_min = 1, soft_max = 127)
    ##Propriete entiere representant postion en X du premier chunk importe
    x_chunk = IntProperty(name = "X", description = "X-Coord of the first imported chunk", default=0,  soft_min = 0, soft_max = 31)
    ##Propriete entiere representant la postion en Z du premier chunk importe
    z_chunk = IntProperty(name = "Z", description = "Z-Coord of the first imported chunk", default=0,  soft_min = 0, soft_max = 31)
    ##
    xsize_chunk = IntProperty(name = "XSize", description = "Number of Chunk imported", default=1,  soft_min = 1, soft_max = 31)
    ##
    zsize_chunk = IntProperty(name = "ZSize", description = "Number of Chunk imported", default=1,  soft_min = 1, soft_max = 31)
    ##
    import_type = EnumProperty(items = (('C',"Cubes",""),('P',"Planes","")), name = "Import as", description = "Choose the type of object which the importer will use", default = 'C')
    
    ##Surcharge de la fonction permettant d'executer notre propre code d'operateur
    def execute(self, context):
        #On recupere les informations depuis l'interface
        keywords = self.as_keywords(ignore=())
        
        #On recupere les valeurs depuis le dictionnaire keywords
        mcrpath = keywords.get("filepath")
        chunkX = keywords.get("x_chunk")
        chunkZ = keywords.get("z_chunk")
        
        #On lance l'algo d'importation depuis un fichier
        mcImport = MCImportAnvilRegion()
        if(mcImport.openMCRegion(mcrpath)):
            mcCurrentChunk = mcImport.getChunk(chunkX, chunkZ)
            print(mcCurrentChunk.getBlocks().getBlock(10, 64, 8)) #TODO Message de Debug
        else:
            return {'CANCELLED'}
        return {'FINISHED'}
    
    ##Surcharge d'une fonction permettant de dessiner le panel represente dans l'interface d'importation
    def draw(self,context):
        layout = self.layout
        
        #On demande le type d'importation souhaite
        row = layout.row(align = True)
        row.prop(self, "import_type")
        
        #On genere la premiere boite permettant de fixer les coord Z
        #box = layout.box()
        box = layout
        #row = box.row()
        #row.label("Z coordinate")
        row = box.row()
        row.prop(self, "z_min")
        #row = box.row()
        row.prop(self, "z_max")
        
        #On genere la seconde boite pour choisir la taille et la position du chunk
        box = layout.box()
        #box = layout
        row = box.row()
        row.label("Chunk Coord/Size")
        row = box.row()
        row.prop(self, "x_chunk")
        #row = box.row()
        row.prop(self, "z_chunk")
        row = box.row()
        row.prop(self, "xsize_chunk")
        row.prop(self, "zsize_chunk")
        
##Fonction permettant l'enregistrement de notre operateur dans le menu Import
def mcimport_menu_item(self,context):
    self.layout.operator(MCImport.bl_idname,"Minecraft (*.mca)")

##Enregistre notre operateur dans Blender
def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(mcimport_menu_item)

##Supprime notre module de la liste des operateurs
def unregister():
    bpy.types.INFO_MT_file_import.remove(mcimport_menu_item)
    bpy.utils.unregister_module(__name__)

#Patch correctif present pour la forme
if __name__ == "__main__":
    register()