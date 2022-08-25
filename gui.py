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

        layout = self.layout
        layout.label(text="Bake GP Curves placeholder")


class GPCURVES_PT_curve_panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "GP Curves"

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type == 'CURVE'

    def draw_header(self, context):
        ob = context.object
        props = ob.data.gpcurves_props
        self.layout.prop(props, "is_gpcurves", text="")

    def draw(self, context):
        ob = context.object
        props = ob.data.gpcurves_props

        layout = self.layout
        layout.active = props.is_gpcurves

        layout.prop(props, "gp")
        layout.prop(props, "layer_mode")
        sub=layout.row()
        if not props.layer_mode=="SPECIFICS":
            sub.enabled=False
        sub.prop(props, "specific_layers")


# auto profile topbar
def gpcurves_topbar(self, context):
    if context.region.alignment == 'RIGHT':
        layout=self.layout
        props=context.scene.gpcurves_scene_props
        layout.prop(props, "gpcurves_process", text="", icon='OUTLINER_DATA_GREASEPENCIL')


### REGISTER ---
def register():
    bpy.utils.register_class(GPCURVES_PT_gp_panel)
    bpy.utils.register_class(GPCURVES_PT_curve_panel)

    bpy.types.TOPBAR_HT_upper_bar.prepend(gpcurves_topbar)

def unregister():
    bpy.utils.unregister_class(GPCURVES_PT_gp_panel)
    bpy.utils.unregister_class(GPCURVES_PT_curve_panel)

    bpy.types.TOPBAR_HT_upper_bar.remove(gpcurves_topbar)