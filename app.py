import numpy as np
import pygfx as gfx
import pylinalg as la

from wgpu.gui.auto import WgpuCanvas

tau = 2 * np.pi
red = "#ff0000"
green = "#00ff00"
blue = "#0000ff"



geometry = gfx.cylinder_geometry(
    radius_bottom=0.125,
    radius_top=0.125,
    height=0.1,
    radial_segments=32,
    theta_start=-1/8 * tau,
    theta_length=3/4 * tau,
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

c3 = gfx.Mesh(geometry=gfx.sphere_geometry(radius=0.1), material=gfx.MeshPhongMaterial(color=blue))

g = gfx.Group()
g.add(c1, c2, c3)

camera = gfx.OrthographicCamera(4, 3)

clock = gfx.Clock()

offset = 0.0

def animate():
    t = clock.get_elapsed_time()
    omega = 0.1 * tau + offset
    g.world.position = [0.0, 0.0, 0.0]
    g.world.rotation = la.quat_from_axis_angle((0.0, 0.0, 1.0), omega * t)
    c1.local.position = [0.0, 0.0, 0.0]
    c2.local.position = [0.0, -0.5, 0.0]
    c2.local.rotation = la.quat_from_axis_angle((1.0, 0.0, 0.0), tau / 4)
    c3.local.position = [0.0, -1.0, 0.0]


canvas = WgpuCanvas()
renderer = gfx.renderers.WgpuRenderer(canvas)

@renderer.add_event_handler("click")
def handle_event(event):
    global offset
    print(offset)
    offset += 0.25 * tau
    


if __name__ == "__main__":
    disp = gfx.Display(camera=camera, stats=True)
    disp.before_render = animate
    disp.show(g)
