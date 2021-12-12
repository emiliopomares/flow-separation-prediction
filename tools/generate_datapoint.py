import generate_naca5
from generate_blockMesh import *
from generate_naca5 import *

points = generate_naca5_airfoil_points(0.3, 4, 0, 10, 101, False)
file = generate_blockMesh(points, 5, 12, 20)
print(file)