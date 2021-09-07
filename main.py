import numpy as np
import heapq
from transaction import Transaction
from event import *

def sample_exp(mean):
    return np.random.exponential(mean)

eventq = []

def pushq(event):
    heapq.heapppush(eventq, (event.time, event))

class Simulation:
    def __init__(self, txngen_mean, no_nodes, slow, ttmine):
        no_slow = len(int(slow*no_nodes))
        self.gblock = Block(pbid=0, bid=1, txnIncluded=set(), miner=-1)
        self.gblock.balance = [0]*no_nodes
        self.nodes = [
            Node(nid=i, speed=0, genesis=gblock, miningtime=ttmine[i])
            for i in range(no_slow)
        ] + [
            Node(nid=i, speed=1, genesis=gblockm, miningtime=ttmine[i])
            for i in range(no_slow, no_nodes)
        ]
        self.txngen_mean = txngen_mean

    def generate_network(self, degree=degree):
        #for p in nodes:
        #    for _ in range(degree):
        #        p.adj.add(nodes[np.random.randint(0,len(nodes))])

    def gen_all_txn(self, max_time):
        for p in self.nodes:
            
            minetime = sample_exp(p.miningtime)
            block2mine = Block(
                pbid=self.gblock,
                bid=np.random.randint(0, 2**128-1),
                txnIncluded=set(Transaction(
                    sender=-1,
                    tid=np.random.randint(0, 2**128-1)
                    receiver=p
                )),
                miner=p
            )
            heapq.heapppush(eventq, (minetime, BlockMined(minetime, block2mine)))
            
            t = sample_exp(self.txngen_mean)
            while(t < max_time):
                elem = Transaction(
                    sender=p,
                    tid = np.random.randint(0, 2**128-1),
                    receiver = self.nodes[np.random.randint(0,len(self.nodes))],
                    value = 0,
                )
                heapq.heapppush(eventq, (t, TxnGen(time=t, txn=elem)))
                t = t + sample_exp(self.txngen_mean)

    def run(self, max_time):
        t = 0
        while(t < max_time):
            t, event = heapq.heappop(eventq)
            handle(event)

    def handle(self, event):
        if(event.eventId == 1):
            event.sender.txnSend(event, )
            
            
                
            
        