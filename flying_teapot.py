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


meshes = gfx.load_mesh("models/teapot.stl")
teapot = meshes[0]
teapot.material = gfx.MeshPhongMaterial(color="#993333")
teapot.local.scale = 1.0 / 20.0 # sensible given teapot.get_bounding_box()


def camera():
    camera = gfx.PerspectiveCamera(fov=70, aspect=16 / 9)
    camera.local.position = [-3.0, -3.0, 3.0]
    camera.show_pos(teapot, up=[0, 0, 1.0])
    return camera


def update():
    t, dt = timer()

    T = 5.0
    angle = 2 * np.pi * (t / T)
    delta_angle = 2 * np.pi * (dt / T)

    teapot.local.position = [0.0, 0.0, 0.5 + 0.5 * (1.0 + np.sin(angle))]

    rot = la.quat_from_axis_angle([0.0, 0.0, 1.0], delta_angle)
    teapot.local.rotation = la.quat_mul(rot, teapot.local.rotation)


scene = gfx.Scene().add(
    environment,
    light(target=teapot),
    teapot,
)

canvas = rendercanvas.auto.RenderCanvas(title="Flying Teapot")
renderer = gfx.renderers.WgpuRenderer(canvas)

gfx.show(
    scene,
    renderer=renderer,
    camera=camera(),
    before_render=update,
)
