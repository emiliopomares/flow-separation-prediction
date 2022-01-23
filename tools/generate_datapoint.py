import generate_naca5
from generate_blockMesh import *
from generate_naca5 import *
from generate_naca4 import *

def generate_example_datapoint():
    #points = generate_naca5_airfoil_points(0.3, 0, 0, 10, 101, False)
    points = generate_naca4_airfoil_points(2, 40, 40, 101, 0, False)
    file = generate_blockMesh(points, -25, 12, 20)
    return file

def print_example_datapoint():
    points = generate_naca4_airfoil_points(2, 40, 40, 101, 0, False)
    print(points)

if __name__ == '__main__':
    print_example_datapoint()