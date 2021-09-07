import numpy as np

p=0
def initLatency(n):         # initializing a 2d array for rho
    global p
    p = np.random.uniform(10,500,[n,n])

def computeLatency(i,j,m):  # computing the latency by taking both nodes and size of message
    lat = p[i.nid][j.nid]
    c = 0.0
    if i.speed == 1 and j.speed == 1:
        c = 100.0
    else:
        c = 5.0
    lat += m/c
    mean = 96.0/c
    lat += np.random.exponential(mean)
    return lat