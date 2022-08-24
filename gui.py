import bpy


class GPCURVES_PT_gp_panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "GP Curves"

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type == 'GPENCIL'

    def draw(self, context):
        ob = context.object
        props = ob.data.gpcurves_props

        layout = self.layout
        layout.prop(props, "is_gpcurves")


class GPCURVES_PT_curve_panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "GP Curves"

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type == 'CURVE'

    def draw(self, context):
        ob = context.object
        props = ob.data.gpcurves_props

        layout = self.layout
        layout.prop(props, "is_gpcurves")
        layout.prop(props, "gp")
        layout.prop(props, "layer_mode")
        sub=layout.row()
        if not props.layer_mode=="SPECIFIC":
            sub.enabled=False
        sub.prop(props, "specific_layer_name")


### REGISTER ---
def register():
    bpy.utils.register_class(GPCURVES_PT_gp_panel)
    bpy.utils.register_class(GPCURVES_PT_curve_panel)

def unregister():
    bpy.utils.unregister_class(GPCURVES_PT_gp_panel)
    bpy.utils.unregister_class(GPCURVES_PT_curve_panel)