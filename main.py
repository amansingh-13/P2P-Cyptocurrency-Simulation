import numpy as np
import heapq

def sample_exp(mean):
    return np.random.exponential(mean)

class Simulation:

    def __init__(self, txngen_mean, no_peers = 5):
        self.peers = [Peer(...) for i in range(no_peers)]
        self.eventq = heapq.heapify([])
        self.txngen_mean = txngen_mean

    def generate_network(self, degree=2):
        for p in peers:
            for _ in range(degree):
                p.adj.add(peers[np.random.randint(0,len(peers))])

    def gen_all_txn(self, max_time):
        for p in peers:
            t = sample_exp(txngen_mean)
            while(t < max_time):
                heapq.heapppush(eventq, (t, TxnGen(...)))
                t = t+sample_exp(txngen_mean)

    def run(self, max_time):
        t = 0
        while(t < max_time):
            t, event = heapq.heappop(eventq)
            handle(event)

    def handle(self, event):
        if(event.eventid == 0):
            event.sender.
            
            
                
            
        