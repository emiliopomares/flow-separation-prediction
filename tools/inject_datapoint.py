import generate_datapoint
import os

blockMeshDictPath = os.getcwd() + "/../openfoam/run/Airfold2D_full/system/blockMeshDict"

file = generate_datapoint.generate_example_datapoint()

with open(blockMeshDictPath, 'w') as f:
    f.write(file)