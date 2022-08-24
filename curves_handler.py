import bpy
from bpy.app.handlers import persistent


def remove_existing_splines(curve_object):
    for spline in curve_object.data.splines:
        curve_object.data.splines.remove(spline)

def create_spline_from_stroke(curve_object, stroke):
    # Create spline
    spline=curve_object.data.splines.new("POLY")
    # Add points
    spline.points.add(len(stroke.points)-1)
    # Place points
    n=0
    for point in stroke.points:
        spline.points[n].co=(*point.co, 1)
        n+=1

def get_layer_list(curve_object, gp_object):
    curve_props=curve_object.data.gpcurves_props

    # Create layer list
    layer_list=[]
    if curve_props.layer_mode=="ALL":
        layer_list=gp_object.layers
    elif curve_props.layer_mode=="ALL_RENDERED":
        for layer in gp_object.layers:
            if not layer.hide:
                layer_list.append(layer)
    elif curve_props.layer_mode=="SPECIFIC":
        specifics=curve_props.specific_layers.split(",")
        for layer in gp_object.layers:
            if layer.info in specifics:
                layer_list.append(layer)
    
    return layer_list

def create_curves_from_gp_active_frame(curve_object, gp_object):
    remove_existing_splines(curve_object)

    layer_list=get_layer_list(curve_object, gp_object)

    # Create splines
    for layer in layer_list:
        if layer.active_frame is not None:
            for stroke in layer.active_frame.strokes:
                create_spline_from_stroke(curve_object, stroke)
                curve_object.update_tag()


@persistent
def gp_curve_handler(scene):
    for ob in scene.objects:
        if ob.type=="CURVE":
            props=ob.data.gpcurves_props
            if props.is_gpcurves:
                if props.gp:
                    print("curving from %s to %s" % (props.gp.name, ob.name))
                    create_curves_from_gp_active_frame(ob, props.gp)



### REGISTER ---

def register():
    bpy.app.handlers.depsgraph_update_post.append(gp_curve_handler)
    bpy.app.handlers.frame_change_post.append(gp_curve_handler)

def unregister():
    bpy.app.handlers.depsgraph_update_post.remove(gp_curve_handler)
    bpy.app.handlers.frame_change_post.remove(gp_curve_handler)