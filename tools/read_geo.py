from config import config
import os
from mesh import Mesh
from simulutils import *
import matplotlib.pyplot as plt

def read_wall_start_face():
    boundaryFile = config['project_path'] + 'constant/polyMesh/boundary'
    with open(boundaryFile) as f:
        lines = f.readlines()
        foundWalls = False
        foundNFaces = False
        for line in lines:
            strippedLine = line.strip()
            if(strippedLine == 'walls'):
                foundWalls = True
            if strippedLine.startswith('nFaces') and foundWalls == True:
                nFacesString = strippedLine.replace('nFaces', '').replace(';', '').strip()
                nFaces = int(nFacesString)
                foundNFaces = True
            if strippedLine.startswith('startFace') and foundWalls == True and foundNFaces == True:
                sFaceString = strippedLine.replace('startFace', '').replace(';', '').strip()
                startFace = int(sFaceString)
                return (nFaces, startFace)

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

def wall_face_to_p(wallFace, nFaces):
    if(wallFace < nFaces//2):
        return (nFaces/2 - wallFace) / (nFaces)
    else:
        return (wallFace / (nFaces))

def detect_separation_points(mesh, wss):
    (nFaces, wallStartFace) = read_wall_start_face()
    epsilon = 0.00505
    wall_start_face = wallStartFace
    sep_faces = []
    sep_p = []
    for i in range(0, len(wss)):
        n = norm(wss[i])
        if n < epsilon:
            sep_faces.append(i)
            sep_p.append(wall_face_to_p(i, nFaces))
    print(sep_faces)
    print(sep_p)

def find_separation_point(mesh):
    latest_time = find_latest_time_dir()
    wallStresses = read_vector_field(latest_time, 'wallShearStress')
    detect_separation_points(mesh, wallStresses)


if __name__ == '__main__':
    (nFaces, wallStartFace) = read_wall_start_face()
    print(nFaces)
    print(wallStartFace)
    g = read_geo() # 0 to 40, upper... 41 to 81 lower   0 to 81 = 82 faces
    
    find_separation_point(g)
    #i = 0
    #x = list(map(lambda x: x[0], g.points))
    #y = list(map(lambda x: x[1], g.points))
    #plt.scatter(x, y, s=0.1, c='b')
    #face_x = [g.points[g.faces[wallStartFace+i][0]][0], g.points[g.faces[wallStartFace+i][1]][0], g.points[g.faces[wallStartFace+i][2]][0], g.points[g.faces[wallStartFace+i][3]][0]]
    #face_y = [g.points[g.faces[wallStartFace+i][0]][1], g.points[g.faces[wallStartFace+i][1]][1], g.points[g.faces[wallStartFace+i][2]][1], g.points[g.faces[wallStartFace+i][3]][1]]
    #plt.scatter(face_x, face_y, s=2.7, c='r')
    #plt.show()

    #time_base_dir = find_latest_time_dir()
    #wall_shear_stress = read_vector_field(time_base_dir, 'wallShearStress')
    #print(wall_shear_stress[1])
    #detect_separation_points(g, wall_shear_stress)
