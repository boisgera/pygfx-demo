# Python Standard Library
import time

# Third-party Libraries
import numpy as np
import pygfx as gfx
import pylinalg as la
import rendercanvas.auto


class Timer:
    def __init__(self):
        self._t = None

    def __call__(self):
        if self._t is None:
            self._t = time.perf_counter()
        t = time.perf_counter()
        self._t, dt = t, t - self._t
        return self._t, dt


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


cube = gfx.Mesh(
    gfx.box_geometry(1.0, 1.0, 1.0),
    gfx.MeshPhongMaterial(color="#336699"),
)


def camera():
    camera = gfx.PerspectiveCamera(fov=70, aspect=16 / 9)
    camera.local.position = [-3.0, -3.0, 3.0]
    camera.show_pos(cube, up=[0, 0, 1.0])
    return camera


def update():
    t, dt = timer()

    T = 5.0
    angle = 2 * np.pi * (t / T)
    delta_angle = 2 * np.pi * (dt / T)

    cube.local.position = [0.0, 0.0, 0.5 + 0.5 * (1.0 + np.sin(angle))]

    rot = la.quat_from_axis_angle([0.0, 0.0, 1.0], delta_angle)
    cube.local.rotation = la.quat_mul(rot, cube.local.rotation)


scene = gfx.Scene().add(
    environment,
    light(target=cube),
    cube,
)

canvas = rendercanvas.auto.RenderCanvas(title="Flying Cube")
renderer = gfx.renderers.WgpuRenderer(canvas)

gfx.show(
    scene,
    renderer=renderer,
    camera=camera(),
    before_render=update,
)