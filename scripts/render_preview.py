"""Render preview images of the generated truck. Blender only.
   blender --background --python scripts/render_preview.py -- --out build/preview
"""
import json, math, os, sys
import bpy

ROOT = os.path.expanduser("~/Projects/PreTripCoach")
argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out")+1] if "--out" in argv else f"{ROOT}/build/preview"
os.makedirs(OUT, exist_ok=True)

bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete()
bpy.ops.import_scene.gltf(filepath=f"{ROOT}/build/truck.glb")

# hide wireframe colliders
for o in bpy.data.objects:
    if o.name.startswith("col_"):
        o.hide_render = True

sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = 1100, 620
sc.render.film_transparent = False
w = bpy.data.worlds.new("w"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.13,0.14,0.16,1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sc.world = w

sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun","SUN"))
sun.data.energy = 4.0; sun.rotation_euler = (math.radians(52), 0, math.radians(38))
sc.collection.objects.link(sun)

cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
sc.collection.objects.link(cam); sc.camera = cam

# aim with a track-to constraint rather than hand-rolled euler math
tgt = bpy.data.objects.new("target", None)
sc.collection.objects.link(tgt)
con = cam.constraints.new("TRACK_TO")
con.target = tgt; con.track_axis = "TRACK_NEGATIVE_Z"; con.up_axis = "UP_Y"

def shot(name, loc, target, lens=38):
    cam.location = loc; cam.data.lens = lens
    tgt.location = target
    bpy.context.view_layer.update()
    sc.render.filepath = f"{OUT}/{name}.png"
    bpy.ops.render.render(write_still=True)
    print("rendered", name)

L = json.load(open(f"{ROOT}/content/truck_layout.json"))
shot("01_full_rig",   (-9.0, 15.0, 7.5),  (10.0, 0, 1.8), lens=52)
shot("02_tractor",    (-4.5,  6.5, 3.2),  (3.0, 0, 1.6))
shot("03_steer_axle", (0.45,  3.35,1.45), (1.35, 1.05,0.72), lens=42)
shot("04_coupling",   (4.25,  2.45,1.05), (5.85, 0.10,1.24), lens=40)
shot("05_trailer_rear",(24.5, 3.5, 2.4),  (20.8, 0, 1.9), lens=45)
