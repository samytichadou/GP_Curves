import bpy


class GPCURVES_PR_gp_properties(bpy.types.PropertyGroup):
    is_gpcurves: bpy.props.BoolProperty(name="GP Curves")

class GPCURVES_PR_curve_properties(bpy.types.PropertyGroup):
    is_gpcurves: bpy.props.BoolProperty(name="GP Curves")
    gp: bpy.props.PointerProperty(type = bpy.types.GreasePencil, name="Grease Pencil")
    layer_mode: bpy.props.EnumProperty(
            name="Layer Mode",
            items=(
                ('ALL', 'All', ""),
                ('ALL_RENDERED', 'All Rendered', ""),
                ('SPECIFIC', 'Specific', ""),
                ),
        )
    specific_layer_name: bpy.props.StringProperty(name="Specific Layer Name")


### REGISTER ---
def register():
    bpy.utils.register_class(GPCURVES_PR_gp_properties)
    bpy.utils.register_class(GPCURVES_PR_curve_properties)
    bpy.types.GreasePencil.gpcurves_props = \
        bpy.props.PointerProperty(type = GPCURVES_PR_gp_properties, name="GP Curves Properties")
    bpy.types.Curve.gpcurves_props = \
        bpy.props.PointerProperty(type = GPCURVES_PR_curve_properties, name="GP Curves Properties")

def unregister():
    bpy.utils.unregister_class(GPCURVES_PR_gp_properties)
    bpy.utils.unregister_class(GPCURVES_PR_curve_properties)
    del bpy.types.GreasePencil.gpcurves_props
    del bpy.types.Curve.gpcurves_props