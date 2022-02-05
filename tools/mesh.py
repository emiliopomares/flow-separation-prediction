class Mesh:
    points = None
    faces = None
    wall_face_start_index = None
    perPointAttributes = None
    perFaceAttributes = None
    boundary_faces = None

    def __init__(self, _points, _faces, _wall_index, _n_wall_faces):
        self.points = _points
        self.faces = _faces
        self.wall_face_start_index = _wall_index
        self.perPointAttributes = {}
        self.perFaceAttributes = {}
        self.boundary_faces = _faces[_wall_index:_wall_index+_n_wall_faces]

    def get_number_of_points(self):
        return len(self.points)

    def get_number_of_faces(self):
        return len(self.faces)

    def get_field_value_for_point(self, point, field):
        return self.perPointAttributes[field][point]

    def get_field_value_for_face(self, face, field):
        return self.perFaceAttributes[field][face]

    def add_point_field(self, field_name, values):
        self.perPointAttributes[field_name] = values

    def add_face_field(self, field_name, values):
        self.perFaceAttributes[field_name] = values
