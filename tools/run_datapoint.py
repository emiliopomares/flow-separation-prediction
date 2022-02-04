from config import config
import subprocess
import os
import sys
import read_geo
import flow_utils
import generate_0_U

angle = float(sys.argv[1]) if len(sys.argv) > 1 else 15
print("Using angle of attack: " + str(angle))

# run Allclean
print("Clearing previous solution...")
subprocess.run([config['project_path']+"Allclean"])

# prepare stuff
zeroUFilePath = config['project_path'] + "0/U"

file = generate_0_U.generate_0_U(18, angle)

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

print("Done")
