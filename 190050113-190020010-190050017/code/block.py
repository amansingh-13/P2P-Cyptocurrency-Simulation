import copy 
from utils import pretty
from params import *
import networkx as nx

# This data structure contains all the details of a single block and the blockchain

class Blockchain:
    def __init__(self, gblock):
        self.blocks = {gblock.bid : (gblock, 0)}
        self.head = gblock
        self.g = nx.DiGraph()
    
    def add_block(self, block, time):
        self.blocks[block.bid] = (block, time)
        self.g.add_edge(block.bid, block.pbid.bid)
        if(block.length > self.head.length):
            self.head = block
            return True
        return False   

    def balance(self, nid):
        return self.head.balance[nid]

class Block:
    def __init__(self, bid, pbid, txnIncluded, miner, time=0):
        self.bid = bid # block id
        self.pbid = pbid # parent block id
        self.txnIncluded = txnIncluded.copy()
        self.miner = miner
        self.time = time

        # txnPool stores all the txn mined till now 
        # length shows the length of chain from genesis block till current block 
        if pbid != 0:
            self.txnPool = pbid.txnPool
            self.length = pbid.length+1
        else:
            self.txnPool = set()
            self.length = 1
        
        if pbid != 0:
            self.balance = pbid.balance.copy()
        else:
            self.balance = [0]*NUM_NODES

        for a in self.txnIncluded: # updating balance of all the user 
            if a.sender != -1:
                self.balance[a.sender.nid] -= a.value
            self.balance[a.receiver.nid] += a.value

        # no need to check parent  
        self.is_valid = True
        for a in self.txnIncluded:
            if a in self.txnPool:
                #print("debug a", a)
                self.is_valid = False
        for b in self.balance:
            if(b < 0):
                #print("debug b", self.balance)
                self.is_valid = False

        for a in self.txnIncluded:
            self.txnPool.add(a)
            
    def __str__ (self):
        return f"Id:{pretty(self.bid)}, Parent:{pretty(self.pbid.bid)}, Miner: {self.miner}, Txns:{pretty(len(self.txnIncluded), 5)}, Time:{pretty(self.time,10)}"