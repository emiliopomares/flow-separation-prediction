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


def generate_airfoil_points(mc, mcp, thick, npoints=101, write_to_file=True):
	x_c 	= []
	y_c 	= []
	y_c_x 	= []
	dbeta = math.pi / float(npoints)
	beta = 0.0
	for i in range(npoints):
		x = (1.0 - math.cos(beta)) / 2.0
		if x < mcp:
			y = (mc/(mcp**2))*(2.0*mcp*x - x**2)
		else:
			y = (mc/((1-mcp)**2))*(1.0 - 2.0*mcp + 2.0*mcp*x - x**2)
		x_c.append(x)
		y_c.append(y)
		beta += dbeta
	if write_to_file:
		with open('camber.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for row in zip(x_c, y_c):
				writer.writerow(row)

if len(sys.argv) < 4:
	print_usage()
	quit()

if len(sys.argv) < 5:
	npoints = 101
else:
	npoints = int(sys.argv[4])

mc 		= float(sys.argv[1]) / 100
mcp 	= float(sys.argv[2]) / 100
thick 	= float(sys.argv[3]) / 100

generate_airfoil_points(mc, mcp, thick, npoints)


