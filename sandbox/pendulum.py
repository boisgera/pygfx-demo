import numpy as np
import pygfx as gfx
import pylinalg as la

# That's too bad, that I have to introduce this extra complexity,
# since Display is supposed to pick the right default for us,
# but I don't know how to add global event handlers (keyboard events)
# otherwise.
# Try to see if another object could not be the target of such an
# event handler, so that we can avoid this complexity.
from rendercanvas.auto import RenderCanvas
from pygfx.renderers import WgpuRenderer
renderer = WgpuRenderer(target=RenderCanvas())


tau = 2 * np.pi
red = "#ff0000"
green = "#00ff00"
blue = "#0000ff"


geometry = gfx.cylinder_geometry(
    radius_bottom=0.125,
    radius_top=0.125,
    height=0.1,
    radial_segments=32,
    theta_start=-1 / 8 * tau,
    theta_length=3 / 4 * tau,
)
material = gfx.MeshPhongMaterial(color=red)
c1 = gfx.Mesh(geometry, material)

geometry = gfx.cylinder_geometry(
    radius_bottom=0.05,
    radius_top=0.05,
    height=1.0,
    radial_segments=32,
)
material = gfx.MeshPhongMaterial(color=green)
c2 = gfx.Mesh(geometry, material)

c3 = gfx.Mesh(
    geometry=gfx.sphere_geometry(radius=0.1),
    material=gfx.MeshPhongMaterial(color=blue),
)

g = gfx.Group()
g.add(c1, c2, c3)


angle = 0.0

g.world.position = [0.0, 0.0, 0.0]
g.world.rotation = la.quat_from_axis_angle((0.0, 0.0, 1.0), angle)
c1.local.position = [0.0, 0.0, 0.0]
c2.local.position = [0.0, -0.5, 0.0]
c2.local.rotation = la.quat_from_axis_angle((1.0, 0.0, 0.0), tau / 4)
c3.local.position = [0.0, -1.0, 0.0]

camera = gfx.OrthographicCamera(4, 3)

clock = gfx.Clock()


arrow_left = False
arrow_right = False


def animate():
    global angle
    _t = clock.get_elapsed_time()
    angle += (arrow_right - arrow_left) * (1 / 30) * tau
    g.world.rotation = la.quat_from_axis_angle((0.0, 0.0, 1.0), angle)


@renderer.add_event_handler("key_down", "key_up")
def handle_event(event):
    global arrow_left, arrow_right
    if event.key == "ArrowLeft":
        arrow_left = event.type == "key_down"
    if event.key == "ArrowRight":
        arrow_right = event.type == "key_down"

if __name__ == "__main__":
    display = gfx.Display(
        camera=camera,
        renderer=renderer,
        stats=True,
        before_render=animate,
    )
    display.show(g)
