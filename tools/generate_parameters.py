import numpy as np

# parameters ranges

min_aoa = 7
max_aoa = 25
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
    return np.random.uniform(low=0, high=22, size=1)[0]
    if np.random.uniform(low=0, high=1, size=1)[0] < 0.75:
        return abs(np.random.normal(7.2, 4**0.5, size=1)[0])
    else:
        # bimodal
        if np.random.uniform(low=0, high=1, size=1)[0] < 0.33:
            return abs(np.random.normal(2, 2**0.5, size=1)[0])
        elif np.random.uniform(low=0, high=1, size=1)[0] > 0.66:
            return abs(np.random.normal(22, 4**0.5, size=1)[0])
        else:
            return np.random.normal((min_aoa+max_aoa)/2, 4.5**0.5, size=1)[0]

def make_Re():
    #return 1000
    # bimodal
    #if np.random.uniform(low=0, high=1, size=1)[0] > 0.75:
    #    return np.random.uniform(low=min_Re, high=min_Re*10, size=1)[0]
    #else:
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

if __name__ == '__main__':
    for i in range(0,30):
        aoa = make_aoa()
        print(aoa)