import bpy
from bpy.app.handlers import persistent
import time


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

def get_layer_list(props, gp_object):
    # Create layer list
    layer_list=[]
    if props.layer_mode=="ALL":
        layer_list=gp_object.layers
    elif props.layer_mode=="VISIBLE":
        for layer in gp_object.layers:
            if not layer.hide:
                layer_list.append(layer)
    elif props.layer_mode=="SPECIFICS":
        specifics=props.specific_layers.split(",")
        for layer in gp_object.layers:
            if layer.info in specifics:
                layer_list.append(layer)
    
    return layer_list

def create_curves_from_gp_active_frame(curve_object, gp_object, frame):
    remove_existing_splines(curve_object)

    layer_list=get_layer_list(curve_object.data.gpcurves_curve_props, gp_object)

    # Create splines
    for layer in layer_list:
        if layer.active_frame is not None:
            for stroke in layer.active_frame.strokes:
                create_spline_from_stroke(curve_object, stroke)
                curve_object.update_tag()


@persistent
def gp_curve_handler(scene):
    start=time.time()
    for ob in scene.objects:
        if ob.type=="CURVE":
            props=ob.data.gpcurves_curve_props
            if props.is_gpcurves and not props.bake_hash:
                if props.gp:
                    print(f"GP CURVES --- frame {scene.frame_current} : curving from {props.gp.name} to {ob.name}")
                    create_curves_from_gp_active_frame(ob, props.gp, scene.frame_current)
    end=time.time()
    exec_time=end-start
    print(f"GP CURVES --- handler executed in : {exec_time}")

@persistent
def gp_curve_startup_handler(scene):
    if bpy.context.scene.gpcurves_scene_props.gpcurves_process:
        bpy.app.handlers.depsgraph_update_post.append(gp_curve_handler)
        bpy.app.handlers.frame_change_post.append(gp_curve_handler)
        print("GPCURVES --- Setting gpcurves handlers ON")

@persistent
def gp_curve_quit_handler(scene):
    for handler in bpy.app.handlers.depsgraph_update_post:
        if "gp_curve_handler"==handler.__name__:
            bpy.app.handlers.depsgraph_update_post.remove(gp_curve_handler)
            print("GPCURVES --- Removing depsgraph gpcurves handler")
            break
    for handler in bpy.app.handlers.frame_change_post:
        if "gp_curve_handler"==handler.__name__:
            bpy.app.handlers.frame_change_post.remove(gp_curve_handler)
            print("GPCURVES --- Removing frame change gpcurves handlers")
            break

### REGISTER ---

def register():
    bpy.app.handlers.load_post.append(gp_curve_startup_handler)
    bpy.app.handlers.load_pre.append(gp_curve_quit_handler)

def unregister():
    bpy.app.handlers.load_post.remove(gp_curve_startup_handler)
    bpy.app.handlers.load_pre.remove(gp_curve_quit_handler)
