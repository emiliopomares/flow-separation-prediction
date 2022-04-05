import make_datapoint

out_file = "./dataset.csv"

max_datapoints = 250

def make_dataset():
    file_object = open(out_file, 'a')
    m = max_datapoints
    while(m>0):
        datapoint = make_datapoint.make_datapoint()    
        file_object.write( str(datapoint['inputs'][0]) + "," + str(datapoint['inputs'][1]) + "," + str(datapoint['inputs'][2]) + "," + str(datapoint['inputs'][3]) + "," + str(datapoint['inputs'][4]) + "," + str(datapoint['outputs'][0]) + "," + str(datapoint['outputs'][1]) + "\n")
        m -= 1
    file_object.close()
        

if __name__ == '__main__':
    make_dataset()