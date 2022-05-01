import numpy as np

# parameters ranges

min_aoa = 5
max_aoa = 15
min_Re = 20
max_Re = 2000

naca4_max_camber_min = 0
naca4_max_camber_max = 9.5
naca4_max_camber_position_min = 0
naca4_max_camber_position_max = 90
naca4_thickness_min = 1
naca4_thickness_max = 40

L = 1 # chord line 1 m
nu = 1e-05 # air cinematic viscosity m²/s 

def make_aoa():
    return np.random.normal((min_aoa+max_aoa)/2, 4**0.5, size=1)[0]

def make_Re():
    return np.random.uniform(low=min_Re, high=max_Re, size=1)[0]

def make_naca4():
    return [
        4, #np.random.uniform(low=naca4_max_camber_min, high=naca4_max_camber_max, size=1)[0],
        40, #np.random.uniform(low=naca4_max_camber_position_min, high=naca4_max_camber_position_max, size=1)[0],
        18 #np.random.uniform(low=naca4_thickness_min, high=naca4_thickness_max, size=1)[0],
    ]

def Re_to_U(Re, _L=L, _nu=nu):
    u = Re*_nu/_L
    print("Freestream vel (m/s): " + str(u))
    return Re*_nu/_L