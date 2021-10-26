from node import Node
from block import Block 
from transaction import Transaction
from event import * 
from utils import * 
from queue import pushq 
import networkx as nx 
from params import *

#this blockchain is for adversary node 
class AdvBlockchain:
    def __init__(self,gblock):
        self.blocks={gblock.bid:(gblock,0)}
        self.head=gblock
        self.private_head=gblock
        self.private_lead=0
        self.state=0 # -1=0'
        self.g=nx.DiGraph() 
        self.total_adv_blocks_gen  = 0
    
    #different function of adding self block.
    # Self block will always be added in private chain 
    def add_self_block(self,block,time):

        self.blocks[block.bid]=(block,time)

        if block.length<self.private_head.length:
            return -100

        old_state=self.state 
        self.private_head=block 
        self.total_adv_blocks_gen += 1
        if self.state==-1:
            self.private_lead=0
            self.head=self.private_head
        else:
            self.private_lead+=1
        
        self.state+=1

        return old_state

    # differnt function for adding foreign block
    # proper chnage in state is maintained and all the 
    # private blocks are released at state = 2 and 1 
    # for other states, first private block is released 
    def add_others_block(self,block,time):
        
        self.blocks[block.bid]=(block,time)

        if block.length > self.head.length :
            self.head=block 

            old_state=self.state

            if self.state==1:
                self.state=-1
                self.private_lead=0

            elif self.state==0:
                self.private_head=self.head  
                self.private_lead=0
                self.state=0 

            elif self.state==2:
                self.state=0
                self.private_lead=0 
                self.head=self.private_head
            
            elif self.state==-1:
                self.state=0
                self.private_lead=0
                self.private_head=self.head 

            
            elif self.state>2 :
                self.state-=1
                self.private_lead-=1
            
            return old_state

        return -100 
    
    # return the first block of 
    # the hidden chain(private chain)
    def first_private_block(self,offset=0) :
        
        block=self.private_head
        l=self.private_lead+offset
        while(l>1):
            block=block.pbid
            l-=1
        return block 

    def balance(self,nid):
        return self.private_head.balance[nid]


        




'''
Adversay node inmherits most of the function from the simple node.
Only different action is taken when a foreign nide arrives at adversary node
and if the adversary node mine a new block successfully 
'''

class AdversaryNode(Node):
    def __init__(self,nid,genesis,miningTime):  
        Node.__init__(self,nid=nid,speed=1,genesis=genesis,miningTime=miningTime) 
        self.blockchain=AdvBlockchain(genesis)
        
        
        
    
    def verifyAndAddReceivedBlock(self, event):
        if event.block.bid in self.blockReceived:
            return 
        self.blockReceived.add(event.block.bid)

        if not event.block.is_valid: # we do not propogate invalid blocks
            return
        
        old_state=self.blockchain.add_others_block(block=event.block,time=event.time)
        
        print(f"{event.block}, Time:{pretty(event.time,10)}")
        print (f"Adversary node state changed to {self.blockchain.state}")

        if old_state==-1 or old_state==0:
            self.mineNewBlock(pblock=self.blockchain.private_head, start_time=event.time)

        elif old_state==1:
            for a in self.peer:
                lat=computeLatency(i=self, j=a, m=100+len(self.blockchain.private_head.txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=self.blockchain.private_head)
                pushq(action)
            # self.mineNewBlock(pblock=self.blockchain.private_head, start_time=event.time)

        elif old_state==2:
            block1=self.blockchain.private_head
            block2=self.blockchain.private_head.pbid 

            for a in self.peer:
                lat=computeLatency(i=self, j=a, m=100+len(block1.txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=block1)
                pushq(action)
                lat=computeLatency(i=self, j=a, m=100+len(block2.txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=block2)
                pushq(action)
            
            # self.mineNewBlock(pblock=self.blockchain.private_head, start_time=event.time)
        
        elif old_state>2:
            block=self.blockchain.first_private_block(offset=1)
            for a in self.peer:
                lat=computeLatency(i=self, j=a, m=100+len(block.txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=block)
                pushq(action)




                


            




    def receiveSelfMinedBlock(self, event):
        self.blockReceived.add(event.block.bid)
        old_state=self.blockchain.add_self_block(block=event.block,time=event.time)

        if old_state==-1:
            
            print(f"{event.block}, Time:{pretty(event.time,10)}")
            print("Adversary wins from -1 to 0")
            for a in self.peer:
                lat=computeLatency(i=self, j=a, m=100+len(event.block.txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=event.block)
                pushq(action)
            self.mineNewBlock(pblock=self.blockchain.private_head, start_time=event.time)
        

        elif old_state>-1 :
            
            print(f"{event.block}, Time:{pretty(event.time,10)}")
            print(f"Adversary node state changed to {self.blockchain.state}")
            self.mineNewBlock(pblock=self.blockchain.private_head, start_time=event.time)
        
        
        
   # this function helps to release all the nodes at the end of the simulation
   # # this is necessary to maintain  the uniformity in network after the end of simulation
   # because if the adversary node is very poerful then it can even maintain 
   # a lead of more than 10 blocks. So using this function we can bring uniformity and 
   # hence bettter visualisation 
    def release_all_private_blocks(self):
        private_blocks=[]
        if self.blockchain.private_lead==0:
            return private_blocks

        while(self.blockchain.private_lead>0):
            private_blocks.append(self.blockchain.first_private_block())
            self.blockchain.private_lead-=1
        
        return private_blocks






        
        

