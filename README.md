# flow-separation-prediction
Flow separation prediction.

The goal of this project is to generate the dataset and train a model to predict the **point of flow separation** over the profile of a NACA parametrized airfoil.

<img src="media/NACA-profile.jpg" alt="NACA profile" style="width: 300px;">

To generate the dataset, multiple passes of a simulation are run under different conditions (Reynold's number and angle of attack), and the point of flow separation (if separation occurs) is measured from simulation data and annotated into the dataset.
![simulation](media/openfoam-simulation.jpg)
