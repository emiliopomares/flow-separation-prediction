from re import X
import mysql.connector
import os

config = {
  'user': os.environ.get('DB_USER', 'flow'),
  'password': os.environ.get('DB_PASSWD', 'abcABC12345%'),
  'host': os.environ.get('DB_HOST', '165.232.146.23'),
  'database': 'simulation_results',
  'raise_on_warnings': True
}

def push_result(aoa, re, mc, mcp, thick, x):
  print("push result called, config: " + str(config))
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor()
  add_datapoint = "INSERT INTO Datapoints VALUES (0, " + str(aoa) + ", " + str(re) + ", " + str(mc) + ", " + str(mcp) + ", " + str(thick) + ", " + str(x) + ")"
  print("Executing query: " + add_datapoint)
  cursor.execute(add_datapoint)
  cnx.commit()
  cursor.close()
  cnx.close()
  return

if __name__ == '__main__':
    print(str(config))
    aoa     = 2.23
    re      = 2000.0
    mc 		= 12
    mcp 	= 14
    thick 	= 16
    sep_x   = 0.73
    push_result(aoa, re, mc, mcp, thick, sep_x)