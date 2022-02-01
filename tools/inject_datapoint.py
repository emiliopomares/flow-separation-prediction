import generate_datapoint
import os
from config import config

blockMeshDictPath = config['project_path'] + "system/blockMeshDict"

file = generate_datapoint.generate_example_datapoint()

with open(blockMeshDictPath, 'w') as f:
    f.write(file)