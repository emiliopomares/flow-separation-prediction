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

def make_datapoint(newData=True):

    # Prepare paths
    blockMeshDictPath = config['project_path'] + "system/blockMeshDict"
    zeroUFilePath = config['project_path'] + "0/U"

    if newData:

        # run Allclean
        print("Clearing previous solution...")
        subprocess.run([config['project_path']+"Allclean"])

        # select parameters

        angle = generate_parameters.make_aoa()
        Re = generate_parameters.make_Re()
        U = generate_parameters.Re_to_U(Re)
        mc, mcp, th = generate_parameters.make_naca4() 
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

    #read geo
    (nFaces, wallStartFace) = read_geo.read_wall_start_face()
    print(nFaces)
    print(wallStartFace)
    g = read_geo.read_geo()

    s = flow_utils.find_separation_point(g)

    print(s)

    output = flow_utils.make_result_from_separation_points(angle, s)

    print("output:  " + str(output['upper_sep_point']) + ", " + str(output['lower_sep_point']))

    print("Done")

    return {'inputs': [ angle, Re, mc, mcp, th ], 'outputs': [output['upper_sep_point'], output['lower_sep_point']]}

if __name__ == '__main__':
    print(make_datapoint(True))