from os import set_blocking
import sys
import math
import csv

#if __name__ == "__main__":
#
#	print(f"Arguments count: {len(sys.argv)}")
#	for i, arg in enumerate(sys.argv):
#		print(f"Argument {i:>6}: {arg}")
#
# parameters:
#
# 1 - Design coefficient of lift    (real, 0.05 to 1)
# 2 - Camber position & refex   (integer, 1 to 9)
# 3 - Thickness  (real, 1 to 30)
# 4 - distance to inlet (real, 1-??)
# 5 - distance to outlet (real, 1-??)
# 6 - Angle of response? attack? (0-60)

def print_usage():
	print(f"Usage: {sys.argv[0]} <mc> <mcp> <thick> <npoints>")
	print("")
	print("Where ")
	print("     <mc>: Max Camber (0 to 9.5)")
	print("    <mcp>: Max camber position (0 to 90)")
	print("  <thick>: Thickness (1 to 40)")
	print("<npoints>: number of points (defaults to 101)")
	print("") 

closed_trailing_edge = True

a_0 = 0.2969
a_1 = -0.126
a_2 = -0.3516
a_3 = 0.2843
a_4 = closed_trailing_edge * -0.1036 + (1-closed_trailing_edge) * -0.1015

def rotate_points(points, angle, pivot=[1,0]):
	print("Rotating angle: ")
	print(angle)
	return list(map(lambda x: [pivot[0] + (x[0]-pivot[0])*math.cos(math.radians(angle)) - (x[1]-pivot[1])*math.sin(math.radians(angle)), (x[0]-pivot[0])*math.sin(math.radians(angle)) + (x[1]+pivot[1])*math.cos(math.radians(angle)) + pivot[1]], points))

def generate_naca4_airfoil_points(mc, mcp, thick, npoints=101, angle=0, write_to_file=True):
	x_c 	= []
	y_c 	= []
	y_c_x 	= []
	y_t		= []
	s_u		= []
	s_l 	= []
	npoints = npoints // 2
	dbeta = math.pi / float(npoints)
	beta = 0.0
	print(mc)
	print(mcp)
	print(thick)
	print(npoints)
	mc 		= float(mc) / 100
	mcp 	= float(mcp) / 100
	thick 	= float(thick) / 100
	for i in range(npoints):
		x_u = 1.0 - (1.0 - math.cos(beta)) / 2.0
		x_l = (1.0 - math.cos(beta)) / 2.0
		if x_u < mcp:
			y = (mc/(mcp**2))*(2.0*mcp*x_u - x_u**2)
			y_x = ((2*mc)/(mcp**2))*(mcp - x_u)
		else:
			y = (mc/((1-mcp)**2))*(1.0 - 2.0*mcp + 2.0*mcp*x_u - x_u**2)
			y_x = ((2*mc)/((1-mcp)**2))*(mcp - x_u)
		t = (thick/0.2)*(a_0*x_u**0.5 + a_1*x_u + a_2*x_u**2 + a_3*x_u**3 + a_4*x_u**4)
		theta = math.atan(y_x)
		x_upper = x_u - t * math.sin(theta)
		y_upper = y + t * math.cos(theta)
		s_u.append([x_upper, y_upper])
		if x_l < mcp:
			y = (mc/(mcp**2))*(2.0*mcp*x_l - x_l**2)
			y_x = ((2*mc)/(mcp**2))*(mcp - x_l)
		else:
			y = (mc/((1-mcp)**2))*(1.0 - 2.0*mcp + 2.0*mcp*x_l - x_l**2)
			y_x = ((2*mc)/((1-mcp)**2))*(mcp - x_l)
		t = (thick/0.2)*(a_0*x_l**0.5 + a_1*x_l + a_2*x_l**2 + a_3*x_l**3 + a_4*x_l**4)
		theta = math.atan(y_x)
		x_lower = x_l + t * math.sin(theta)
		y_lower = y - t * math.cos(theta)
		s_l.append([x_lower, y_lower]) 
		x_c.append(x_l)
		y_c.append(y)
		y_c_x.append(y_x)
		beta += dbeta
	s_l.append([1,0])
	allpoints = [*s_u, *s_l]
	allpoints = rotate_points(allpoints, angle)
	if write_to_file:
		with open('camber.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for row in zip(x_c, y_c):
				writer.writerow(row)
		with open('surface.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for row in allpoints:
				writer.writerow(row)
	else:
		return allpoints


if(__name__ == "__main__"):
	if len(sys.argv) < 4:
		print_usage()
		quit()
	if len(sys.argv) < 5:
		npoints = 101
	else:
		npoints = int(sys.argv[4])
	mc 		= sys.argv[1]
	mcp 	= sys.argv[2]
	thick 	= sys.argv[3]
	print(generate_naca4_airfoil_points(mc, mcp, thick, npoints, 0, True))


