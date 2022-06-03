from config import config
import subprocess
import generate_datapoint
import os
import sys
import read_geo
import flow_utils
import generate_0_U
from generate_blockMesh import *
from generate_naca5 import *
from generate_naca4 import *
import generate_parameters

# This is the script to generate the training dataset

def make_datapoint():
    return make_datapoint_with_params(0, 0, 0, 0, 0, True, True)

def make_datapoint_with_params(aoa, re, _mc, _mcp, _thick, newData=True, generate=True):

    # Prepare paths
    blockMeshDictPath = config['project_path'] + "system/blockMeshDict"
    zeroUFilePath = config['project_path'] + "0/U"

    if newData:

        # run Allclean
        print("Clearing previous solution...")
        subprocess.run([config['project_path']+"Allclean"])

        # select parameters

        angle = generate_parameters.make_aoa()
        
        if(not generate):
            angle = aoa
        print("Selected aoa: " + str(angle))
        Re = generate_parameters.make_Re()
        
        if(not generate):
            Re = re
        print("Selected Re: " + str(Re))
        U = generate_parameters.Re_to_U(Re)
        mc, mcp, th = generate_parameters.make_naca4() 
        if(not generate):
            mc = _mc
            mcp = _mcp
            th = thick

        print("Input for this datapoint:  angle " + str(angle) + ", Re/free stream vel " + str(Re)+"/"+str(U) + ", mc " + str(mc) + ", mcp " + str(mcp) + ", th " + str(th))

        # Generate a blockmesh
        points = generate_naca4_airfoil_points(mc, mcp, th, 101, 0, False)
        file = generate_blockMesh(points, 0, 12, 20) # these last three parameters, 0, 12 and 20, see what we do with them...

        with open(blockMeshDictPath, 'w') as f:
            f.write(file)

        os.chdir(config['project_path'])
        subprocess.run(["blockMesh"])
        file = generate_0_U.generate_0_U(U, angle) # fix aoa and free stream velocity here

        with open(zeroUFilePath, 'w') as f:
            f.write(file)

        # run Allrun
        print("Simulating...")
        subprocess.run([config['project_path']+"Allrun"])
        # run postprocess
        print("Postprocessing...")
        os.chdir(config['project_path'])
        subprocess.run(["simpleFoam", "-postProcess", "-func", "wallShearStress"])
        subprocess.run(["simpleFoam", "-postProcess", "-func", "yPlus"])

    #read geo
    (nFaces, wallStartFace) = read_geo.read_wall_start_face()
    print(nFaces)
    print(wallStartFace)
    g = read_geo.read_geo()

    print("Boundary start face: " + str(g.get_boundary_start_face()))
    sf = g.get_boundary_start_face()
    print("A boundary face: " + str(g.get_face_vertices_by_index(sf)))
    print("Area of the face: " + str(g.get_face_area(sf)))
    print("Axis at that face: " + str(g.get_face_normals_unit_by_index(sf)))

    s = flow_utils.find_separation_point(g)

    print(s)

    print("Done")

    datapoint = {'inputs': [ angle, Re, mc, mcp, th ], 'outputs': [s]}
    print("  The datapoint: " + str(datapoint))
    return datapoint

if __name__ == '__main__':
    aoa     = float(sys.argv[1])
    re      = float(sys.argv[2])
    mc 		= float(sys.argv[3])
    mcp 	= float(sys.argv[4])
    thick 	= float(sys.argv[5])
    print(make_datapoint_with_params(aoa, re, mc, mcp, thick, True, False))