import sys
import json

def main(filename):
    with open(filename) as f:
        data = json.load(f)
        print(data)

if __name__ == '__main__':
    main(sys.argv[1])
