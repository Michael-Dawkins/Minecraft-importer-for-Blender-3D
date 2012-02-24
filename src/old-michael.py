'''
Created on 23 sept. 2011

@author: mike
'''

#--- ### Header
bl_info = {
    "name": "MC Import",
    "author": "Michael Dawkins and CYRIL VLAMINCK",
    "version": (0, 1, 0),
    "blender": (2, 5, 9),
    "api": 35622,
    "location": "View3D >Specials (W-key)",
    "category": "Import-Export",
    "description": "Import your minecraft constructions into blender.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
    }

import bpy
import zlib
import random
from bpy.utils import register_module, unregister_module


class MCImportOp(bpy.types.Operator):

	bl_idname = "import_scene.minecraft_region"
	bl_label = "Minecraft Region Import"
	bl_description = "Import minecraft region"


def create_3n_matrix(x,y,z):
    return [[[1 for n in range(x)] for n in range(y)] for n in range(z)]

def main():
    xmatrix = 7
    ymatrix = 7
    zmatrix = 7
    matrix = create_3n_matrix(xmatrix,ymatrix,zmatrix)
    matrix2 = create_3n_matrix(xmatrix,ymatrix,zmatrix)
    
    #on fait un trou dans la matrice pour rigoler
    matrix[10][5][7]=0
    
    #on vire les cubes qui ne seront pas visible
    for i in range(1,xmatrix-1):
        for j in range (1,ymatrix-1):
            for k in range(1,zmatrix-1):
                if ((matrix[i-1][j][k] == 1) and (matrix[i+1][j][k] == 1) and (matrix[i][j-1][k] == 1) and (matrix[i][j+1][k] == 1) and (matrix[i][j][k-1] == 1) and (matrix[i][j][k+1] == 1)):
                    matrix2[i][j][k]=0
        print(i)
                    

    #on genere les cubes (long des que plus de 15*15*15)    
    for i in range(0,xmatrix):
        for j in range (0,ymatrix):
            for k in range(0,zmatrix):
                if (matrix2[i][j][k] == 1):
                    bpy.ops.mesh.primitive_plane_add(location = (i,j,k))
                    bpy.context.scene.cursor_location = bpy.context.active_object.location
                    bpy.context.scene.cursor_location.z -= 1
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                    ##
                    bpy.context.active_object.scale.x = 0.5
                    bpy.context.active_object.scale.y = 0.5
                    bpy.context.active_object.scale.z = 0.5
                    bpy.ops.object.transform_apply(scale = True)
        print(i)
    
def joujou():
    setattr(bpy.context.scene.objects[0],'draw_type','WIRE')
    
    for i in range( 0, len(bpy.context.scene.objects) ):
        setattr(bpy.context.scene.objects[i],'draw_type','WIRE')
        
    for i in range( 0, len(bpy.context.scene.objects) ):
        setattr(bpy.context.scene.objects[i],'draw_type','WIRE')
        
    for i in range (0,len(bpy.context.scene.objects)):
        bpy.context.scene.objects[i].game.physics_type = 'RIGID_BODY'

    bpy.context.scene.render.engine = 'BLENDER_RENDER'
    bpy.context.scene.render.engine = 'BLENDER_GAME'
    
    bpy.ops.transform.resize(value=(2,2,2))
    #bpy.context.screen.areas[5].spaces[0].use_pivot_point_align = False
    
    
    xsize = 5
    ysize = 5
    zsize = 8
    random.seed(1)
    for i in range(0, xsize):
        for j in range(0,ysize):
            for k in range(0,zsize):
                isCube = random.randint(0,1)
                if(isCube == 1):
                    bpy.ops.mesh.primitive_cube_add(location = (i,j,k))
                    bpy.context.scene.cursor_location = bpy.context.active_object.location
                    bpy.context.scene.cursor_location.z -= 1
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                    ##
                    bpy.context.active_object.scale.x = 0.5
                    bpy.context.active_object.scale.y = 0.5
                    bpy.context.active_object.scale.z = 0.5
                    bpy.ops.object.transform_apply(scale = True)
main()