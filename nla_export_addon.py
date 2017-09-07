bl_info = {
    "name": "Batch NLA export",
    "category": "Import-Export",
}

import bpy

class NLABatchExport(bpy.types.Operator):
    """Custom NLA batch export"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "export.nlaexport"     # unique identifier for buttons and menu items to reference.
    bl_label = "Batch NLA export"      # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):        # execute() is called by blender when running the operator.
        path = bpy.path.abspath('//')
        tracks = context.object.animation_data.nla_tracks
        # store muted flags so we can restore later
        trackmutes = []
        for track in tracks:
            trackmutes.append(track.mute)

        # for each track that isn't muted, we select the linked action and export as fbx
        for track in tracks:
            if track.mute == False:
                # Mute all tracks that aren't the current one
                for temptrack in tracks:
                    if temptrack != track:
                        temptrack.mute = True
                
                # Select action and export
                bpy.context.active_object.animation_data.action = track.strips[0].action
                bpy.ops.export_scene.fbx (
                    filepath = str(path + "animations/" + "Anim_" + track.strips[0].action.name + '.fbx'), 
                    use_selection = True, 
                    object_types = {'ARMATURE'}, 
                    bake_anim = True, 
                    bake_anim_use_nla_strips = True, 
                    bake_anim_use_all_actions = False, 
                    add_leaf_bones = False, 
                    bake_anim_use_all_bones = True, 
                    use_armature_deform_only = True)
                
                # Restore all mute flags
                it = 0
                for temptrack in tracks:
                    temptrack.mute = trackmutes[it]
                    it += 1
                    
        # Not sure if this is necessary, but let's clear it anyway            
        trackmutes.clear()
        return {'FINISHED'}            # this lets blender know the operator finished successfully.

def register():
    bpy.utils.register_class(NLABatchExport)


def unregister():
    bpy.utils.unregister_class(NLABatchExport)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
