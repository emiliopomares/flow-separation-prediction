# Base off Thien Phans's work
import math

hyperparameters = {
    'z_depth': 0.3,
    'mesh_scale': 1, 
    'cell_size_at_leading_edge':  0.01,
    'cell_size_at_trailing_edge': 0.03,
    'cell_size_in_middle': 0.035,
    'separating_point_position': 0.4,
    'boundary_layer_thickness': 0.5,
    'first_layer_thickness': 0.005,
    'expansion_ratio': 1.2,
    'max_cell_size_in_inlet': 1,
    'max_cell_size_in_outlet': 1,
    'max_cell_size_in_inlet_x_outlet': 1
}

def generate_blockMesh(pointList, aoa, inlet_x_dist, outlet_x_dist):
    return generate_blockMesh_full(pointList, aoa, inlet_x_dist, outlet_x_dist, \
        hyperparameters['z_depth'], \
        hyperparameters['mesh_scale'], \
        hyperparameters['cell_size_at_leading_edge'], \
        hyperparameters['cell_size_at_trailing_edge'], \
        hyperparameters['cell_size_in_middle'], \
        hyperparameters['separating_point_position'], \
        hyperparameters['boundary_layer_thickness'], \
        hyperparameters['first_layer_thickness'], \
        hyperparameters['expansion_ratio'], \
        hyperparameters['max_cell_size_in_inlet'], \
        hyperparameters['max_cell_size_in_outlet'], \
        hyperparameters['max_cell_size_in_inlet_x_outlet'])

def generate_blockMesh_full(csv_data, aoa, inlet_x_dist, \
    outlet_x_dist, z_depth, mesh_scale, cell_size_at_leading_edge, \
    cell_size_at_trailing_edge, cell_size_in_middle, \
    separating_point_position, boundary_layer_thickness, \
    first_layer_thickness, expansion_ratio, \
    max_cell_size_in_inlet, max_cell_size_in_outlet, \
    max_cell_size_in_inlet_x_outlet, write_to_file=True):
    num_mesh_on_boundary_layer = round(math.log(1+(expansion_ratio-1)*boundary_layer_thickness/first_layer_thickness)/math.log(expansion_ratio))
    expansion_ratio_on_bl = expansion_ratio**num_mesh_on_boundary_layer
    last_layer_thickness = first_layer_thickness * expansion_ratio ** num_mesh_on_boundary_layer
    expansion_ratio_out_of_bl = max_cell_size_in_inlet / last_layer_thickness
    expansion_ratio_tail = max_cell_size_in_outlet / cell_size_at_trailing_edge
    expansion_ratio_1 = (last_layer_thickness/inlet_x_dist) * (expansion_ratio_out_of_bl-1)+1
    num_mesh_out_of_boundary_layer = round(math.log(expansion_ratio_out_of_bl)/math.log(expansion_ratio_1))
    expansion_ratio_2 = (cell_size_at_trailing_edge / outlet_x_dist) * (expansion_ratio_tail-1)+1
    expansion_ratio_in_leading = cell_size_in_middle / cell_size_at_leading_edge
    expansion_ratio_3 = (cell_size_at_leading_edge/separating_point_position) * (expansion_ratio_in_leading-1) + 1
    expansion_ratio_4 = (cell_size_at_trailing_edge/(1-cell_size_in_middle)) + 1
    num_mesh_in_trailing = 20
    num_mesh_3 = math.log(expansion_ratio_in_leading) / math.log(expansion_ratio_3)
    num_mesh_in_leading = round(num_mesh_3)
    expansion_ratio_trailing = cell_size_in_middle / cell_size_at_trailing_edge
    inlet_expansion_ratio_1 = cell_size_at_trailing_edge / max_cell_size_in_inlet
    inlet_expansion_ratio_2 = 0.25
    result = "\n"
    result += "FoamFile\n"
    result += "{\n"
    result += " version 2.0;\n"
    result += " format ascii;\n"
    result += " class dictionary;\n"
    result += " object blockMeshDict;\n"
    result += "}\n"
    result += "convertToMeters " + str(mesh_scale) + ";\n"
    result += "\n"
    result += "geometry\n"
    result += "{\n"
    result += "}\n"
    result += "\n"
    result += "vertices\n"
    result += "("
    result += " ( 0      0      0)\n"
    result += " ( 1      0      0)\n"
    result += " ( 1     %g      0)\n" % inlet_x_dist
    result += " ( %g    0       0)\n" % (-inlet_x_dist+1)
    result += " ( 0     0      %g)\n" % z_depth
    result += " ( 1     0      %g)\n" % z_depth
    result += " ( 1    %g      %g)\n" % (inlet_x_dist, z_depth)
    result += " ( %g     0      %g)\n" % (-inlet_x_dist+1, z_depth)
    result += " ( %g    %g      0)\n" % (outlet_x_dist+1, math.sin(math.pi/180*aoa)*(outlet_x_dist+1))
    result += " ( %g    %g      0)\n" % (outlet_x_dist+1, inlet_x_dist)
    result += " ( %g    %g     %g)\n" % (outlet_x_dist+1, math.sin(math.pi/180*aoa)*(outlet_x_dist+1), z_depth)
    result += " ( %g    %g     %g)\n" % (outlet_x_dist+1, inlet_x_dist, z_depth)
    result += " ( %g    %g     %g)\n" % (1, -inlet_x_dist, 0)
    result += " ( %g    %g     %g)\n" % (1, -inlet_x_dist, z_depth)
    result += " ( %g    %g      0)\n" % (outlet_x_dist+1, -inlet_x_dist)
    result += " ( %g    %g     %g)\n" % (outlet_x_dist+1, -inlet_x_dist, z_depth)
    result += " (  1     0      0)\n"
    result += " (  1     0     %g)\n" % (z_depth)
    result += ");"
    result += "\n"
    result += "blocks\n"
    result += "(\n"
    result += " hex (0 1 2 3 4 5 6 7) (%g %g 1)" % ()
    return result


