from node import Node
from block import Block 
from transaction import Transaction
from event import * 
from utils import * 
from queue import pushq 
import networkx as nx 

class AdvBlockchain:
    def __init__(self,gblock):
        self.blocks={gblock.bid:(gblock,0)}
        self.head=gblock
        self.private_head=gblock
        self.private_lead=0
        self.state=0 # -1=0'
        self.g=nx.DiGraph() 
    

    def add_self_block(self,block,time):
        block.time=time 
        self.blocks[block.bid]=(block,time)

        if block.length<self.private_head.length:
            return -100

        old_state=self.state 
        self.private_head=block 
        if self.state==-1:
            self.private_lead=0
            self.head=self.private_head
        else:
            self.private_lead+=1
        
        self.state+=1

        return old_state
    
    def add_others_block(self,block,time):
        block.time=time 
        self.blocks[block.bid]=(block,time)

        if block.length > self.head.length :
            self.head=block 

            old_state=self.state

            if self.state==1:
                self.state=-1
                self.private_lead=0 
            elif self.state==0:
                self.private_head=block 
                self.private_lead=0
                self.state=0 
            elif self.state==2:
                self.state=0
                self.private_lead=0 
                self.head=self.private_head
            
            else :
                self.state-=1
                self.private_head-=1
            
            return old_state

        return -100 
    
    def first_private_block(self) :
        
        block=self.private_head
        l=self.private_lead
        while(l>1):
            block=block.pbid
            l-=1
        return block 

    def balance(self,nid):
        return self.private_head.balance[nid]


        






class AdversaryNode(Node):
    def __init__(self,nid,genesis,miningTime):  
        Node.__init__(nid=nid,speed=1,genesis=genesis,miningTime=miningTime) 
        self.blockchain=AdvBlockchain(genesis)
        
        
        
    
    def verifyAndAddReceivedBlock(self, event):
        if event.block.bid in self.blockReceived:
            return 
        self.blockReceived.add(event.block.bid)

        if not event.block.is_valid: # we do not propogate invalid blocks
            return
        
        old_state=self.blockchain.add_others_block(block=event.block,time=event.time)

        if old_state==-1 or old_state==0:
            self.mineNewBlock(pblock=event.block, start_time=event.time)

        elif old_state==1:
            for a in self.peer:
                lat=computeLatency(i=self, j=a, m=100+(self.blockchain.private_head.txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=self.blockchain.private_head)
                pushq(action)
            # self.mineNewBlock(pblock=self.blockchain.private_head, start_time=event.time)

        elif old_state==2:
            block1=self.blockchain.private_head
            block2=self.blockchain.private_head.pbid 

            for a in self.peer:
                lat=computeLatency(i=self, j=a, m=100+(block1.txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=block1)
                pushq(action)
                lat=computeLatency(i=self, j=a, m=100+(block2.txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=block2)
                pushq(action)
            
            # self.mineNewBlock(pblock=self.blockchain.private_head, start_time=event.time)
        
        elif old_state>2:
            for a in self.peer:
                lat=computeLatency(i=self, j=a, m=100+(self.blockchain.first_private_block().txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=self.blockchain.first_private_block())
                pushq(action)




                


            




    def receiveSelfMinedBlock(self, event):
        self.blockReceived.add(event.block.bid)
        old_state=self.blockchain.add_self_block(block=event.block,time=event.time)

        if old_state==-1:
            print("Adversary wins from 0' to 0")
            print(f"{event.block}, Time:{pretty(event.time,10)}")
            for a in self.peer:
                lat=computeLatency(i=self, j=a, m=100+(event.block.txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=event.block)
                pushq(action)
            self.mineNewBlock(pblock=event.block, start_time=event.time)
        

        elif old_state>-1 :
            print(f"Private chain increased to state {self.blockchain.state}")
            print(f"{event.block}, Time:{pretty(event.time,10)}")
            self.mineNewBlock(pblock=event.block, start_time=event.time)



        
        

