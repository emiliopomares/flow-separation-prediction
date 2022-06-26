from re import X
import mysql.connector
import os
import json

config = {
  'user': os.environ.get('DB_USER', 'flow'),
  'password': os.environ.get('DB_PASSWD', 'abcABC12345%'),
  'host': os.environ.get('DB_HOST', '165.232.146.23'),
  'database': 'simulation_results',
  'raise_on_warnings': True
}

def retrieve_results():
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor()
  retrieve_datapoints = "SELECT * FROM Datapoints"
  cursor.execute(retrieve_datapoints)
  results = cursor.fetchall()
  cursor.close()
  cnx.close()
  return results

if __name__ == '__main__':
    obj = "dataset = " + json.dumps(retrieve_results())
    print(obj)