import generate_datapoint
import generate_0_U
import os
from config import config

blockMeshDictPath = config['project_path'] + "system/blockMeshDict"

file = generate_datapoint.generate_example_datapoint()

with open(blockMeshDictPath, 'w') as f:
    f.write(file)

zeroUFilePath = config['project_path'] + "0/U"

file = generate_0_U(18, 45)

with open(zeroUFilePath, 'w') as f:
    f.write(file)