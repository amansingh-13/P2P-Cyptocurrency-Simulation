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

    def __init__(self, nid, speed, genesis, miningTime):
        self.nid=nid
        self.speed=speed # 1=fast, 0=slow
        self.lbid=genesis.bid
        self.blockChain[genesis.bid]=copy.deepcopy(genesis)
        self.miningTime=miningTime

    def addPeer(self,peerId):
        self.peer.add(peerId)

    def txnSend(self, event, hp):
        self.txnReceived.add(event.txn.tid);

        for a in self.peers:
            t=event.time+lat
            action=TxnRecv(time=t,sender=self.nid,receiver=a,txn=event.txn)
            heapq.heappush(hp,(t,action))
            


    def txnRecv(self,event,hp):
        if event.txn.tid in self.txnReceived:
            return 
        self.txnReceived.add(event.txn.tid)

        for a in self.peers:
            t=event.time+lat
            action=TxnRecv(time=t,sender=self.nid,receiver=a,txn=event.txn)
            heapq.heappush(hp,(t,action))
    
    def blockVerify(self,cblock):
        pblock=self.blockChain[cblock.pbid]
        for a in cblock.txnIncluded:
            sb=pblock.balance[a.sender]-a.value
            if sb<0:
                return False
            if sb!=cblock.balance[a.sender]:
                return False
        return True

    def mineNewBlock(self,block):
        remaingTxn=self.txnReceived.difference(block.txnPool)

    def addReceivedBlock(self,block):

        if self.blockVerify(block)!=True:
            return False

        temp=copy.deepcopy(block)
        # temp.length=self.blockChain[temp.pbid].length+1
        self.blockChain[temp.bid]=temp
        if temp.length>self.blockChain[self.lbid].length:
            self.lbid=temp.bid

        return True
    
    
    

      



    
    



        