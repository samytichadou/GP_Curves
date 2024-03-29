import bpy

from .curves_handler import set_handlers, remove_handlers


def gpcurves_process_update(self, context):
    if self.gpcurves_process:
        print("GPCURVES --- GP Curves Process ON")
        set_handlers()
    else:
        print("GPCURVES --- GP Curves Process OFF")
        remove_handlers()

class GPCURVES_PR_greasepencil_properties(bpy.types.PropertyGroup):
    bake_collection: bpy.props.PointerProperty(type = bpy.types.Collection, name="Baked Curves Collection")
    temp_bake_collection: bpy.props.PointerProperty(type = bpy.types.Collection, name="Baked Curves Collection")
    layer_mode: bpy.props.EnumProperty(
        name="Layer Mode",
        items=(
            ('ALL', 'All GP Layers', ""),
            ('VISIBLE', 'Only Visible GP Layers', ""),
            ('SPECIFICS', 'Specific(s) GP layer(s)', ""),
            ),
    )
    
    frame_range: bpy.props.EnumProperty(
        name="Frame Range",
        items=(
            ('ALL', 'All GP Frames', ""),
            ('SCENE', 'Scene Frame Range', ""),
            ('CUSTOM', 'Custom Frame Range', ""),
            ),
    )
    custom_start_frame: bpy.props.IntProperty(name="Start", min=0, default=1)
    custom_end_frame: bpy.props.IntProperty(name="End", min=0, default=250)

    specific_layers: bpy.props.StringProperty(
        name="Specific Layers",
        description="GP Layer(s) name(s) separated by comma",    
    )
    temp_specific_layers: bpy.props.StringProperty(
        name="Specific Layers",
        description="GP Layer(s) name(s) separated by comma",    
    )

    object_properties_parent: bpy.props.PointerProperty(type = bpy.types.Object, name="Object Properties Parent")
    temp_object_properties_parent: bpy.props.PointerProperty(type = bpy.types.Object, name="Object Properties Parent")

    bake_hash: bpy.props.StringProperty(name="Bake Hash")

class GPCURVES_PR_curve_properties(bpy.types.PropertyGroup):
    is_gpcurves: bpy.props.BoolProperty(name="GP Curves")
    gp: bpy.props.PointerProperty(type = bpy.types.GreasePencil, name="Grease Pencil")
    layer_mode: bpy.props.EnumProperty(
            name="Layer Mode",
            items=(
                ('ALL', 'All GP Layers', ""),
                ('VISIBLE', 'Only Visible GP Layers', ""),
                ('SPECIFICS', 'Specific(s) GP layer(s)', ""),
                ),
        )
    specific_layers: bpy.props.StringProperty(
        name="Specific Layers",
        description="GP Layer(s) name(s) separated by comma",    
    )
    
    bake_hash: bpy.props.StringProperty(name="Bake Hash")

class GPCURVES_PR_scene_properties(bpy.types.PropertyGroup):
    gpcurves_process: bpy.props.BoolProperty(name="GP Curves Process", update=gpcurves_process_update)

### REGISTER ---
def register():
    bpy.utils.register_class(GPCURVES_PR_greasepencil_properties)
    bpy.utils.register_class(GPCURVES_PR_curve_properties)
    bpy.utils.register_class(GPCURVES_PR_scene_properties)
    bpy.types.GreasePencil.gpcurves_gp_props = \
        bpy.props.PointerProperty(type = GPCURVES_PR_greasepencil_properties, name="GP Grease Pencil Properties")
    bpy.types.Curve.gpcurves_curve_props = \
        bpy.props.PointerProperty(type = GPCURVES_PR_curve_properties, name="GP Curves Properties")
    bpy.types.Scene.gpcurves_scene_props = \
        bpy.props.PointerProperty(type = GPCURVES_PR_scene_properties, name="GP Curves Scene Properties")

def unregister():
    bpy.utils.unregister_class(GPCURVES_PR_greasepencil_properties)
    bpy.utils.unregister_class(GPCURVES_PR_curve_properties)
    bpy.utils.unregister_class(GPCURVES_PR_scene_properties)
    del bpy.types.GreasePencil.gpcurves_gp_props
    del bpy.types.Curve.gpcurves_curve_props
    del bpy.types.Scene.gpcurves_scene_props
