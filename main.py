import numpy as np
import heapq



class Simulation:

    def __init__(self):
        self.peers = [Peer(...) for i in range(5)]
        self.eventq = heapq.heapify([])
        self.curr_time = 0

    def generate_network(self):
        for p in self.peers:
            for i in range(len(self.peers)):

    
    

