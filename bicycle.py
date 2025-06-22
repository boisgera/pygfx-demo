# Python Standard Library
import math
import time

# Third-party Libraries
import numpy as np
import pygfx as gfx
import pylinalg as la
import rendercanvas.auto

canvas = rendercanvas.auto.RenderCanvas(title="Ball")
renderer = gfx.renderers.WgpuRenderer(canvas)

WIDTH, HEIGHT = 20.0, 20.0

l = 3.0

frame = gfx.Mesh(
    gfx.box_geometry(0.1, l, 0.1),
    gfx.MeshBasicMaterial(color="#00ff00"),
)

frame.local.position = [0.0, l/2, 0.0]

front_wheel = gfx.Mesh(
    gfx.box_geometry(0.2, l/4, 0.2),
    gfx.MeshBasicMaterial(color="#ffff00"),
)

frame.add(front_wheel)
front_wheel.local.position = [0.0, l/2, 0.0]

back_wheel = gfx.Mesh(
    gfx.box_geometry(0.2, l/4, 0.2),
    gfx.MeshBasicMaterial(color="#ffff00"),
)

frame.add(back_wheel)
back_wheel.local.position = [0.0, -l/2, 0.0]

bicycle = gfx.Group().add(frame)

grid = gfx.Grid(
    orientation="xy",
    material=gfx.GridMaterial(
        major_step=1.0,
        major_thickness=1.0,
        thickness_space="screen",
        major_color="#ffffff",
        infinite=False,
    ),
)
grid.local.scale = [WIDTH, HEIGHT, 1.0]
grid.local.position = [-WIDTH/2, -HEIGHT/2, 0.0]

camera = gfx.OrthographicCamera(width=1.1*WIDTH, height=1.1*HEIGHT)
camera.local.position = [WIDTH/2, HEIGHT/2, 1000.0]
camera.look_at([0.0, 0.0, 0.0])


scene = gfx.Scene().add(
    bicycle,
    grid,
)

t0 = None

m = 1.0
g = 9.81
x, y = 0.0, 0.0
v = 0.0
theta = 0.0
d_theta = 0.0
angle = 0.0
omega = 0.0

bicycle.local.position = [0.0, y, 0.0]


def on_key_down(event):
    global v, d_theta
    if event.key == "ArrowUp":
        v += 5.0
    if event.key == "ArrowDown":
        v += -5.0
    if event.key == "ArrowLeft":
        d_theta += 1.0
    if event.key == "ArrowRight":
        d_theta += -1.0

renderer.add_event_handler(on_key_down, "key_down")

def on_key_up(event):
    global v, d_theta
    if event.key == "ArrowUp":
        v -= 5.0
    if event.key == "ArrowDown":
        v -= -5.0
    if event.key == "ArrowLeft":
        d_theta -= 1.0
    if event.key == "ArrowRight":
        d_theta -= - 1.0

renderer.add_event_handler(on_key_up, "key_up")

def update():
    global t0
    global x, y, v, theta, d_theta, angle
    t1 = time.perf_counter()
    dt = t1 - t0
    x += - v * dt * math.sin(angle)
    y +=   v * dt * math.cos(angle)
    theta += d_theta * dt
    theta = max(-math.pi/2*0.75, min(math.pi/2*0.75, theta))
    angle += v / l * math.tan(theta) * dt
    # print(theta)
    bicycle.local.position = [x, y, 0.0]
    bicycle.local.rotation = la.quat_from_axis_angle(
        [0.0, 0.0, 1.0], angle)
    front_wheel.local.rotation = la.quat_from_axis_angle(
        [0.0, 0.0, 1.0], theta)
    
    t0 = t1

def animate():
    update()
    renderer.render(scene, camera)
    canvas.request_draw(animate)


# Initial render to set up the scene synchrously
renderer.render(scene, camera) # The first render is likely to be very slow

canvas.request_draw(animate)
t0 = time.perf_counter()
rendercanvas.auto.loop.run()
