#import sys

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

#def print_usage():
#	print(f"Usage: {sys.argv[0]} <dc> <cpr> <thick> <din> <dout> <aa>")
#	print("")
#	print("Where ")
#	print("    <dc>: Desgien coefficient of list (0.05 to 1)")
#	print("   <cpr>: Camber position & refex  (integer, 1 to 9)")
#	print(" <thick>: Thickness (1 to 30)")
#	print("   <din>: Distance to inlet (1-20)")
#	print("  <dout>: Distance to outlet (1-20)")
#	print("    <aa>: Angle of attack (0-60)")
#	print("") 


#def generate_airfoil_points(fc, cpr, thick, npoints=101):
#	result = []
#	for i in range(npoints):
		

#if len(sys.argv) < 7:
#	print_usage() 


