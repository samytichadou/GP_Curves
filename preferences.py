import bpy
import os

addon_name=os.path.basename(os.path.dirname(__file__))

class GPCURVES_PF_preferences(bpy.types.AddonPreferences) :
    bl_idname = addon_name

    debug: bpy.props.BoolProperty(
        name="Debug",
        )

    def draw(self, context) :
        layout = self.layout
        layout.prop(self, "debug")

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)

### REGISTER ---
def register():
    bpy.utils.register_class(GPCURVES_PF_preferences)
def unregister():
    bpy.utils.unregister_class(GPCURVES_PF_preferences)
