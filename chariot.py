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

def register(event_handler):
    name = event_handler.__name__
    assert name.startswith("on_")
    event_name = name[3:]
    renderer.add_event_handler(event_handler, event_name)
    return event_handler

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


frame = gfx.load_mesh("models/frame.stl")[0]
_wheel_left = gfx.load_mesh("models/wheel.stl")[0]
_wheel_right = gfx.load_mesh("models/wheel.stl")[0]
frame.material = gfx.MeshPhongMaterial(color="#0000ff")

_wheel_left.material = gfx.MeshPhongMaterial(color="#ff0000")
_wheel_left.local.rotation = la.quat_from_axis_angle([-1.0, 0.0, 0.0], np.pi / 2)
_wheel_left.local.position = [0.0, +5.0, 0.0]
wheel_left = gfx.Group().add(_wheel_left)
_wheel_right.material = gfx.MeshPhongMaterial(color="#00ff00")
_wheel_right.local.rotation = la.quat_from_axis_angle([+1.0, -0.0, 0.0], np.pi / 2)
_wheel_right.local.position = [0.0, -5.0, 0.0]
wheel_right = gfx.Group().add(_wheel_right)

_chariot = gfx.Group().add(
    frame,
    wheel_left,
    wheel_right,
)
_chariot.local.position = [0.0, 0.0, 1.0]
chariot = gfx.Group().add(_chariot)
root = chariot

def camera():
    camera = gfx.PerspectiveCamera(fov=70, aspect=16 / 9)
    camera.local.position = [0.0, 0.0, 50.0]
    camera.show_pos(chariot, up=[0, 0, 1.0])
    return camera

omega = 0.0
v = 0.0

def update():
    _, dt = timer()

    v_left = v - omega * 5.0
    omega_left = v_left / 1.0
    v_right = v + omega * 5.0
    omega_right = v_right / 1.0

    wheel_left.local.rotation = la.quat_mul(
        la.quat_from_axis_angle([0.0, 1.0, 0.0], omega_left * dt),
        wheel_left.local.rotation,
    )

    wheel_right.local.rotation = la.quat_mul(
        la.quat_from_axis_angle([0.0, 1.0, 0.0], omega_right * dt),
        wheel_right.local.rotation,
    )

    chariot.local.rotation = la.quat_mul(
        la.quat_from_axis_angle([0.0, 0.0, 1.0], omega * dt),
        chariot.local.rotation,
    )

    axis, angle = la.quat_to_axis_angle(chariot.local.rotation)
    if np.isnan(axis[2]):
        angle = 0.0
    else:
        angle = angle * np.sign(axis[2])

    chariot.local.position = [
        chariot.local.position[0] + v * dt * np.cos(angle),
        chariot.local.position[1] + v * dt * np.sin(angle),
        chariot.local.position[2],
    ]

text = gfx.Text(
    text = "Use the arrow keys to control the chariot",
    font_size=3.0,
    material=gfx.TextMaterial(color="#000"),
    screen_space=False,
)

print(text.world.position) # = [0.9, 0.9, 0.0],

text.world.position = [0.0, 10.0, 0.0]

scene = gfx.Scene().add(
    text,
    environment,
    light(target=root),
    root,
)


canvas = rendercanvas.auto.RenderCanvas(title="Flying Teapot")
renderer = gfx.renderers.WgpuRenderer(canvas)

@register
def on_key_down(event):
    global v, omega
    if event.key == "ArrowUp":
        v += 5.0
    if event.key == "ArrowDown":
        v -= 5.0
    if event.key == "ArrowLeft":
        omega += 1.0
    if event.key == "ArrowRight":
        omega -= 1.0

@register
def on_key_up(event):
    global v, omega
    if event.key == "ArrowUp":
        v -= 5.0
    if event.key == "ArrowDown":
        v += 5.0
    if event.key == "ArrowLeft":
        omega -= 1.0
    if event.key == "ArrowRight":
        omega += 1.0




gfx.show(
    scene,

    renderer=renderer,
    camera=camera(),
    before_render=update,
)
