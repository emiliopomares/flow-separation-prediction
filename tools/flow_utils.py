import simulutils
from flow_utils import *
import read_geo

def detect_separation_points(mesh, wss):
    print("detect separation points")
    (nFaces, wall_start_face) = read_geo.read_wall_start_face()
    epsilon = 0.0505
    sep_faces = []
    sep_p_old = []
    upper_sep_p = []
    lower_sep_p = []
    for i in range(0, len(wss)):
        n = simulutils.norm(wss[i])
        if n < epsilon:
            #sep_faces.append(i)
            #sep_p_old.append(wall_face_to_p_old(i, nFaces))
            #sep_p.append(wall_face_to_p(mesh, i))
            if(i > len(wss)//2):
                lower_sep_p.append(wall_face_to_p(mesh, i))
            else:
                upper_sep_p.append(wall_face_to_p(mesh, i))
    return {
        'upper_sep_points': upper_sep_p,
        'lower_sep_points': lower_sep_p
    }

def find_separation_point(mesh):
    print("find separation points")
    latest_time = simulutils.find_latest_time_dir()
    wallStresses = read_geo.read_vector_field(latest_time, 'wallShearStress')
    return detect_separation_points(mesh, wallStresses)

def calculate_partial_profile_length(mesh, wall_face_index):
    total_length = 0
    count = 0
    n_wall_faces = len(mesh.boundary_faces)
    is_upper = wall_face_index <= n_wall_faces//2
    start_face = 0
    if is_upper == False:
        start_face = n_wall_faces // 2
    for i in range(start_face, wall_face_index):
        count+=1
        v1 = None
        v2 = None
        for index in mesh.boundary_faces[i]:
            point = mesh.points[index]
            if point[2] > 0.0:
                continue
            if v1 == None:
                v1 = point
            else:
                v2 = point
            if v1 != None and v2 != None:
                total_length += simulutils.norm([v2[0]-v1[0], v2[1]-v1[1], 0])
    return total_length

def calculate_profile_length(mesh, comp_func):
    total_length = 0
    count = 0
    n_wall_faces = len(mesh.boundary_faces)
    for face in mesh.boundary_faces:
        count+=1
        if comp_func(count-1, n_wall_faces)==False:
            continue
        v1 = None
        v2 = None
        for index in face:
            point = mesh.points[index]
            if point[2] > 0.0:
                continue
            if v1 == None:
                v1 = point
            else:
                v2 = point
            if v1 != None and v2 != None:
                total_length += simulutils.norm([v2[0]-v1[0], v2[1]-v1[1], 0])
    return total_length

def calculate_upper_profile_length(mesh):
    return calculate_profile_length(mesh, lambda x, y: x < y//2)

def calculate_lower_profile_length(mesh):
    return calculate_profile_length(mesh, lambda x, y: x >= y//2)

def wall_face_to_p(mesh, wallFace):
    return calculate_partial_profile_length(mesh, wallFace)

def wall_face_to_p_old(wallFace, nFaces):
    if(wallFace < nFaces//2):
        return (nFaces/2 - wallFace) / (nFaces)
    else:
        return (wallFace / (nFaces))