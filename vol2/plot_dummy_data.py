import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

def load(filename):
    with open(filename) as f:
        return np.array([
            [cell for cell in row]
            for row in csv.reader(f)
        ])


def main(filename):
    datatable = load(filename)
    heights = datatable[:, 0]
    weights = datatable[:, 1]
    plt.scatter(heights, weights)
    plt.show()

if __name__ == '__main__':
    main(sys.argv[1])
