# Python Standard Library
import time

# Third-party Libraries
import numpy as np
import scipy.integrate
import pygfx as gfx
import pylinalg as la
import rendercanvas.auto

m = 1.0
l = 1.0
b = 0.1
g = 10.0

def fun(t, theta_dtheta):
    theta, dtheta = theta_dtheta
    d2theta = - b / m * dtheta - g / l * np.sin(theta)
    return np.array([dtheta, d2theta])


_, tf = t_span = 0.0, 60.0
y0 = np.array([np.pi - 0.1, 0.0])

y = scipy.integrate.solve_ivp(
        fun=fun,
        y0=y0,
        t_span=t_span,
        dense_output = True,
    ).sol


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
        orientation="xz",
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


axe = gfx.load_mesh("models/axe.stl")[0]
axe.material = gfx.MeshPhongMaterial(color="#53565A")
axe.local.rotation = la.quat_from_axis_angle([1.0, 0.0, 0.0], np.pi / 2)
axe.local.rotation = la.quat_mul(
    la.quat_from_axis_angle([0.0, 1.0, 0.0], np.pi / 2), axe.local.rotation
)

mass = gfx.Mesh(
    gfx.sphere_geometry(radius=0.15),
    gfx.MeshPhongMaterial(color="#53565A"),
)
mass.local.position = [1.0, 0.0, 0.0]

axe.add(mass)

pendulum = gfx.Group().add(axe)

pendulum.local.position = [0.0, 0.0, 1.0]

text = gfx.Text(
    text="",
    text_align="center",
    font_size=0.2,
    material=gfx.TextMaterial(color="#000"),
)
text.local.position = [0.0, 0.0, 2.25]
text.local.rotation = la.quat_from_axis_angle([1.0, 0.0, 0.0], np.pi / 2)

def camera():
    camera = gfx.OrthographicCamera()
    camera.local.position = [0.0, -3.0, 1.0]
    camera.show_pos(pendulum, up=[0, 1.0, 1.0])
    return camera


def update():
    t, _ = timer()
    theta, dtheta = y(t)
    _ = dtheta
    if t <= tf:
        pendulum.local.rotation = la.quat_from_axis_angle([0.0, -1.0, 0.0], theta)
        text.set_text(f"t = {t:04.1f}")

scene = gfx.Scene().add(
    environment,
    light(target=pendulum),
    pendulum,
    text,
)

canvas = rendercanvas.auto.RenderCanvas(title="Pendulum")
renderer = gfx.renderers.WgpuRenderer(canvas)

gfx.show(
    scene,
    renderer=renderer,
    camera=camera(),
    after_render=update,
)
