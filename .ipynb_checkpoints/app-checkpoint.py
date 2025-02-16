import numpy as np
import pygfx as gfx
# import pylinalg as la

geometry = gfx.box_geometry(1.0, 1.0, 1.0)
material = material = gfx.MeshPhongMaterial()
cube = gfx.Mesh(geometry, material)

camera = gfx.OrthographicCamera(2, 2)

clock = gfx.Clock()


def animate():
    t = clock.get_elapsed_time()
    omega = 2 * np.pi
    cube.world.position = [0.2 * np.sin(omega * t), 0.2 * np.cos(omega * t), 0]


if __name__ == "__main__":
    disp = gfx.Display(camera=camera)
    disp.before_render = animate
    disp.show(cube)
