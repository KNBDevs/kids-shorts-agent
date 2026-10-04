import bpy, sys, os, math
from mathutils import Vector
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import roster

names = [a for a in sys.argv[1:] if a in roster.ROSTER] or list(roster.ROSTER)
out = os.environ.get("OUT", os.path.join(HERE, "inspect")); os.makedirs(out, exist_ok=True)
views = {"front": (0, -1), "left_side": (-1, 0), "back": (0, 1), "three_quarter": (-0.55, -1)}
for name in names:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    w = bpy.data.worlds.new("w"); sc.world = w
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.82, 0.82, 0.83, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.45
    ch = roster.build(name)
    g = bpy.data.materials.new("floor"); g.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.8, 0.81, 1)
    bpy.ops.mesh.primitive_plane_add(size=40); bpy.context.object.data.materials.append(g)
    for loc, rot, e, s in [((-3, -4, 5), (50, 0, -35), 260, 5), ((4, -2, 3), (60, 0, 60), 90, 4), ((0, 5, 4), (-55, 0, 0), 140, 4)]:
        bpy.ops.object.light_add(type="AREA", location=loc, rotation=tuple(math.radians(r) for r in rot))
        bpy.context.object.data.energy = e; bpy.context.object.data.size = s
    hh = ch["height"]
    tgt = bpy.data.objects.new("t", None); sc.collection.objects.link(tgt); tgt.location = (0, 0, hh * 0.5)
    bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam; cam.data.lens = 85
    c = cam.constraints.new("TRACK_TO"); c.target = tgt; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
    r = sc.render; r.engine = "CYCLES"; sc.cycles.samples = 20; sc.cycles.use_denoising = True
    r.resolution_x, r.resolution_y = 480, 560; sc.view_settings.view_transform = "Standard"
    for k, (dx, dy) in views.items():
        v = Vector((dx, dy, 0)).normalized() * (hh * 3.3)
        cam.location = (v.x, v.y, hh * 0.62)
        r.filepath = os.path.join(out, f"{name}_{k}.png")
        bpy.ops.render.render(write_still=True)
    print("DONE", name, flush=True)
