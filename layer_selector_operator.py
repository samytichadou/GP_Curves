import bpy

class GPCURVES_MT_add_layer_menu(bpy.types.Menu):
    bl_label = "Add Specific Layer"
    #bl_idname = "GPCURVES_MT_add_layer_menu"

    def draw(self, context):
        ob = context.object
        props = ob.data.gpcurves_curve_props
        gp = props.gp
        layer_list = props.specific_layers.split(",")

        layout = self.layout
        for layer in gp.layers:
            layer_name = layer.info
            sub=layout.row()
            if layer_name in layer_list:
                sub.enabled=False
            op = sub.operator("gpcurves.add_layer", text=layer_name)
            op.layer_name = layer_name

class GPCURVES_OT_add_layer_menu_caller(bpy.types.Operator):
    bl_idname = "gpcurves.add_layer_menu_caller"
    bl_label = "Add Specific Layer"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        gp = ob.data.gpcurves_curve_props.gp
        return ob and gp

    def execute(self, context):
        bpy.ops.wm.call_menu(name="GPCURVES_MT_add_layer_menu")
        return {'FINISHED'}

class GPCURVES_OT_add_layer(bpy.types.Operator):
    bl_idname = "gpcurves.add_layer"
    bl_label = "Add this Layer"
    bl_options = {'REGISTER','UNDO','INTERNAL'}

    layer_name : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ob = context.object
        props = ob.data.gpcurves_curve_props
        layer_field = props.specific_layers

        if layer_field and not layer_field.strip().endswith(","):
            props.specific_layers += ","

        props.specific_layers += self.layer_name

        context.area.tag_redraw()

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(GPCURVES_MT_add_layer_menu)
    bpy.utils.register_class(GPCURVES_OT_add_layer_menu_caller)
    bpy.utils.register_class(GPCURVES_OT_add_layer)

def unregister():
    bpy.utils.unregister_class(GPCURVES_MT_add_layer_menu)
    bpy.utils.unregister_class(GPCURVES_OT_add_layer_menu_caller)
    bpy.utils.unregister_class(GPCURVES_OT_add_layer)