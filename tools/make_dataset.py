import make_datapoint
import push_result

max_datapoints = 250

def make_dataset():
    m = max_datapoints
    while(m>0):
        datapoint = make_datapoint.make_datapoint()    
        push_result.push_result(datapoint['inputs'][0], datapoint['inputs'][1], datapoint['inputs'][2], datapoint['inputs'][3], datapoint['inputs'][4], datapoint['outputs'][0])
        m -= 1

if __name__ == '__main__':
    make_dataset()