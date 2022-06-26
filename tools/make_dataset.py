import make_datapoint
import push_result

max_datapoints = 10000

def make_dataset():
    m = max_datapoints
    while(m>0):
        datapoint = make_datapoint.make_datapoint()    
        push_result.push_result(datapoint['inputs'][0], datapoint['inputs'][1], datapoint['inputs'][2], datapoint['inputs'][3], datapoint['inputs'][4], datapoint['outputs'][0])
        m -= 1

if __name__ == '__main__':
    print("Using db user " + push_result.config['user'])
    print("Using db passwd " + push_result.config['password'])
    print("Using db host " + push_result.config['host'])
    make_dataset()