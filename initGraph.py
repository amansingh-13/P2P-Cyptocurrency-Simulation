import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

G = nx.Graph()

n = 15
md = int(np.log2(n))
nodes = np.empty(n, dtype=list)
nodes[0] = [1]
nodes[1] = [0]
for i in range(2,n):
    nc = np.random.randint(i)+1
    l = random.sample(range(0,i),min(nc,md))
    nodes[i] = sorted(l)
    for x in l:
        nodes[x] += [i]


for i in range(n):
    for x in nodes[i]:
        G.add_edge(i,x)
nx.draw(G)
plt.show()

s = 0
m = 0
for x in nodes:
    s += len(x)
    m = max(m,len(x))