import bpy
import random

from . import curves_handler as c_h

bake_name="GP_Curves_Bake"

def generate_random():
    return(str(random.randrange(0,99999)).zfill(5))

def create_curve_object(name, collection):
    datas=bpy.data
    # Create curve data
    new_curve=datas.curves.new(name, "CURVE")
    # Create object
    new_object=datas.objects.new(name, new_curve)
    # Link to collection
    collection.objects.link(new_object)
    return new_object

def create_hide_keyframes(ob, hide, group):
    ob.hide_viewport=ob.hide_render=hide
    ob.keyframe_insert(
        data_path='hide_viewport',
        group=group,
    )
    ob.keyframe_insert(
        data_path='hide_render',
        group=group,
    )

def bake_gp_to_curves(gp_datas, target_coll, scene):
    gp_name=gp_datas.name
    props=gp_datas.gpcurves_gp_props
    old_frame=scene.frame_current

    layer_list=c_h.get_layer_list(props, gp_datas)

    # Per layer
    for layer in layer_list:
        ob_base_name="%s_%s" % (gp_name, layer.info)

        previous_object=None

        for frame in layer.frames:
            ob_name="%s_%s" % (ob_base_name, str(frame.frame_number).zfill(5))
            new_object=create_curve_object(ob_name, target_coll)

            curve_props=new_object.data.gpcurves_curve_props
            curve_props.bake_hash=props.bake_hash
            curve_props.gp=gp_datas

            for stroke in frame.strokes:
                c_h.create_spline_from_stroke(new_object, stroke)

            # Keyframe start
            if frame.frame_number>scene.frame_start:
                scene.frame_current=scene.frame_start
            create_hide_keyframes(new_object, True, bake_name)

            # Keyframe Previous object
            scene.frame_current=frame.frame_number
            if previous_object:
                create_hide_keyframes(previous_object, True, bake_name)
            
            # Keyframe end
            create_hide_keyframes(new_object, False, bake_name)
            previous_object=new_object

    scene.frame_current=old_frame

def remove_bake(hash):
    for ob in bpy.data.objects:
        if ob.type=="CURVE":
            if ob.data.gpcurves_curve_props.bake_hash==hash:
                bpy.data.objects.remove(ob, do_unlink=True)

def remove_collection_if_empty(coll):
    if not coll.objects:
        bpy.data.collections.remove(coll)
        return True
    return False

def create_collection(name, scene):
    coll=bpy.data.collections.new(name)
    scene.collection.children.link(coll)
    return coll

