import bpy
from bpy.app.handlers import persistent
import time

from .preferences import get_addon_preferences

def get_addon_version(name="GP Curves"):
    import addon_utils
    for addon in addon_utils.modules()[:]:
        if addon.bl_info['name']==name:
            return addon.bl_info.get('version')
    return None

version=get_addon_version()

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
                # print(f"Updating {layer.info}") #DEBUG
                # layer.frames.update()
                layer_list.append(layer)
    elif props.layer_mode=="SPECIFICS":
        specifics=props.specific_layers.split(",")
        for layer in gp_object.layers:
            if layer.info in specifics:
                # print(f"Updating {layer.info}") #DEBUG
                # layer.frames.update()
                layer_list.append(layer)
    
    return layer_list

def create_curves_from_gp_active_frame(curve_object, gp_object, frame, debug=False):
    stroke_list=[]
    chk_frame=False

    if debug: #DEBUG
        print(f"GPCURVES --- Getting layers for {gp_object.name}") #DEBUG

    layer_list=get_layer_list(curve_object.data.gpcurves_curve_props, gp_object)

    # Create splines
    for layer in layer_list:
        # print(f"Updating {layer.info}") #DEBUG
        # layer.frames.update()
        for f in reversed(layer.frames):
            if f.frame_number<=frame:
                chk_frame=True
                if debug: #DEBUG
                    print(f"GPCURVES --- Active GP Frame for {layer.info} : {f.frame_number}") #DEBUG
                for stroke in f.strokes:
                    stroke_list.append(stroke)
                break

    remove_existing_splines(curve_object)

    if chk_frame:
        if debug: #DEBUG
            print(f"GPCURVES --- Removing splines from {curve_object.name}") #DEBUG
        if debug: #DEBUG
            print("GPCURVES --- Creating strokes") #DEBUG
        for stroke in stroke_list:
            create_spline_from_stroke(curve_object, stroke)
        curve_object.update_tag()

        # if layer.active_frame is not None:
        #     print(f"--- {layer.info} : frame{layer.active_frame.frame_number}") #DEBUG
        #     for stroke in layer.active_frame.strokes:
        #         print(f"Creating {stroke}") #DEBUG
        #         create_spline_from_stroke(curve_object, stroke)
        #         curve_object.update_tag()

def get_gp_linked_curves(scene):
    curve_list=[]
    for ob in scene.objects:
        if ob.type=="CURVE":
            props=ob.data.gpcurves_curve_props
            if props.is_gpcurves and not props.bake_hash:
                if props.gp:
                    curve_list.append(ob)
    return curve_list

@persistent
def framechange_handler(scene):
    scn=bpy.context.scene
    debug=get_addon_preferences().debug

    if debug: #DEBUG
        start=time.perf_counter() #DEBUG
        print() #DEBUG
        print(f"GPCURVES ------ FRAME HANDLER ------ v{version}") #DEBUG

    for ob in get_gp_linked_curves(scn):
        props=ob.data.gpcurves_curve_props
        if debug: #DEBUG
            print(f"GPCURVES --- frame {scn.frame_current} : curving from {props.gp.name} to {ob.name}") #DEBUG
        create_curves_from_gp_active_frame(ob, props.gp, scn.frame_current, debug)

    if debug: #DEBUG
        end=time.perf_counter() #DEBUG
        print(f"GPCURVES --- handler executed in {end-start:0.8f} s") #DEBUG
        print() #DEBUG

@persistent
def depsgraph_handler(scene):
    context=bpy.context
    scn=context.scene
    debug=get_addon_preferences().debug

    if debug: #DEBUG
        start=time.perf_counter() #DEBUG
        print() #DEBUG
        print(f"GPCURVES ------ DEPSGRAPH HANDLER ------ v{version}") #DEBUG

    chk_handler=False
    if context.active_object:
        if context.active_object.type=="GPENCIL"\
        and context.mode!="OBJECT":
            for ob in get_gp_linked_curves(scn):
                props=ob.data.gpcurves_curve_props
                if props.gp==context.active_object.data:
                    chk_handler=True
                    if debug: #DEBUG
                        print(f"GPCURVES --- frame {scn.frame_current} : curving from {props.gp.name} to {ob.name}") #DEBUG
                    create_curves_from_gp_active_frame(ob, props.gp, scn.frame_current, debug)
                    break

    if debug: #DEBUG
        end=time.perf_counter() #DEBUG
        if chk_handler: #DEBUG
            print(f"GPCURVES --- handler executed in {end-start:0.8f} s") #DEBUG
        else: #DEBUG
            print(f"GPCURVES --- No valid object, handler aborted in {end-start:0.8f} s") #DEBUG
        print() #DEBUG

