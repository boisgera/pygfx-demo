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
square_width = 1.2
assert square_width > width
hole_radius = 0.2

cylinder = sdf.capped_cylinder(
    [0.0, 0.0, -width / 2],
    [0.0, 0.0, +width / 2],
    radius,
)
square = sdf.box(
    a=[-square_radius, +square_radius, -square_width / 2],
    b=[+square_radius, +square_radius, +square_width / 2],
)
hole = sdf.cylinder(radius)

wheel = (cylinder | square) - hole 
wheel.save("models/wheel.stl")