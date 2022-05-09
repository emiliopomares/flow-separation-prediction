import simulutils
from flow_utils import *
from mesh import *
import read_geo

def detect_separation_point(mesh, wss):
    print("detect separation points")
    wall_face_index = mesh.get_boundary_start_face()
    print("wall face index: " + str(wall_face_index))

    epsilon = 0.0505
    sep_faces = []
    sep_p_old = []
    upper_sep_p = []
    lower_sep_p = []
    previous_stress = 0
    previous_wall_centroid = None
    for i in range(0, len(wss)//2):
        print("i : " + str(i))
        print("wall face + i : " + str(wall_face_index+i))
        face_normals = mesh.get_face_normals_unit_by_index(wall_face_index+i)
        wall_centroid = mesh.get_face_centroid_by_index(wall_face_index+i)
        print("wall face normals parallel: " + str(face_normals[0]))
        print("wall shear stress: " + str(wss[i]))
        stress_in_parallel_direction = simulutils.dot_product(wss[i], face_normals[0])
        n = stress_in_parallel_direction #simulutils.norm(wss[i]) * (-simulutils.sign_of(wss[i][0]) + 1)/2
        print(" Sep point test face  " + str(i) + " -> " + str(n))
        sign_test = previous_stress * n
        if(sign_test < 0 and n > 0):
            print("     Separation point found at wall face " + str(i))
            print("     Previous wall face centroid: " + str(previous_wall_centroid) + ", stress value: " + str(previous_stress))
            print("     Wall face centroid: " + str(wall_centroid) + ", stress value: " + str(n))
            total_upper_surface_length = calculate_upper_profile_length(mesh)
            prev_point_length = calculate_partial_profile_length(mesh, i-1)
            past_point_length = calculate_partial_profile_length(mesh, i)
            print("             Total surface length: " + str(total_upper_surface_length) + ",    prev point length: " + str(prev_point_length/ total_upper_surface_length) + ",  past point length length: " + str(past_point_length/ total_upper_surface_length))
            print("                                             ,    prev point stress: " + str(previous_stress) + ",  past point length length: " + str(n))
            prev_point_x = prev_point_length / total_upper_surface_length
            past_point_x = past_point_length / total_upper_surface_length
            return find_zero_crossing_linear(prev_point_x, previous_stress, past_point_x, n)
        previous_wall_centroid = wall_centroid
        previous_stress = n
    return 1.0

def find_zero_crossing_linear(x_1, y_1, x_2, y_2):
    total_y_advance = -(y_2 - y_1)
    y_to_zero = y_1
    fraction = y_to_zero / total_y_advance
    print("    total_y_advance: " + str(total_y_advance) + ", y_to_zero: " + str(y_1) + ", fraction: " + str(fraction))
    result = x_1 + (x_2-x_1)*fraction
    print("   x_1: "+str(x_1)+", x_2: "+str(x_2)+", x result: " + str(result))
    return result

def calculate_pressure_lift_drag(mesh, angle_of_attack):
    latest_time = simulutils.find_latest_time_dir()
    pressure = read_geo.read_scalar_field(latest_time, 'p')
    boundary_faces = mesh.get_boundary_faces()
    for boundary_face in boundary_faces:
        area = mesh.calculate_face_area(boundary_face)
        normals = mesh.get_face_normals_unit(boundary_face) # normal direction is normals[1]
        
    return [0,0,0]

def calculate_wallShearStress_lift_drag(mesh, angle_of_attack):
    latest_time = simulutils.find_latest_time_dir()
    wallStresses = read_geo.read_vector_field(latest_time, 'wallShearStress')
    return [0,0,0]

def find_separation_point(mesh):
    latest_time = simulutils.find_latest_time_dir()
    wallStresses = read_geo.read_vector_field(latest_time, 'wallShearStress')
    return detect_separation_point(mesh, wallStresses)

def get_min_x_of_face(mesh, face):
    x = []
    for index in face:
        x.append(mesh.points[index][0])
    return min(x)

def calculate_profile_projection(mesh, wallFaceIndex):
    total_length = 0
    count = 0
    n_wall_faces = len(mesh.boundary_faces)
    #print("min x = " + str(get_min_x_of_face(mesh, mesh.boundary_faces[38] )))
    face = mesh.boundary_faces[wallFaceIndex]
    measures = 0
    accum_x = 0
    for index in face:
        point = mesh.points[index]
        #print("   point in face " + str(point))
        if point[2] > 0.0:
            continue
        accum_x += point[0]  
        measures += 1  
    return accum_x / measures

def calculate_upper_profile_length(mesh):
    total_length = 0
    count = 0
    wall_face_index = mesh.get_boundary_start_face()
    n_upper_faces = len(mesh.boundary_faces)//2
    for i in range(0, n_upper_faces):
        face_parallel_vector = mesh.get_face_parallel_vector_by_index(wall_face_index+i)
        vector_length = simulutils.norm(face_parallel_vector)
        total_length += vector_length
    return total_length

def calculate_partial_profile_length(mesh, stop_index):
    total_length = 0
    number_of_boundary_faces = len(mesh.get_boundary_faces())
    wall_face_index = mesh.get_boundary_start_face()
    n_upper_faces = len(mesh.boundary_faces)//2
    for i in range(0, number_of_boundary_faces):
        face_parallel_vector = mesh.get_face_parallel_vector_by_index(wall_face_index+i)
        vector_length = simulutils.norm(face_parallel_vector)
        total_length += vector_length
        if i == stop_index:
            break
    return total_length

#def calculate_upper_profile_length(mesh):
#    return calculate_upper_profile_length(mesh, lambda x, y: x < y//2)

#def calculate_lower_profile_length(mesh):
#    return calculate_upper_profile_length(mesh, lambda x, y: x >= y//2)

def wall_face_to_p(mesh, wallFaceIndex):
    #return wallFaceIndex
    return calculate_profile_projection(mesh, wallFaceIndex)
    #return calculate_partial_profile_length(mesh, wallFace)

def wall_face_to_p_old(wallFace, nFaces):
    if(wallFace < nFaces//2):
        return (nFaces/2 - wallFace) / (nFaces)
    else:
        return (wallFace / (nFaces))

def make_result_from_separation_points(angle, s):
    result = {
        'lower_sep_point':1,
        'upper_sep_point':1
    }
    if len(s['upper_sep_points']) == 0:
        result['upper_sep_point'] = 1
    elif angle>0:
        result['upper_sep_point'] = min(s['upper_sep_points'])
    if len(s['lower_sep_points']) == 0:
        result['lower_sep_point'] = 1
    elif angle<=0:
        result['lower_sep_point'] = min(s['lower_sep_points'])
    return result