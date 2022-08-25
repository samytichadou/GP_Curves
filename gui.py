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
        props = ob.data.gpcurves_gp_props

        layout = self.layout 

        layout.prop(props, "bake_collection", text="Collection")
        layout.prop(props, "layer_mode", text="Mode")
        sub=layout.row(align=True)
        if not props.layer_mode=="SPECIFICS":
            sub.enabled=False
        sub.prop(props, "specific_layers", text="Layer(s)")
        layout.operator("gpcurves.bake_gp_curves")
        layout.operator("gpcurves.remove_bake")
        if props.bake_hash:
            layout.label(text="Bake Hash : %s"% props.bake_hash)
        else:
            layout.label(text="No bake")

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
        props = ob.data.gpcurves_curve_props
        if not props.bake_hash:
            self.layout.prop(props, "is_gpcurves", text="")
        else:
            self.layout.label(text="", icon="OUTLINER_OB_GREASEPENCIL")

    def draw(self, context):
        ob = context.object
        props = ob.data.gpcurves_curve_props

        layout = self.layout
        if props.is_gpcurves or props.bake_hash:
            layout.active

        if props.bake_hash:
            layout.label(text="Baked from : %s" % props.gp.name)
            layout.label(text="Hash : %s" % props.bake_hash)
            return
        layout.prop(props, "gp", text="GP Datas")
        layout.prop(props, "layer_mode", text="Mode")
        sub=layout.row(align=True)
        if not props.layer_mode=="SPECIFICS":
            sub.enabled=False
        sub.prop(props, "specific_layers", text="Layer(s)")
        sub.operator("gpcurves.add_layer_menu_caller", text="", icon="ADD")


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