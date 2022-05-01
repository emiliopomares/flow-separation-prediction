# Based off Thien Phans's work
import math

hyperparameters = {
    'z_depth':                          0.3,
    'mesh_scale':                       1, 
    'cell_size_at_leading_edge':        0.01,
    'cell_size_at_trailing_edge':       0.03,
    'cell_size_in_middle':              0.035,
    'separating_point_position':        0.4,
    'boundary_layer_thickness':         0.1,
    'first_layer_thickness':            0.0002, # 0.00001, # was 0.005 working value 0.00002
    'expansion_ratio':                  1.2,
    'max_cell_size_in_inlet':           1,
    'max_cell_size_in_outlet':          1,
    'max_cell_size_in_inlet_x_outlet':  1
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

globalRefine = 2.5
parallelRefine = 1*globalRefine
normalRefine = 1*globalRefine


def generate_blockMesh_full(pointList, aoa, inlet_x_dist, \
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
    expansion_ratio_at_outlet = max_cell_size_in_inlet_x_outlet * (expansion_ratio_out_of_bl/max_cell_size_in_outlet) * (num_mesh_out_of_boundary_layer+num_mesh_on_boundary_layer)/num_mesh_out_of_boundary_layer
    num_mesh_1 = math.log(expansion_ratio_out_of_bl)/math.log(expansion_ratio_1)
    num_mesh_2 = math.log(expansion_ratio_tail)/math.log(expansion_ratio_2)
    num_mesh_4 = math.log(expansion_ratio_trailing)/math.log(expansion_ratio_4)
    a = max_cell_size_in_inlet_x_outlet**(1/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer))
    num_mesh_at_tail = round(num_mesh_2)
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
    result += " hex (0 1 2 3 4 5 6 7) (%g %g 1)\n" % (round(parallelRefine*(num_mesh_in_leading+num_mesh_in_trailing)), round(normalRefine*(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer)))
    result += " edgeGrading\n"
    result += " (\n"
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (separating_point_position, num_mesh_in_leading/(num_mesh_in_leading+num_mesh_in_trailing), expansion_ratio_in_leading)
    result += "         ( %g %g %g )\n" % (1-separating_point_position, 1-num_mesh_in_leading/(num_mesh_in_leading+num_mesh_in_trailing), expansion_ratio_trailing)
    result += "     )\n"
    result += "         %g %g\n" % (inlet_expansion_ratio_1, inlet_expansion_ratio_1)
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (separating_point_position, num_mesh_in_leading/(num_mesh_in_leading+num_mesh_in_trailing), expansion_ratio_in_leading)
    result += "         ( %g %g %g )\n" % (1-separating_point_position, 1-num_mesh_in_leading/(num_mesh_in_leading+num_mesh_in_trailing), expansion_ratio_trailing)
    result += "     )\n"
    # y direction expansion ratio
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_on_bl)
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_out_of_bl)
    result += "     )\n"
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_on_bl)
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_out_of_bl)
    result += "     )\n"
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_on_bl)
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_out_of_bl)
    result += "     )\n"
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_on_bl)
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_out_of_bl)
    result += "     )\n"
    # z direction expansion ratio
    result += "     1  1  1  1"
    result += " )\n"
    result += " hex ( 1 8 9 2 5 10 11 6 ) ( %g %g 1 )\n" % (round(parallelRefine*num_mesh_at_tail), round(normalRefine*(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer)))
    result += " edgeGrading\n"
    result += " (\n"
    # x direction expansion ratio
    result += " %g %g %g %g " % (expansion_ratio_tail, expansion_ratio_tail, expansion_ratio_tail, expansion_ratio_tail)
    # y direction expansion ratio
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_on_bl)
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_out_of_bl)
    result += "     )\n"
    result += " %g %g \n" % (expansion_ratio_at_outlet, expansion_ratio_at_outlet)
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_on_bl)
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), expansion_ratio_out_of_bl)
    result += "     )\n"
    # z direction expansion ratio
    result += " 1 1 1 1 \n"
    result += " )\n"
    result += " hex (3 12 16 0 7 13 17 4) (%g %g 1)\n" % (round(parallelRefine*(num_mesh_in_leading+num_mesh_in_trailing)), round(normalRefine*(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer)))
    result += " edgeGrading\n"
    result += " (\n"
    # x direction expansion ratio
    result += " %g " % (inlet_expansion_ratio_1)
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (separating_point_position, num_mesh_in_leading/(num_mesh_in_leading+num_mesh_in_trailing), expansion_ratio_in_leading)
    result += "         ( %g %g %g )\n" % (1-separating_point_position, 1-num_mesh_in_leading/(num_mesh_in_leading+num_mesh_in_trailing), expansion_ratio_trailing)
    result += "     )\n"
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (separating_point_position, num_mesh_in_leading/(num_mesh_in_leading+num_mesh_in_trailing), expansion_ratio_in_leading)
    result += "         ( %g %g %g )\n" % (1-separating_point_position, 1-num_mesh_in_leading/(num_mesh_in_leading+num_mesh_in_trailing), expansion_ratio_trailing)
    result += "     )\n"
    result += " %g " % (inlet_expansion_ratio_1)
    # y direction expansion ratio
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_out_of_bl)
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_on_bl)
    result += "     )\n"
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_out_of_bl)
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_on_bl)
    result += "     )\n"
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_out_of_bl)
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_on_bl)
    result += "     )\n"
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_out_of_bl)
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_on_bl)
    result += "     )\n"
    # z direction expansion ratio
    result += "  1 1 1 1 \n"
    result += " )\n"
    result += "\n"
    result += " hex ( 12 14 8 16 13 15 10 17 ) ( %g %g 1 ) \n" % (round(parallelRefine*num_mesh_at_tail), round(normalRefine*(num_mesh_on_boundary_layer + num_mesh_out_of_boundary_layer)))
    result += " edgeGrading\n"
    result += " (\n"
    # x direction expansion ratio
    result += " %g %g %g %g \n" % (expansion_ratio_tail, expansion_ratio_tail, expansion_ratio_tail, expansion_ratio_tail)
    # y direction expansion ratio
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_out_of_bl)
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_on_bl)
    result += "     )\n"
    result += " %g %g \n" % (1/expansion_ratio_at_outlet, 1/expansion_ratio_at_outlet)
    result += "     (\n"
    result += "         ( %g %g %g )\n" % (1-boundary_layer_thickness/inlet_x_dist, 1-num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_out_of_bl)
    result += "         ( %g %g %g )\n" % (boundary_layer_thickness/inlet_x_dist, num_mesh_on_boundary_layer/(num_mesh_on_boundary_layer+num_mesh_out_of_boundary_layer), 1/expansion_ratio_on_bl)
    result += "     )\n"
    # z direction expansion ratio
    result += "  1 1 1 1 \n"
    result += " )\n"
    result += ");\n"
    result += "\n"
    result += "edges\n"
    result += "(\n"
    result += " arc 3 2 ( %g %g %g )\n" % ( -inlet_x_dist*math.sin(math.pi/4)+1, inlet_x_dist*math.sin(math.pi/4), 0)
    result += " arc 7 6 ( %g %g %g )\n" % ( -inlet_x_dist*math.sin(math.pi/4)+1, inlet_x_dist*math.sin(math.pi/4), z_depth)
    result += " spline 1 0 \n"
    result += " (\n"
    for i in range(0, 49):
        result += "     ( %g %g 0 ) \n" % (pointList[i][0], pointList[i][1])
    result += " )\n"
    result += "\n"
    result += " spline 5 4 \n"
    result += " (\n"
    for i in range(0, 49):
        result += "     ( %g %g %g ) \n" % (pointList[i][0], pointList[i][1], z_depth)
    result += " )\n"
    result += "\n"
    result += " arc 3 12 ( %g %g 0 ) \n" % (-inlet_x_dist*math.sin(math.pi/4)+1, -inlet_x_dist*math.sin(math.pi/4))
    result += " arc 7 13 ( %g %g %g ) \n" % (-inlet_x_dist*math.sin(math.pi/4)+1, -inlet_x_dist*math.sin(math.pi/4), z_depth)
    result += "\n"
    result += " spline 0 16 \n"
    result += " (\n"
    for i in range(0, 49):
        result += "     ( %g %g %g ) \n" % (pointList[50+i][0], pointList[50+i][1], 0)
    result += " )\n"
    result += "\n"
    result += " spline 4 17 \n"
    result += " (\n"
    for i in range(0, 49):
        result += "     ( %g %g %g ) \n" % (pointList[50+i][0], pointList[50+i][1], z_depth)
    result += " )\n"
    result += "\n"
    result += ");\n"
    result += "\n"
    result += "faces\n"
    result += "(\n"
    result += ");\n"
    result += "\n"
    result += "faces\n"
    result += "(\n"
    result += ");\n"
    result += "\n"
    result += "defaultPatch\n"
    result += "{\n"
    result += " name frontAndBack;\n"
    result += " type empty;\n"
    result += "}\n"
    result += "\n"
    result += "boundary\n"
    result += "(\n"
    result += "inlet\n"
    result += " {\n"
    result += "     type patch; \n"
    result += "     faces \n"
    result += "     ( \n"
    result += "         ( 9 2 6 11 ) \n"
    result += "         ( 2 3 7 6 ) \n"
    result += "         ( 3 12 13 7 ) \n"
    result += "         ( 12 15 14 13 ) \n"
    result += "     ); \n"
    result += " }\n"
    result += "\n"
    result += "outlet\n"
    result += " {\n"
    result += "     type patch; \n"
    result += "     faces \n"
    result += "     (\n"
    result += "         ( 8 9 10 11 ) \n"
    result += "         ( 15 8 10 14 ) \n"
    result += "     );\n"
    result += " }\n"
    result += "\n"
    result += "walls\n"
    result += " {\n"
    result += "     type wall;\n"
    result += "     faces\n"
    result += "     (\n"
    result += "         ( 0 1 5 4 )\n"
    result += "         ( 0 4 17 16 )\n"
    result += "     );\n"
    result += " }\n"
    result += "\n"
    result += "interface1\n"
    result += " {\n"
    result += "     type patch;\n"
    result += "     faces\n"
    result += "     (\n"
    result += "         ( 1 8 10 5 )\n"
    result += "     );\n"
    result += " }\n"
    result += "interface2\n"
    result += " {\n"
    result += "     type patch;\n"
    result += "     faces\n"
    result += "     (\n"
    result += "         ( 16 17 10 8 )\n"
    result += "     );\n"
    result += " }\n"
    result += ");"
    result += "\n"
    result += "mergePatchPairs\n"
    result += "(\n"
    result += " ( interface1 interface2 )\n"
    result += ");\n"
    return result


