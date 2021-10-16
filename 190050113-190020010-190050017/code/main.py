import numpy as np
import heapq
from node import Node
from transaction import Transaction
from event import *
import networkx as nx
import matplotlib.pyplot as plt
from queue import eventq, pushq
import random
from utils import *
from params import *

def sample_exp(mean):
    return np.random.exponential(mean)

class Simulation:
    def __init__(self, txngen_mean, no_nodes, slow, ttmine):
        """
        Initializes the simulation object
        """
        no_slow = int(slow*no_nodes)
        self.G = nx.Graph()
        self.gblock = Block(pbid=0, bid=1, txnIncluded=set(), miner=-1)
        self.gblock.balance = [0]*no_nodes
        self.nodes = [
            Node(nid=i, speed=0, genesis=self.gblock, miningTime=ttmine[i])
            for i in range(no_slow)
        ] + [
            Node(nid=i, speed=1, genesis=self.gblock, miningTime=ttmine[i])
            for i in range(no_slow, no_nodes)
        ]
        self.txngen_mean = txngen_mean
        initLatency(no_nodes)


    def generate_network(self):
        """
        Generates an appropriate network by connecting nodes
        """
        n = len(self.nodes)
        md = int(np.log2(n))
        self.G.add_edge(0,1)
        self.nodes[0].addPeer(self.nodes[1])
        self.nodes[1].addPeer(self.nodes[0])
        for i in range(2,n):
            nc = np.random.randint(i)+1
            l = random.sample(range(0,i),min(nc,md))
            l = sorted(l)
            for x in l:
                self.G.add_edge(i,x)
                self.nodes[x].addPeer(self.nodes[i])
                self.nodes[i].addPeer(self.nodes[x])

    def print_graph(self):        
        """
        print the graph to visualize the network
        """

        nx.draw(self.G)
        plt.show()

    def gen_all_txn(self, max_time):
        """
        Add all transaction events and start mining on the genesis
        block in the simulation queue (including only the coinbase txn)
        """
        for p in self.nodes:

            # generate block on genesis
            minetime = sample_exp(p.miningTime)
            block2mine = Block(
                pbid=self.gblock,
                bid=np.random.randint(0, 2**31-1),
                txnIncluded=set([Transaction(
                    sender=-1,
                    tid=np.random.randint(0, 2**31-1),
                    receiver=p,
                    value=50
                )]),
                miner=p
            )
            # add mining finish times to event queue
            pushq(BlockMined(minetime, block2mine))
            
            # generate transactions based on the mean interarrival time
            t = sample_exp(self.txngen_mean)
            while(t < max_time):
                elem = Transaction(
                    sender=p,
                    tid = np.random.randint(0, 2**31-1),
                    receiver = self.nodes[np.random.randint(0,len(self.nodes))],
                    value = 0,
                )
                
                pushq(TxnGen(time=t, txn=elem))
                t = t + sample_exp(self.txngen_mean)

    def run(self, max_time):
        """
        Runs simulation for `max_time`
        """
        t = 0
        while(t < max_time and len(eventq)!=0):
            t, event = heapq.heappop(eventq)
            # print (f"Time: {t}")
            self.handle(event)
        file=open("log_tree.txt","w+")
        for a in self.nodes:
            heading="*"*100+f"Id:{a.nid}"+"*"*100+"\n"
            file.write(heading)
            for block in a.blockchain.blocks.values():
                if block.pbid == 0: 
                    log_to_write=f"Id:{pretty(block.bid)}, Parent:{pretty(-1)}, Miner: {block.miner}, Txns:{pretty(len(block.txnIncluded), 5)}, Time:{block.time}\n"
                else:
                    log_to_write=f"Id:{pretty(block.bid)}, Parent:{pretty(block.pbid.bid)}, Miner: {block.miner}, Txns:{pretty(len(block.txnIncluded), 5)}, Time:{block.time}\n"
                file.write(log_to_write)
            


    def handle(self, event):
        """
        Calls the appropriate event handler for latest event
        """
        if(event.eventId == 1):
            event.txn.sender.txnSend(event)
        elif(event.eventId == 2):
            event.receiver.txnRecv(event)
        elif(event.eventId == 3):
            event.receiver.verifyAndAddReceivedBlock(event)
        elif(event.eventId == 4):
            event.block.miner.receiveSelfMinedBlock(event)
        else:
            print("bug in simulation.handle()")

    def draw_bc(self, nid):
        colormap = []
        for node in self.nodes[nid].blockchain.g:
            if(node == 1): colormap.append('red')
            else: colormap.append('blue')
        nx.draw(self.nodes[nid].blockchain.g, 
                nx.drawing.nx_agraph.graphviz_layout(self.nodes[nid].blockchain.g, prog='dot'),
                node_color=colormap,
                node_size=20,
                arrowsize=5)
        plt.show()
            
            
if __name__ == "__main__":
    mean_inter_arrival = 100
    num_nodes = NUM_NODES
    percentage_slow = 0.6 # (in decimals)
    
    # mean_mining_time = [25000]*10
    # simulation_time = 400000
    mean_mining_time = [10000]*NUM_NODES
    simulation_time = 40000

    simulator = Simulation(mean_inter_arrival,num_nodes,percentage_slow,mean_mining_time)
    simulator.generate_network()
    # simulator.print_graph()
    simulator.gen_all_txn(simulation_time)
    simulator.run(simulation_time)

    # draw bc
    # for i in range(NUM_NODES):
    #         simulator.draw_bc(i)