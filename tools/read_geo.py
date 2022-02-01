from config import config
import os
from mesh import Mesh
from simulutils import *
import matplotlib.pyplot as plt

def read_vector_field(base_dir, field_name):
    fieldPath = config['project_path'] + base_dir + '/' + field_name
    with open(fieldPath, 'r') as f:
        lines = f.readlines()
        all_points = []
        state = False
        for line in lines:
            if line.startswith('('):
                if state == False:
                    state = True
                else:
                    components_str = line.replace('(', '').replace(')', '').split(' ')
                    all_points.append([float(components_str[0]), float(components_str[1]), float(components_str[2])])
    return all_points

def read_points():
    return read_vector_field('constant/polyMesh', 'points')

def read_faces():
    # warning: quads are expected!
    meshFacesPath = config['project_path'] + "constant/polyMesh/faces"
    with open(meshFacesPath, 'r') as f:
        lines = f.readlines()
        all_faces = []
        state = False
        for line in lines:
            if line.startswith('(') and state == False:
                state = True
            elif line.startswith('4') and state == True:
                components_str = line.replace('(', ' ').replace(')', '').split(' ')
                all_faces.append([ int(components_str[1]), int(components_str[2]), int(components_str[3]), int(components_str[4])])
    return all_faces

def read_geo():
    points = read_points()
    faces = read_faces()
    result = Mesh(points, faces)
    return result

def detect_separation_points(mesh, wss):
    epsilon = 0.00505
    wall_start_face = 22202 # must parse this!
    sep_faces = []
    for i in range(0, len(wss)):
        n = norm(wss[i])
        if n < epsilon:
            sep_faces.append(i+wall_start_face)
    print(sep_faces)

if __name__ == '__main__':
    g = read_geo()
    i = 78
    x = list(map(lambda x: x[0], g.points))
    y = list(map(lambda x: x[1], g.points))
    plt.scatter(x, y, s=0.1, c='b')
    face_x = [g.points[g.faces[22202+i][0]][0], g.points[g.faces[22202+i][1]][0], g.points[g.faces[22202+i][2]][0], g.points[g.faces[22202+i][3]][0]]
    face_y = [g.points[g.faces[22202+i][0]][1], g.points[g.faces[22202+i][1]][1], g.points[g.faces[22202+i][2]][1], g.points[g.faces[22202+i][3]][1]]
    plt.scatter(face_x, face_y, s=2.7, c='r')
    plt.show()

    #time_base_dir = find_latest_time_dir()
    #wall_shear_stress = read_vector_field(time_base_dir, 'wallShearStress')
    #print(wall_shear_stress[1])
    #detect_separation_points(g, wall_shear_stress)
