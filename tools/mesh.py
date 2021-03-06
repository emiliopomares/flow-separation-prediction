import math

class Mesh:
    points = None
    faces = None
    wall_face_start_index = None
    perPointAttributes = None
    perFaceAttributes = None
    boundary_faces = None
    boundary_start_face = 0

    def __init__(self, _points, _faces, _wall_index, _n_wall_faces):
        self.points = _points
        self.faces = _faces
        self.wall_face_start_index = _wall_index
        self.perPointAttributes = {}
        self.perFaceAttributes = {}
        self.boundary_faces = _faces[_wall_index:_wall_index+_n_wall_faces]
        self.boundary_start_face = _wall_index

    def get_number_of_points(self):
        return len(self.points)

    def get_number_of_faces(self):
        return len(self.faces)

    def get_face_by_index(self, face_index):
        return self.faces[face_index]

    def get_face_parallel_vector_by_index(self, face_index): # must know direction!
        print("get face parallel vector called with face: " + str(face_index))
        face_vertices = self.get_face_vertices_by_index(face_index)
        anchor = face_vertices[0]
        cis = face_vertices[1]
        mult = 1
        if cis[0]==anchor[0] and cis[1]==anchor[1]:
            anchor = face_vertices[2]
            cis = face_vertices[0]
            mult = -1
        cis_vector = [mult*(cis[0]-anchor[0]), mult*(cis[1]-anchor[1]), 0]
        return cis_vector

    def get_face_normals_unit_by_index(self, face_index): # must know direction!
        face_vertices = self.get_face_vertices_by_index(face_index)
        anchor = face_vertices[0]
        cis = face_vertices[1]
        trans = face_vertices[2]
        mult = 1
        if cis[0]==anchor[0] and cis[1]==anchor[1]:
            anchor = face_vertices[2]
            cis = face_vertices[0]
            trans = face_vertices[1]
            mult = -1
        a = math.sqrt((cis[0]-anchor[0])**2 + (cis[1]-anchor[1])**2)
        b = abs(trans[2]-anchor[2])
        print("    Anchor vertex: " + str(anchor))
        print("    Cis vertex: " + str(cis))
        print("    Trans vertex: " + str(trans))
        cis_direction = [mult*(cis[0]-anchor[0])/a, mult*(cis[1]-anchor[1])/a, 0]
        normal_direction = [mult*(-cis_direction[1]), mult*cis_direction[0], 0]
        trans_direction = [0, 0, mult]
        return (cis_direction, normal_direction, trans_direction)
        

    def get_face_area(self, face):
        face_vertices = self.get_face_vertices_by_index(face)
        anchor = face_vertices[0]
        cis = None
        trans = None
        for vertex in face_vertices:
            if vertex[0:2] != anchor[0:2] and vertex[2] == anchor[2]:
                cis = vertex
            if vertex[0:2] == anchor[0:2] and vertex[2] != anchor[2]:
                trans = vertex
        a = math.sqrt((cis[0]-anchor[0])**2 + (cis[1]-anchor[1])**2)
        b = abs(trans[2]-anchor[2])
        return a*b

    def get_face_centroid_by_index(self, face_index):
        vertices = self.get_face_vertices_by_index(face_index)
        accX = 0
        accY = 0
        accZ = 0
        for vertex in vertices:
            accX += vertex[0]
            accY += vertex[1]
            accZ += vertex[2]
        return [accX/len(vertices), accY/len(vertices), accZ/len(vertices)]

    def get_face_vertices_by_index(self, face_index):
        result = []
        face_vertices = self.get_face_by_index(face_index)
        for vertex in face_vertices:
            result.append(self.points[vertex])
        return result

    def get_boundary_faces(self):
        return self.boundary_faces

    def get_boundary_start_face(self):
        return self.boundary_start_face

    def get_field_value_for_point(self, point, field):
        return self.perPointAttributes[field][point]

    def get_field_value_for_face(self, face, field):
        return self.perFaceAttributes[field][face]

    def add_point_field(self, field_name, values):
        self.perPointAttributes[field_name] = values

    def add_face_field(self, field_name, values):
        self.perFaceAttributes[field_name] = values
