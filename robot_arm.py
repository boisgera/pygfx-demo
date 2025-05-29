# Python Standard Library
import copy
import time

# Third-party Libraries
import numpy as np
import pygfx as gfx
import pylinalg as la
import rendercanvas.auto


class Timer:
    def __init__(self):
        self._t0 = None
        self._t = None

    def __call__(self):
        if self._t0 is None:
            self._t0 = time.perf_counter()
            self._t = self._t0
        t = time.perf_counter()
        self._t, dt = t, t - self._t
        return self._t - self._t0, dt


timer = Timer()

environment = gfx.Group().add(
    gfx.Background.from_color("#ffffff"),
    gfx.Grid(
        orientation="xy",
        material=gfx.GridMaterial(
            major_step=1.0,
            thickness_space="world",
            major_thickness=0.005,
            major_color="#000000",
            infinite=True,
        ),
    ),
)


def light(target):
    directional_light = gfx.DirectionalLight(intensity=3.0, target=target)
    directional_light.local.position = [-10.0, -10.0, 0.5]
    return gfx.Group().add(
        gfx.AmbientLight(intensity=2.0),
        directional_light,
    )


axe_1 = gfx.load_mesh("models/axe.stl")[0]
axe_1.material = gfx.MeshPhongMaterial(color="#53565A")
axe_2 = gfx.load_mesh("models/axe.stl")[0]
axe_2.material = gfx.MeshPhongMaterial(color="#d3d3d3")
axe_2.local.scale = 0.99 # avoid z-fighting

axe_2.local.position = [1.0, 0.0, 0.0]

arm = gfx.Group().add(
    axe_1,
    axe_2,
)

n = 1000
positions = np.zeros((n, 3)) + np.array([2.0, 0.0, 0.25])
positions = positions.astype(np.float32)
line = gfx.Line(
    gfx.Geometry(positions=positions),
    gfx.LineSegmentMaterial(
        thickness=5.0, 
        color=[0.0, 0.7, 0.3, 1.0],
    ),
)

def camera():
    camera = gfx.OrthographicCamera()
    camera.local.position = [0.0, 0.0, 4.0]
    camera.show_pos(arm, up=[0, 1.0, 0.0])
    return camera


def update():
    t, _ = timer()

    T = 5.0
    angle_1 = 2 * np.pi * (t / T)
    angle_2 = 2 * np.pi * (t / T)

    arm.local.rotation = la.quat_from_axis_angle([0.0, 0.0, 1.0], angle_1)
    axe_2.local.rotation = la.quat_from_axis_angle([0.0, 0.0, 1.0], angle_2)

    position = positions[-1]
    new_position = [
        np.cos(angle_1) + np.cos(angle_1 + angle_2),
        np.sin(angle_1) + np.sin(angle_1 + angle_2),
        0.025,
    ]

    # If we add a single new position for the line, dashed lines
    # will apper. Therefore we interpolate the old and new positions
    # and add 10 new positions instead.
    offset = 10
    positions[:-offset] = positions[offset:]
    s = np.linspace(0.0, 1.0, offset)
    delta = new_position - position
    positions[-offset:] = position + np.einsum("i,j->ij", s, delta)

    line.geometry.positions.set_data(positions)

scene = gfx.Scene().add(
    environment,
    light(target=arm),
    arm,
    line,
)

canvas = rendercanvas.auto.RenderCanvas(title="Robotic Arm")
renderer = gfx.renderers.WgpuRenderer(canvas)

gfx.show(
    scene,
    renderer=renderer,
    camera=camera(),
    after_render=update,
)