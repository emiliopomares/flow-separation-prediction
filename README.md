# flow-separation-prediction
Flow separation prediction.

The goal of this project is to generate the dataset and train a model to predict the **point of flow separation** over the profile of a NACA parametrized airfoil.

An example of NACA airfoil profile:
<img src="media/NACA_profile.jpg" alt="NACA profile" style="width: 800px;">

To generate the dataset, multiple passes of a simulation are run under different conditions (Reynold's number and angle of attack), and the point of flow separation (if separation occurs) is measured from simulation data and annotated into the dataset.

OpenFOAM was used to run the simulations using the SIMPLE solver:
![simulation](media/openfoam-simulation.jpg)

A convergence study was carried out to determine how fine the simulation domain grid should be. The mesh was refined until convergence (change below threshold) was achieved.
<img src="media/grid-size-convergence.jpg" alt="Grid size convergence" style="width: 800px;">

The result was a trained model that, within the tight restrictions of the project, produced a result accurate within 2%.


A plot of the learnt function for different values of Re and angle of attack:
<img src="media/learnt-function.jpg" alt="Learnt Function" style="width: 800px;">

It was also interesting to visualize the separation/no separation boundary in parameter space:
<img src="media/separation-boundary.jpg" alt="Separation boundary" style="width: 800px;">

This project was awarded top marks by the Commitee.
