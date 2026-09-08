#!/usr/bin/env python3
"""Blender script: build the tractor-trailer from content/truck_layout.json.

Run headless:
    blender --background --python scripts/generate_truck.py -- --out build/

Produces build/truck.glb and build/truck_manifest.json. Every inspectable part is a
separate object named part_<item_id> with a collider child col_<item_id>.

The layout is pre-computed -- do not hand-place geometry. To move a part, edit
scripts/build_truck_layout.py and regenerate.
"""
import json, math, os, sys

try:
    import bpy, bmesh                      # noqa: F401
except ImportError:
    sys.exit("Run inside Blender:\n"
             "  blender --background --python scripts/generate_truck.py -- --out build/")

ROOT = os.path.expanduser("~/Projects/PreTripCoach")
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[argv.index("--out") + 1] if "--out" in argv else f"{ROOT}/build"
os.makedirs(OUT, exist_ok=True)

L = json.load(open(f"{ROOT}/content/truck_layout.json"))
REF = L["reference"]

# ── helpers ─────────────────────────────────────────────────────────────────
_mats = {}
def mat(hexcol):
    if hexcol in _mats:
        return _mats[hexcol]
    m = bpy.data.materials.new(hexcol)
    m.use_nodes = True
    r, g, b = (int(hexcol[i:i+2], 16) / 255 for i in (1, 3, 5))
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (lin(r), lin(g), lin(b), 1)
    bsdf.inputs["Roughness"].default_value = 0.65
    _mats[hexcol] = m
    return m

def clear():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for c in (bpy.data.meshes, bpy.data.materials):
        for b in list(c):
            c.remove(b)

def box(name, pos, size, color, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    o = bpy.context.object
    o.name = name
    o.scale = tuple(s if s > 0 else 0.01 for s in size)
    o.rotation_euler = tuple(math.radians(a) for a in rot)
    o.data.materials.append(mat(color))
    return o

def cyl(name, pos, size, color, rot=(0, 0, 0), verts=16):
    r, h = size[0], size[1]
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=pos)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = tuple(math.radians(a) for a in rot)
    o.data.materials.append(mat(color))
    return o

def sphere(name, pos, size, color):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8,
                                         radius=size[0], location=pos)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(mat(color))
    return o

def collider(parent, pid):
    """Simple box collider child, slightly inflated for comfortable tapping."""
    d = parent.dimensions
    bpy.ops.mesh.primitive_cube_add(size=1, location=parent.location)
    c = bpy.context.object
    c.name = f"col_{pid}"
    c.scale = (max(d.x, 0.08) * 1.35, max(d.y, 0.08) * 1.35, max(d.z, 0.08) * 1.35)
    c.parent = parent
    c.matrix_parent_inverse = parent.matrix_world.inverted()
    c.display_type = "WIRE"
    c.hide_render = True
    return c

# ── vehicle shell (context, not inspectable) ────────────────────────────────
def shell():
    W, HW = REF["width"], REF["width"] / 2
    steel, tyre, alu, white = "#8A8F98", "#1A1C1F", "#B9BEC6", "#E8E8E6"

    box("body_hood", (1.05, 0, 1.42), (2.10, W - 0.10, 0.64), "#1D6A4A")
    box("body_bumper", (-0.10, 0, 0.72), (0.22, W, 0.34), steel)
    box("body_cab", (3.35, 0, 2.10), (2.40, W, 1.90), "#1D6A4A")
    box("body_roof_fairing", (3.90, 0, 3.35), (1.40, W - 0.14, 0.60), white)
    box("body_catwalk", (5.10, 0, 1.16), (0.95, 1.10, 0.05), steel)
    for side in (1, -1):
        box(f"body_frame_{'l' if side > 0 else 'r'}",
            (3.60, side * 0.46, 1.02), (6.60, 0.09, 0.24), steel)
        box(f"body_step_{'l' if side > 0 else 'r'}",
            (2.95, side * 1.22, 0.62), (0.55, 0.30, 0.05), steel)

    def wheel(tag, x, y, r=0.535, w=0.295):
        cyl(f"wheel_{tag}", (x, y, r), (r, w), tyre, rot=(90, 0, 0))
        cyl(f"rim_{tag}",   (x, y + 0.02, r), (r * 0.55, w * 0.7), alu, rot=(90, 0, 0))

    for side in (1, -1):
        s = "l" if side > 0 else "r"
        wheel(f"steer_{s}", REF["steer_axle_x"], side * 1.16)
        for i, ax in enumerate(REF["drive_axles_x"]):
            wheel(f"drive{i}_{s}_i", ax, side * 0.98, 0.525)
            wheel(f"drive{i}_{s}_o", ax, side * 1.31, 0.525)
        for i, ax in enumerate(REF["trailer_tandems_x"]):
            wheel(f"trl{i}_{s}_i", ax, side * 0.98, 0.525)
            wheel(f"trl{i}_{s}_o", ax, side * 1.31, 0.525)

    tn, te = REF["trailer_nose_x"], REF["trailer_end_x"]
    tf, tt = REF["trailer_floor_z"], REF["trailer_top_z"]
    box("body_trailer", ((tn + te) / 2, 0, (tf + tt) / 2), (te - tn, W, tt - tf), white)
    box("body_trailer_underride", (te - 0.10, 0, 0.55), (0.10, 1.90, 0.14), steel)

# ── build ───────────────────────────────────────────────────────────────────
def main():
    clear()
    shell()
    manifest, tri_est = [], 0

    for p in L["parts"]:
        pid, prim, pos, size = p["id"], p["primitive"], p["position"], p["size"]
        variants = [(pid, pos)]
        if p.get("mirror_y") and abs(pos[1]) > 1e-6:
            variants.append((f"{pid}_r", [pos[0], -pos[1], pos[2]]))

        for name, pp in variants:
            if prim == "box":
                o = box(name, pp, size, p["color"], p["rotation_deg"])
            elif prim == "cylinder":
                o = cyl(name, pp, size, p["color"], p["rotation_deg"])
            else:
                o = sphere(name, pp, size, p["color"])
            collider(o, name.replace("part_", "").replace("ctrl_", ""))
            tri_est += len(o.data.polygons) * 2
            manifest.append({
                "id": name, "station": p["station"],
                "position": [round(v, 3) for v in pp],
                "bounds": [round(v, 3) for v in o.dimensions],
                "note": p["note"],
            })

    json.dump({"generated_from": "content/truck_layout.json",
               "stations": L["stations"],
               "procedures_no_geometry": L["procedures_no_geometry"],
               "parts": manifest},
              open(f"{OUT}/truck_manifest.json", "w"), indent=1)

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.export_scene.gltf(filepath=f"{OUT}/truck.glb", export_format="GLB",
                              export_yup=True, export_apply=True)

    total = sum(len(o.data.polygons) * 2 for o in bpy.data.objects
                if o.type == "MESH" and not o.name.startswith("col_"))
    print(f"\nexported {OUT}/truck.glb")
    print(f"  named parts   : {len(manifest)}")
    print(f"  objects       : {len(bpy.data.objects)}")
    print(f"  triangles     : ~{total}  (budget 80,000)")
    print(f"  stations      : {len(L['stations'])}")
    if total > 80000:
        print("  WARNING over budget -- reduce cylinder vert counts")

if __name__ == "__main__":
    main()
