import numpy as np

def load():
    return [["1", "2", "3"], ["4", "5", "6"]]

def display():
    a = load()
    np.array(a)
    fp1 = open("csv1.csv", "w")
    for row in a:
        fp1.write(",".join(row) + "\n")
    # fp1.write(str(np.array(a)))

if __name__ == '__main__':
    display()

