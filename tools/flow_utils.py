from simulutils import *
from flow_utils import *
import read_geo

def detect_separation_points(mesh, wss):
    print("detect separation points")
    (nFaces, wallStartFace) = read_geo.read_wall_start_face()
    epsilon = 0.0505
    wall_start_face = wallStartFace
    sep_faces = []
    sep_p = []
    for i in range(0, len(wss)):
        n = norm(wss[i])
        if n < epsilon:
            sep_faces.append(i)
            sep_p.append(wall_face_to_p(i, nFaces))
    return sep_p

def find_separation_point(mesh):
    print("find separation points")
    latest_time = find_latest_time_dir()
    wallStresses = read_geo.read_vector_field(latest_time, 'wallShearStress')
    return detect_separation_points(mesh, wallStresses)

def wall_face_to_p(wallFace, nFaces):
    if(wallFace < nFaces//2):
        return (nFaces/2 - wallFace) / (nFaces)
    else:
        return (wallFace / (nFaces))