import numpy as np
import heapq
from transaction import Transaction
from event import *

def sample_exp(mean):
    return np.random.exponential(mean)

gblock = Block(pbid=0, bid=1, set())

class Simulation:
    def __init__(self, txngen_mean, no_nodes, slow):
        no_slow = len(int(slow*no_nodes))
        self.nodes = [
            Node(nid=i, speed=0, genesis=gblock)
            for i in range(no_slow)
        ] + [
            Node(nid=i+no_slow, speed=1, genesis=gblock)
            for i range(no_nodes-no_slow)
        ]
        self.eventq = heapq.heapify([])
        self.txngen_mean = txngen_mean

    def generate_network(self, degree=2):
        for p in nodes:
            for _ in range(degree):
                p.adj.add(nodes[np.random.randint(0,len(nodes))])

    def gen_all_txn(self, max_time):
        count = 0
        for p in nodes:
            t = sample_exp(txngen_mean)
            while(t < max_time):
                elem = Transaction(sender=p.id, tid=count)
                heapq.heapppush(eventq, (t, TxnGen()))
                t = t + sample_exp(txngen_mean)
                count += 1

    def run(self, max_time):
        t = 0
        while(t < max_time):
            t, event = heapq.heappop(eventq)
            handle(event)

    def handle(self, event):
        if(event.eventid == 0):
            event.sender.
            
            
                
            
        