class GPCURVES_OT_bake_gp_curves(bpy.types.Operator):
    bl_idname = "gpcurves.bake_gp_curves"
    bl_label = "Bake GP to Curves"
    bl_options = {'REGISTER','UNDO','INTERNAL'}

    collection_mode: bpy.props.EnumProperty(
            name="Collection Mode",
            items=(
                ('NEW', 'Create New Collection', ""),
                ('EXISTING', 'Use Existing Collection', ""),
                ),
        )
    new_collection_name: bpy.props.StringProperty(name="New Collection Name")
    remove_previous_collection: bpy.props.BoolProperty(name="Remove Previous Collection if Empty", default=True)

    layer_mode: bpy.props.EnumProperty(
        name="Layer Mode",
        items=(
            ('ALL', 'All GP Layers', ""),
            ('VISIBLE', 'Only Visible GP Layers', ""),
            ('SPECIFICS', 'Specific(s) GP layer(s)', ""),
            ),
    )

    temp_hash=""
    temp_name=""

    old_layers=None

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type == 'GPENCIL'

    def invoke(self, context, event):
        ob = context.object
        props = ob.data.gpcurves_gp_props

        props.temp_bake_collection=props.bake_collection
        props.temp_specific_layers=props.specific_layers

        self.temp_hash=generate_random()
        self.temp_name=self.new_collection_name="%s_%s_%s" % (bake_name, ob.name, self.temp_hash)
        
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        ob = context.object
        props = ob.data.gpcurves_gp_props

        layout = self.layout

        if props.bake_hash and props.bake_collection:
            box=layout.box()
            col=box.column(align=True)
            col.label(text="Previous Bake to remove", icon="INFO")
            col.label(text="Hash : %s" % props.bake_hash)
            col.label(text="Collection : %s" % props.bake_collection.name)
            sub=col.row()
            if self.collection_mode=="EXISTING" and props.temp_bake_collection==props.bake_collection:
                sub.enabled=False
            sub.prop(self, "remove_previous_collection")

        layout.separator()

        layout.prop(self, "collection_mode", text="")
        if self.collection_mode=="NEW":
            layout.prop(self, "new_collection_name", text="", icon="COLLECTION_NEW")
        else:
            layout.prop(props, "temp_bake_collection", text="")

        layout.separator()

        layout.prop(self, "layer_mode", text="Mode")
        sub=layout.row(align=True)
        if not self.layer_mode=="SPECIFICS":
            sub.enabled=False
        sub.prop(props, "temp_specific_layers", text="Layer(s)")
        sub.operator("gpcurves.add_layer_menu_caller", text="", icon="ADD")

    def execute(self, context):
        ob = context.object
        scn = context.scene
        props = ob.data.gpcurves_gp_props

        # Remove previous
        if props.bake_hash:
            remove_bake(props.bake_hash)
        if self.remove_previous_collection:
            if props.bake_hash and props.bake_collection:
                if self.collection_mode!="EXISTING"\
                or props.bake_collection!=props.temp_bake_collection:
                    remove_collection_if_empty(props.bake_collection)

        # Pass new properties
        props.bake_collection=props.temp_bake_collection
        props.layer_mode=self.layer_mode
        props.specific_layers=props.temp_specific_layers

        # New hash
        props.bake_hash=self.temp_hash

        # Create new coll if needed
        if self.collection_mode=="NEW":
            if not self.new_collection_name:
                name=self.temp_name
            else:
                name=self.new_collection_name
            coll=create_collection(self.new_collection_name, context.scene)
            props.bake_collection=coll
        else:
            coll=props.bake_collection
        bake_gp_to_curves(ob.data, coll, scn)

        return {'FINISHED'}


class GPCURVES_OT_update_bake(bpy.types.Operator):
    bl_idname = "gpcurves.update_bake"
    bl_label = "Update Existing Bake"
    bl_options = {'REGISTER','UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        if ob.type == 'GPENCIL':
            if ob.data.gpcurves_gp_props.bake_hash:
                return True

    def execute(self, context):
        ob=context.object
        props=ob.data.gpcurves_gp_props

        remove_bake(props.bake_hash)

        bake_gp_to_curves(ob.data, props.bake_collection, context.scene)

        return {'FINISHED'}


class GPCURVES_OT_remove_bake(bpy.types.Operator):
    bl_idname = "gpcurves.remove_bake"
    bl_label = "Remove Bake"
    bl_options = {'REGISTER','UNDO','INTERNAL'}

    remove_collection: bpy.props.BoolProperty(name="Remove Bake Collection if Empty", default=True)

    @classmethod
    def poll(cls, context):
        ob = context.object
        if ob.type == 'GPENCIL':
            if ob.data.gpcurves_gp_props.bake_hash:
                return True

    def invoke(self, context, event):        
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        ob = context.object
        props = ob.data.gpcurves_gp_props

        layout = self.layout

        layout.label(text="Previous Collection : %s" % props.bake_collection.name)
        layout.prop(self, "remove_collection")
        layout.separator
        layout.label(text="Remove Bake ?")

    def execute(self, context):
        ob=context.object
        props=ob.data.gpcurves_gp_props

        remove_bake(props.bake_hash)

        if self.remove_collection:
            if props.bake_hash and props.bake_collection:
                remove_collection_if_empty(props.bake_collection)

        props.bake_hash=""

        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(GPCURVES_OT_bake_gp_curves)
    bpy.utils.register_class(GPCURVES_OT_update_bake)
    bpy.utils.register_class(GPCURVES_OT_remove_bake)

def unregister():
    bpy.utils.unregister_class(GPCURVES_OT_bake_gp_curves)
    bpy.utils.unregister_class(GPCURVES_OT_update_bake)
    bpy.utils.unregister_class(GPCURVES_OT_remove_bake)