@persistent
def render_init_handler(scene):
    scn=bpy.context.scene
    debug=get_addon_preferences().debug

    if debug: #DEBUG
        start=time.perf_counter() #DEBUG
        print() #DEBUG
        print(f"GPCURVES ------ RENDER INIT HANDLER ------ v{version}") #DEBUG

    for handler in bpy.app.handlers.depsgraph_update_post:
        if "depsgraph_handler"==handler.__name__:
            bpy.app.handlers.depsgraph_update_post.remove(depsgraph_handler)
            print("GPCURVES --- Removing depsgraph_update_post handler")
            break

    if debug: #DEBUG
        end=time.perf_counter() #DEBUG
        print(f"GPCURVES --- Render init handler executed in {end-start:0.8f} s") #DEBUG
        print() #DEBUG

@persistent
def render_end_handler(scene):
    scn=bpy.context.scene
    debug=get_addon_preferences().debug

    if debug: #DEBUG
        start=time.perf_counter() #DEBUG
        print() #DEBUG
        print(f"GPCURVES ------ RENDER END HANDLER ------ v{version}") #DEBUG

    bpy.app.handlers.depsgraph_update_post.append(depsgraph_handler)
    print("GPCURVES --- Setting depsgraph handler")

    if debug: #DEBUG
        end=time.perf_counter() #DEBUG
        print(f"GPCURVES --- Render end handler executed in {end-start:0.8f} s") #DEBUG
        print() #DEBUG

def set_handlers():
    bpy.app.handlers.frame_change_post.append(framechange_handler)
    print("GPCURVES --- Setting frame change handler")
    bpy.app.handlers.depsgraph_update_post.append(depsgraph_handler)
    print("GPCURVES --- Setting depsgraph handler")
    bpy.app.handlers.render_init.append(render_init_handler)
    print("GPCURVES --- Setting render_init handler")
    bpy.app.handlers.render_complete.append(render_end_handler)
    print("GPCURVES --- Setting render_complete handler")
    bpy.app.handlers.render_cancel.append(render_end_handler)
    print("GPCURVES --- Setting render_cancel handler")

def remove_handlers():
    for handler in bpy.app.handlers.frame_change_post:
        if "framechange_handler"==handler.__name__:
            bpy.app.handlers.frame_change_post.remove(framechange_handler)
            print("GPCURVES --- Removing frame_change_post handler")
            break
    for handler in bpy.app.handlers.depsgraph_update_post:
        if "depsgraph_handler"==handler.__name__:
            bpy.app.handlers.depsgraph_update_post.remove(depsgraph_handler)
            print("GPCURVES --- Removing depsgraph_update_post handler")
            break
    for handler in bpy.app.handlers.render_init:
        if "render_init_handler"==handler.__name__:
            bpy.app.handlers.render_init.remove(render_init_handler)
            print("GPCURVES --- Removing render_init handler")
            break
    for handler in bpy.app.handlers.render_complete:
        if "render_end_handler"==handler.__name__:
            bpy.app.handlers.render_complete.remove(render_end_handler)
            print("GPCURVES --- Removing render_complete handler")
            break
    for handler in bpy.app.handlers.render_cancel:
        if "render_end_handler"==handler.__name__:
            bpy.app.handlers.render_cancel.remove(render_end_handler)
            print("GPCURVES --- Removing render_cancel handler")
            break

@persistent
def load_post_handler(scene):
    if bpy.context.scene.gpcurves_scene_props.gpcurves_process:
        set_handlers()

@persistent
def load_pre_handler(scene):
    if bpy.context.scene.gpcurves_scene_props.gpcurves_process:
        remove_handlers()

### REGISTER ---

def register():
    bpy.app.handlers.load_post.append(load_post_handler)
    bpy.app.handlers.load_pre.append(load_pre_handler)

def unregister():
    bpy.app.handlers.load_post.remove(load_post_handler)
    bpy.app.handlers.load_pre.remove(load_pre_handler)
