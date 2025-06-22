# Python Standard Library
import time

# Third-party Libraries
import pygfx as gfx
import rendercanvas.auto

canvas = rendercanvas.auto.RenderCanvas(title="Ball")
renderer = gfx.renderers.WgpuRenderer(canvas)

WIDTH, HEIGHT = 20.0, 20.0

ball = gfx.Mesh(
    gfx.sphere_geometry(radius=0.5),
    gfx.MeshBasicMaterial(color="#00ff00"),
)

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
    ball,
    grid,
)

t0 = None

m = 1.0
g = 9.81
vx, vy = 10.0, 10.0
x, y = 0.0, 0.0
ball.local.position = [x, y, 0.0]

def update():
    global t0
    global x, y, vx, vy
    t1 = time.perf_counter()
    dt = t1 - t0
    vy += - g / m * dt
    x += vx * dt
    y += vy * dt
    ball.local.position = [x, y, 0.0]
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
