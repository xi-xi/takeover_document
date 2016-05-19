import sys
import numpy.random as nr


def create_dummy_field():
    height = nr.normal(170.0, 5.0)
    weight = nr.normal(height - 105.0, 10.0)
    return height, weight


def main(filename):
    n = 1000
    with open(filename, "w") as f:
        for _ in range(n):
            field = create_dummy_field()
            f.write(",".join([str(cell) for cell in field]) + "\n")

if __name__ == '__main__':
    main(sys.argv[1])
