import bpy
import random

from . import curves_handler as c_h

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

def bake_gp_to_curves(gp_datas, target_coll):
    gp_name=gp_datas.name
    props=gp_datas.gpcurves_gp_props

    layer_list=c_h.get_layer_list(props, gp_datas)

    # Per layer
    for layer in layer_list:
        ob_base_name="%s_%s" % (gp_name, layer.info)
        for frame in layer.frames:
            ob_name="%s_%s" % (ob_base_name, str(frame.frame_number).zfill(5))
            new_object=create_curve_object(ob_name, target_coll)

            curve_props=new_object.data.gpcurves_curve_props
            curve_props.bake_hash=props.bake_hash
            curve_props.gp=gp_datas

            for stroke in frame.strokes:
                c_h.create_spline_from_stroke(new_object, stroke)


class GPCURVES_OT_bake_gp_curves(bpy.types.Operator):
    bl_idname = "gpcurves.bake_gp_curves"
    bl_label = "Bake GP to Curves"
    bl_options = {'REGISTER','UNDO','INTERNAL'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type == 'GPENCIL'

    def execute(self, context):
        ob = context.object
        props = ob.data.gpcurves_gp_props
        props.bake_hash=generate_random()
        bake_gp_to_curves(ob.data, props.bake_collection)
        return {'FINISHED'}


### REGISTER ---
def register():
    bpy.utils.register_class(GPCURVES_OT_bake_gp_curves)

def unregister():
    bpy.utils.unregister_class(GPCURVES_OT_bake_gp_curves)