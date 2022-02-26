from config import config
from os import listdir
from os.path import isdir, join
import math

def find_latest_time_dir():
    output_path = config['project_path']
    onlydirs = [f for f in listdir(output_path) if isdir(output_path + '/' + f) and f.isnumeric()]
    to_amounts = list(map(lambda x: int(x), onlydirs))
    latest_dir = max(to_amounts)
    return str(latest_dir)

def norm(vec):
    return math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)

def sign_of(v):
    if v>0:
        return 1
    return -1

if __name__ == '__main__':
    d = find_latest_time_dir()
    print(d)