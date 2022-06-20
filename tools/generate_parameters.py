import numpy as np

# parameters ranges

min_aoa = 16
max_aoa = 16
min_Re = 1000
max_Re = 1000

naca4_max_camber_min = 4 #0
naca4_max_camber_max = 4 #9.5
naca4_max_camber_position_min = 40 #0
naca4_max_camber_position_max = 40 #90
naca4_thickness_min = 18 #1
naca4_thickness_max = 18 #40

L = 1 # chord line 1 m
nu = 1e-05 # air cinematic viscosity m²/s 

enable_turbulence = False

def make_aoa():
    return np.random.uniform(low=min_aoa, high=max_aoa, size=1)[0]
    
def make_Re():
    return np.random.uniform(low=min_Re, high=max_Re, size=1)[0]

def make_naca4():
    return [
        np.random.uniform(low=naca4_max_camber_min, high=naca4_max_camber_max, size=1)[0],
        np.random.uniform(low=naca4_max_camber_position_min, high=naca4_max_camber_position_max, size=1)[0],
        np.random.uniform(low=naca4_thickness_min, high=naca4_thickness_max, size=1)[0],
    ]

def Re_to_U(Re, _L=L, _nu=nu):
    u = Re*_nu/_L
    print("Freestream vel (m/s): " + str(u))
    return Re*_nu/_L

if __name__ == '__main__':
    for i in range(0,30):
        aoa = make_aoa()
        print(aoa)