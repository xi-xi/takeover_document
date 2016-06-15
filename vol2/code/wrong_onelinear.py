import csv


def load_csv(filename):
    with open(filename) as f:
        return [
            [cell for cell in row]
            for row in csv.reader(f)
        ]
