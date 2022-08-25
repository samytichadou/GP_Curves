import bpy

from .curves_handler import gp_curve_handler


def gpcurves_process_update(self, context):
    if self.gpcurves_process:
        bpy.app.handlers.depsgraph_update_post.append(gp_curve_handler)
        bpy.app.handlers.frame_change_post.append(gp_curve_handler)
        print("GPCURVES -- GP Curves Process ON")
    else:
        bpy.app.handlers.depsgraph_update_post.remove(gp_curve_handler)
        bpy.app.handlers.frame_change_post.remove(gp_curve_handler)
        print("GPCURVES -- GP Curves Process OFF")
    return

class GPCURVES_PR_curve_properties(bpy.types.PropertyGroup):
    is_gpcurves: bpy.props.BoolProperty(name="GP Curves")
    gp: bpy.props.PointerProperty(type = bpy.types.GreasePencil, name="Grease Pencil")
    layer_mode: bpy.props.EnumProperty(
            name="Layer Mode",
            items=(
                ('ALL', 'All', ""),
                ('ALL_RENDERED', 'All Rendered', ""),
                ('SPECIFICS', 'Specifics', ""),
                ),
        )
    specific_layers: bpy.props.StringProperty(name="Specific Layers")

class GPCURVES_PR_scene_properties(bpy.types.PropertyGroup):
    gpcurves_process: bpy.props.BoolProperty(name="GP Curves Process", update=gpcurves_process_update)


### REGISTER ---
def register():
    bpy.utils.register_class(GPCURVES_PR_curve_properties)
    bpy.utils.register_class(GPCURVES_PR_scene_properties)
    bpy.types.Curve.gpcurves_props = \
        bpy.props.PointerProperty(type = GPCURVES_PR_curve_properties, name="GP Curves Properties")
    bpy.types.Scene.gpcurves_scene_props = \
        bpy.props.PointerProperty(type = GPCURVES_PR_scene_properties, name="GP Curves Scene Properties")

def unregister():
    bpy.utils.unregister_class(GPCURVES_PR_curve_properties)
    bpy.utils.unregister_class(GPCURVES_PR_scene_properties)
    del bpy.types.Curve.gpcurves_props
    del bpy.types.Scene.gpcurves_scene_props