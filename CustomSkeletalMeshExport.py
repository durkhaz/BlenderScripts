bl_info = {
    "name": "Partial Skeletal Mesh Export",
    "category": "Import-Export",
}

import bpy
import os

class SkelMeshExport(bpy.types.Operator):
    """Custom Skeletal Mesh Export"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "export.armorexport"     # unique identifier for buttons and menu items to reference.
    bl_label = "Partial Skeletal Mesh Export"      # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):        # execute() is called by blender when running the operator.
        path = bpy.path.abspath('//armors//') #path of .blend
        selobjs = context.selected_objects
        name_armature = ""
        name_mesh = ""

        if len(selobjs) == 2:
            for obj in selobjs:
                if obj.type == 'ARMATURE':
                    name_armature = obj.name
                    obj.name = 'armature'
                    context.scene.objects.active = obj
                    armature = obj
                if obj.type == 'MESH':
                    name_mesh = obj.name
                    mesh = obj
                    
            print ("Mesh: " + name_mesh + " Armature: " + name_armature)

            if (len(name_mesh) > 0) & (len(name_armature) > 0): 
                if not os.path.exists(path + name_armature):
                    os.makedirs(path + name_armature)
                bpy.ops.export_scene.fbx (
                    filepath = str(path + name_armature + '//' + name_mesh + '.fbx'), 
                    use_selection = True, 
                    object_types = {'ARMATURE', 'MESH'}, 
                    mesh_smooth_type = 'FACE',
                    bake_anim = False, 
                    bake_anim_use_nla_strips = False, 
                    bake_anim_use_all_actions = False, 
                    add_leaf_bones = False, 
                    bake_anim_use_all_bones = False, 
                    use_armature_deform_only = True)
            
            else:
                print("Script needs exactly one armature and one mesh")
            if len(name_armature) > 0:
                armature.name = name_armature
            
        else:
            print("Script needs exactly two elements")
        return {'FINISHED'}            # this lets blender know the operator finished successfully.

def register():
    bpy.utils.register_class(SkelMeshExport)


def unregister():
    bpy.utils.unregister_class(SkelMeshExport)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
