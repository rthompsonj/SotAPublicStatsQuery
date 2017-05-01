import json
import sys

def read_data(input):    
    with open(input, 'r') as f:
        lines = f.read()
    data = json.loads(lines)
    return data        

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input = sys.argv[1]
    else:
        input = 'output.json'
    read_data(input)
