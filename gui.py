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

        layout.operator("gpcurves.bake_gp_curves")
        layout.operator("gpcurves.remove_bake")

        box=layout.box()
        if props.bake_hash:
            col=box.column(align=True)
            row=col.row()
            row.label(text="Previous Bake", icon="INFO")
            row.operator('gpcurves.update_bake', text="", icon="FILE_REFRESH")
            col.label(text="Hash : %s" % props.bake_hash)
            row=col.row(align=True)
            row.label(text="Collection : %s" % props.bake_collection.name)

            row.separator()
            row.prop(props.bake_collection, "hide_select", text="", emboss=False)
            row.prop(props.bake_collection, "hide_viewport", text="", emboss=False)
            row.prop(props.bake_collection, "hide_render", text="", emboss=False)

            if props.object_properties_parent:
                parent = props.object_properties_parent.name
            else:
                parent = "None"
            col.label(text="Parent Object : %s" % parent)
            if props.layer_mode=="ALL":
                layers="All"
            elif props.layer_mode=="VISIBLE":
                layers="Only Visibles"
            else:
                layers=props.specific_layers
            col.label(text="Layers : %s" % layers)
            if props.frame_range=="ALL":
                f_range="All GP Frames"
            elif props.frame_range=="SCENE":
                f_range="Scene Frame Range"
            else:
                f_range="%i - %i" % (props.custom_start_frame, props.custom_end_frame)
            col.label(text="Frame Range : %s" % f_range)
        else:
            box.label(text="No Bake", icon="INFO")

        # sub=layout.row(align=True)
        # if not props.layer_mode=="SPECIFICS":
        #     sub.enabled=False
        # sub.prop(props, "specific_layers", text="Layer(s)")

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
        if props.bake_hash:
            self.layout.label(text="", icon="OUTLINER_OB_GREASEPENCIL")
        else:
            self.layout.prop(props, "is_gpcurves", text="")

    def draw(self, context):
        ob = context.object
        props = ob.data.gpcurves_curve_props

        layout = self.layout
        if not props.is_gpcurves and not props.bake_hash:
            layout.active=False

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