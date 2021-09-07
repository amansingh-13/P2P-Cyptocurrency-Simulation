from node import Node
import numpy as np

p=0
def initLatency(n):
    global p
    p = np.random.uniform(10,500,[n,n])

def computeLatency(i,j,m):
    lat = p[i.nid][j.nid]
    c = 0
    if i.speed == 1 and j.speed == 1:
        c = 100
    else:
        c = 5
    lat += m/c
    mean = 96/c
    lat += np.random.exponential(mean)
    return lat