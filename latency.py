import numpy as np

p=0
def initLatency(n):
    global p
    p = np.random.uniform(10,500,[n,n])

def computeLatency(i,j,m):
    lat = p[i.nid][j.nid]
    c = 0.0
    if i.speed == 1 and j.speed == 1:
        c = 100.0
    else:
        c = 5.0
    lat += m/c
    mean = 96.0/c
    # print(mean)
    lat += np.random.exponential(mean)
    # print("lat="+str(lat))
    return lat