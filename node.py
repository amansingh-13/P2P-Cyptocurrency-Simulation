import copy

from numpy.core.numeric import tensordot 
from block import Block
from transaction import Transaction
from event import *
import heapq
import numpy as np 
from random import sample
from latency import computeLatency

from main import pushq

class Node:

    blockChain={}
    # txnPool=set()
    balance=0
    peer=set()
    txnReceived=set()
    blockReceived=set()


    def __init__(self, nid, speed, genesis, miningTime):
        self.nid=nid
        self.speed=speed # 1=fast, 0=slow
        self.lbid=genesis.bid
        self.blockChain[genesis.bid]=copy.deepcopy(genesis)
        self.miningTime=miningTime

    def addPeer(self,node):
        self.peer.add(node)

    def txnSend(self, event):
        self.txnReceived.add(event);

        for a in self.peer:
            t=event.time+computeLatency(self,a,1)
            action=TxnRecv(time=t,sender=self,receiver=a,txn=event.txn)
            pushq(action)

            


    def txnRecv(self,event):
        if event.txn in self.txnReceived:
            return 
        self.txnReceived.add(event.txn)

        for a in self.peer:
            t=event.time+computeLatency(self,a,1)
            action=TxnRecv(time=t,sender=self.nid,receiver=a,txn=event.txn)
            pushq(action)
    
    def blockVerify(self,cblock):
        pblock=self.blockChain[cblock.pbid]
        for a in cblock.txnIncluded:

            cb=pblock[a.receiver]+a.value
            if cb!=cblock.balance[a.receiver]:
                return False

            if a.sender==-1:
                continue

            sb=pblock.balance[a.sender]-a.value
            if sb<0:
                return False
            if sb!=cblock.balance[a.sender]:
                return False
        return True

    def mineNewBlock(self,block,lat):
        remaingTxn=self.txnReceived.difference(block.txnPool)
        numTxn=max(np.random.randint(0,len(remaingTxn)),900)

        txnToInclude=set(sample(remaingTxn,numTxn))
        txnId=np.random.randint(0,2**128-1)
        coinBaseTxn=Transaction(tid=txnId,sender=-1,receiver=self.nid,value=50)
        txnToInclude.add(coinBaseTxn)


        newBlockId=np.random.randint(0,2**128-1)

        newBlock=Block(bid=newBlockId,pbid=block,txnIncluded=txnToInclude,miner=self)

        lat=lat+np.random.exponential(self.miningTime)
        newMiningEvent=BlockMined(time=lat, block=newBlock)
        pushq(newMiningEvent)









    def verifyAndAddReceivedBlock(self,event):

        if self.blockVerify(event.block)!=True:
            return False
        
        

        temp=copy.deepcopy(event.block)
        # temp.length=self.blockChain[temp.pbid].length+1
        self.blockChain[temp.bid]=temp
        if temp.length>self.blockChain[self.lbid].length:
            self.lbid=temp.bid
            self.mineNewBlock(block=temp,lat=event.time)

        
        for a in self.peer:
            lat=computeLatency(i=self,j=a,m=100+len(temp.txnIncluded))
            lat=event.time+lat
            action=BlockRecv(time=lat,sender=self,receiver=a,block=temp)
            pushq(action)

        return True
    
    def receiveSelfMinedBlock(self, event):
        temp=copy.deepcopy(event.block)
        self.blockChain[temp.bid]=temp

        if temp.length>self.blockChain[self.lbid].length:
            self.lbid=temp.bid
            for a in self.peer:
                lat=computeLatency(i=self,j=a,m=100+len(temp.txnIncluded))
                lat=event.time+lat
                action=BlockRecv(time=lat,sender=self,receiver=a,block=temp)
                pushq(action)    