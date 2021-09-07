import copy 
from block import Block
from transaction import Transaction
from event import TxnRecv
import heapq

class Node:

    blockChain={}
    txnPool=set()
    balance=0
    peer=set()
    txnReceived=set()

    def __init__(self, nid, speed, genesis):
        self.nid=nid
        self.speed=speed # 0=fast, 1=slow
        self.lbid=genesis.bid
        self.blockChain[genesis.bid]=copy.deepcopy(genesis)

    def addBlock(self,block):

        temp=copy.deepcopy(block)
        # temp.length=self.blockChain[temp.pbid].length+1
        self.blockChain[temp.bid]=temp
        if temp.length>self.blockChain[self.lbid].length:
            self.lbid=temp.bid

      
    def txnSend(self, event, hp,lat):
        self.txnReceived.add(event.txn.tid);

        for a in self.peers:
            t=event.time+lat
            action=TxnRecv(time=t,sender=self.nid,receiver=a,txn=event.txn)
            heapq.heappush(hp,(t,action))
            


    def txnRecv(self,event,hp, lat):
        if event.txn.tid in self.txnReceived:
            return 
        
        for a in self.peers:
            t=event.time+lat
            action=TxnRecv(time=t,sender=self.nid,receiver=a,txn=event.txn)
            heapq.heappush(hp,(t,action))

    
    



        