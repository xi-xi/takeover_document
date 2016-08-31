import numpy as np
from multiprocessing import Process

def single_process():
    for _ in range(5):
        hard_task()

def multi_process():
    ps = []
    for _ in range(5):
        ps.append(Process(target=hard_task))
        ps[-1].start()
    for p in ps:
        p.join()

def hard_task():
    mat = np.random.rand(500, 500)
    return np.linalg.eig(mat)
