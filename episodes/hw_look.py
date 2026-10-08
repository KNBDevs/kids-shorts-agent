import bpy
from stage import sky_m, sun, w

TREES = [(0.86, 0.45, 0.16), (0.72, 0.3, 0.14), (0.92, 0.66, 0.22), (0.58, 0.55, 0.26), (0.82, 0.4, 0.22), (0.95, 0.72, 0.32)]


def _base(m, rgb):
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*rgb, 1)


def autumn(dusk=False):
    k = 0
    for m in bpy.data.materials:
        if m.name.startswith('tree'):
            _base(m, TREES[k % len(TREES)])
            k += 1
        elif m.name.startswith('ground'):
            _base(m, (0.55, 0.62, 0.36) if not dusk else (0.42, 0.48, 0.32))
        elif m.name.startswith('stage_ring'):
            _base(m, (0.5, 0.28, 0.52))
        elif m.name == 'stage':
            _base(m, (1.0, 0.92, 0.8))
    r = sky_m.node_tree.nodes['Color Ramp'].color_ramp
    if dusk:
        r.elements[0].color = (0.98, 0.62, 0.5, 1)
        r.elements[1].color = (0.24, 0.26, 0.58, 1)
        sun.data.energy = 2.0
        sun.data.color = (1.0, 0.8, 0.66)
        w.node_tree.nodes['Background'].inputs[0].default_value = (0.45, 0.45, 0.75, 1)
    else:
        r.elements[0].color = (1.0, 0.76, 0.56, 1)
        r.elements[1].color = (0.42, 0.56, 0.92, 1)
        sun.data.energy = 2.8
        sun.data.color = (1.0, 0.88, 0.74)
        w.node_tree.nodes['Background'].inputs[0].default_value = (0.75, 0.7, 0.8, 1)
