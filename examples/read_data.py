import json
import sys

def read_data(input):    
    with open(input, 'r') as f:
        data = json.loads(f.read())
    return data        

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input = sys.argv[1]
    else:
        input = 'output.json'
    data = read_data(input)
