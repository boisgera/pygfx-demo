import numpy as np
import sdf  # from https://github.com/fogleman/sdf

# Axe
length = 1.0
width = 0.2
height = 0.05

box = sdf.box(a=[0, -width / 2, 0], b=[length, width / 2, height])
disk = sdf.capped_cylinder([0.0, 0.0, 0.0], [0.0, 0.0, height], width / 2)
hole = sdf.capped_cylinder([0.0, 0.0, 0.0], [0.0, 0.0, height], 0.5 * width / 2)

axe = (box | disk | disk.translate([length, 0.0, 0.0])) - (
    hole | hole.translate([length, 0.0, 0.0])
)

axe.save("models/axe.stl")

# Wheel
width = 0.5
radius = 1.0
square_radius = 0.5
square_width = 0.75
assert square_width > width
hole_radius = 0.2

cylinder = sdf.capped_cylinder(
    [0.0, 0.0, -width / 2],
    [0.0, 0.0, +width / 2],
    radius,
)
square = sdf.box(
    a=[-square_radius, -square_radius, -square_width / 2],
    b=[+square_radius, +square_radius, +square_width / 2],
)
hole = sdf.cylinder(hole_radius)

wheel = (cylinder | square) - hole
wheel.save("models/wheel.stl")

# Frame
radius = 5.0
ratio = 0.8
width = 0.5
axe_radius = 0.20001
frame = sdf.capped_cylinder(
    [0.0, 0.0, -width / 2],
    [0.0, 0.0, +width / 2],
    radius,
)
frame -= sdf.box(
    a=[-2 * radius, -2 * radius, -width],
    b=[-ratio * radius, +2 * radius, +2 * width],
)
frame -= sdf.box(
    a=[+ratio * radius, -2 * radius, -width],
    b=[2 * ratio * radius, +2 * radius, +2 * width],
)
frame |= (
    sdf.capped_cylinder([0.0, 0.0, 0.0], [0.0, 0.0, 2*radius], axe_radius)
    .rotate(np.pi / 2, [0.0, -1.0, 0.0])
    .translate([radius, 0.0, 0.0])
)

frame = frame.rotate(np.pi / 2, [0.0, 0.0, 1.0])


frame.save("models/frame.stl")
