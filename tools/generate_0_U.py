import math
from config import config

def generate_0_U(velocity, angle):
    vel_x = velocity * math.cos(math.radians(angle))
    vel_y = velocity * math.sin(math.radians(angle))
    result = ""
    result += "/*--------------------------------*- C++ -*----------------------------------*\\n"
    result += "| =========                 |                                                 |\n"
    result += "| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n"
    result += "|  \\    /   O peration     | Version:  5                                     |\n"
    result += "|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |\n"
    result += "|    \\/     M anipulation  |                                                 |\n"
    result += "\*---------------------------------------------------------------------------*/\n"
    result += "FoamFile\n"
    result += "{\n"
    result += "    version     2.0;\n"
    result += "    format      ascii;\n"
    result += "    class       volVectorField;\n"
    result += "    object      U;\n"
    result += "}\n"
    result += "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
    result += "\n"
    result += "dimensions      [0 1 -1 0 0 0 0];\n"
    result += "\n"
    result += "internalField   uniform ("+str(vel_x)+" "+str(vel_y)+" 0);\n"
    result += "\n"
    result += "boundaryField\n"
    result += "{\n"
    result += "    inlet\n"
    result += "    {\n"
    result += "        type            freestream;\n"
    result += "        freestreamValue uniform ("+str(vel_x)+" "+str(vel_y)+" 0);\n"
    result += "    }\n"
    result += "\n"
    result += "    outlet\n"
    result += "    {\n"
    result += "        type            freestream;\n"
    result += "        freestreamValue uniform ("+str(vel_x)+" "+str(vel_y)+" 0);\n"
    result += "    }\n"
    result += "\n"
    result += "    walls\n"
    result += "    {\n"
    result += "        type            noSlip;\n"
    result += "    }\n"
    result += "\n"
    result += "    frontAndBack\n"
    result += "    {\n"
    result += "        type            empty;\n"
    result += "    }\n"
    result += "}\n"
    result += "\n"
    result += "// ************************************************************************* //\n"
    return result


if __name__ == '__main__':
    
    zeroUFilePath = config['project_path'] + "0/U"

    file = generate_0_U(18, 20)

    with open(zeroUFilePath, 'w') as f:
        f.write(file)