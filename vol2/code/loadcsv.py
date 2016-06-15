import sys
import csv


def main(filename):
    with open(filename) as f:
        for row in csv.reader(f):
            for cell in row:
                print(cell)

if __name__ == '__main__':
    main(sys.argv[1])
