from os import set_blocking
import sys
import math
import csv

def print_usage():
	print(f"Usage: {sys.argv[0]} <mc> <mcp> <thick> <npoints>")
	print("")
	print("Where ")
	print("    <dcl>: Design coefficient of lift (0.05 to 1)")
	print("    <mcp>: Max camber position (5-std- or 10-ref- to 25, mutiple of 5)")
	print("    <ref>: Standard or reflexed camber (0 or 1)")
	print("  <thick>: Thickness (1 to 30)")
	print("<npoints>: number of points (defaults to 101)")
	print("") 

closed_trailing_edge = True

a_0 = 0.2969
a_1 = -0.126
a_2 = -0.3516
a_3 = 0.2843
a_4 = closed_trailing_edge * -0.1036 + (1-closed_trailing_edge) * -0.1015

r_std = [
	0.0580,
	0.1260,
	0.2025,
	0.2900,
	0.3910
]

k1_std = [
	361.400,
	51.640,
	15.957,
	6.643,
	3.230
]

r_ref = [
	0,
	0.1300,
	0.2170,
	0.3180,
	0.4410
]

k1_ref = [
	0,
	51.990,
	15.793,
	6.520,
	3.191
]

k2_over_k1_std = [
	0,
	0,
	0,
	0,
	0
]

k2_over_k1_ref = [
	0,
	0.000764,
	0.00677,
	0.0303,
	0.1355
]

def camber_line_y_std_front(x, r, k1, k2_over_k1):
	return (k1/6)*(x**3 - 3*r*x**2 + r**2*(3-r)*x)

def camber_line_grad_std_front(x, r, k1, k2_over_k1):
	return (k1/6)*(3*x**2 - 6*r*x + r**2*(3-r))

def camber_line_y_ref_front(x, r, k1, k2_over_k1):
	return (k1/6)*((x-r)**3 - k2_over_k1*(1-r)**3*x - r**3*x + r**3)

def camber_line_grad_ref_front(x, r, k1, k2_over_k1):
	return (k1/6)*(3*(x-r)**2 - k2_over_k1*(1-r)**3 - r**3)


def camber_line_y_std_back(x, r, k1, k2_over_k1):
	return ((k1*r**3)/6)*(1-x)

def camber_line_grad_std_back(x, r, k1, k2_over_k1):
	return -(k1*r**3)/6

def camber_line_y_ref_back(x, r, k1, k2_over_k1):
	return (k1/6)*(k2_over_k1*(x-r)**3-k2_over_k1*(1-r)**3*x-r**3*x+r**3)

def camber_line_grad_ref_back(x, r, k1, k2_over_k1):
	return (k1/6)*(3*k2_over_k1*(x-r)**2-k2_over_k1*(1-r)**3*x-r**3)

generators = {
	0:
	{
		'y_front': camber_line_y_std_front,
		'grad_front': camber_line_grad_std_front,
		'y_back': camber_line_y_std_back,
		'grad_back': camber_line_grad_std_back,
		'r': r_std,
		'k1': k1_std,
		'k2_over_k1': k2_over_k1_std
	},
	1:
	{
		'y_front': camber_line_y_ref_front,
		'grad_front': camber_line_grad_ref_front,
		'y_back': camber_line_y_ref_back,
		'grad_back': camber_line_grad_ref_back,
		'r': r_ref,
		'k1': k1_ref,
		'k2_over_k1': k2_over_k1_ref
	}
}

def generate_airfoil_points(dcl, mcp_index, ref, thick, npoints=101, write_to_file=True):
	s_u			= []
	s_l 		= []
	r 			= generators[ref]['r'][mcp_index]
	k1 			= generators[ref]['k1'][mcp_index]
	k2_over_k1 	= generators[ref]['k2_over_k1'][mcp_index]
	dbeta = math.pi / float(npoints)
	beta = 0.0
	for i in range(npoints):
		x_c = (1.0 - math.cos(beta)) / 2.0
		if x_c<r:
			y_c = (dcl/0.3) * generators[ref]['y_front'](x_c, r, k1, k2_over_k1)
			y_x = (dcl/0.3) * generators[ref]['grad_front'](x_c, r, k1, k2_over_k1)
		else:
			y_c = (dcl/0.3) * generators[ref]['y_back'](x_c, r, k1, k2_over_k1)
			y_x = (dcl/0.3) * generators[ref]['grad_back'](x_c, r, k1, k2_over_k1)
		t = (thick/0.2)*(a_0*x_c**0.5 + a_1*x_c + a_2*x_c**2 + a_3*x_c**3 + a_4*x_c**4)
		theta = math.atan(y_x)
		x_upper = x_c - t * math.sin(theta)
		x_lower = x_c + t * math.sin(theta)
		y_upper = y_c + t * math.cos(theta)
		y_lower = y_c - t * math.cos(theta)
		s_u.append([x_upper, y_upper])
		s_l.append([x_lower, y_lower]) 
		beta += dbeta
	if write_to_file:
		with open('surface.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for row in s_u:
				writer.writerow(row)
			for row in s_l:
				writer.writerow(row)


if len(sys.argv) < 5:
	print_usage()
	quit()

if len(sys.argv) < 6:
	npoints = 101
else:
	npoints = int(sys.argv[5])

def validate_dcl(dcl):
	if dcl < 0.05 or dcl > 1:
		print_usage()
		quit()

def validate_ref(ref):
	if(ref != 0 and ref != 1):
		print_usage()
		quit()

def validate_mcp(ref, mcp):
	if(mcp != 5 and mcp != 10 and mcp != 15 and mcp != 20 and mcp != 25):
		print_usage()
		quit()
	if(mcp == 5 and ref == 0):
		print_usage()
		quit()

def validate_thick(thick):
	if(thick < 0.01 or thick > 0.3):
		print_usage()
		quit()

dcl 	= float(sys.argv[1])
validate_dcl(dcl)
ref		= int(sys.argv[3])
validate_ref(ref)
mcp 	= int(sys.argv[2])
validate_mcp(ref, mcp)
thick 	= float(sys.argv[4]) / 100
validate_thick(thick)

generate_airfoil_points(dcl, (mcp-5)//5, ref, thick, npoints)


