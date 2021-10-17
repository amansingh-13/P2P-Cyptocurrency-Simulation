from adversary import * 
from node import Node

#this blockchain is for adversary node 
# it inherits form AdvBlockchain
# only difference is in the transition form 2 -> 1 and 0'-> 0 or 1.
class StubBlockchain(AdvBlockchain):
    def __init__(self, gblock):
        super().__init__(gblock)
    

    def add_self_block(self,block,time):
        self.blocks[block.bid]=(block,time)

        if block.length<self.private_head.length:
            return -100

        old_state=self.state 
        self.private_head=block
        self.total_adv_blocks_gen += 1


        if self.state==-1:
            self.private_lead=1
            self.state=1

        elif self.state>-1:
            self.private_lead+=1
            self.state+=1

        return old_state
    
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

            
            
            elif self.state==-1:
                self.state=0
                self.private_lead=0
                self.private_head=self.head 

            
            elif self.state>1 :
                self.state-=1
                self.private_lead-=1
            
            return old_state

        return -100 

# this is similar to AdvNode, only difference is handling transition for 0' to 0 or 1 and 2 to 1. 
# it does not go form 2 to 0 directly. 

class StubNode(Node):
    def __init__(self, nid, genesis, miningTime):
        super().__init__(nid=nid, speed=1, genesis=genesis, miningTime=miningTime)
        self.blockchain=StubBlockchain(genesis)


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

        
        elif old_state>0:
            block=self.blockchain.first_private_block(offset=1)
            for a in self.peer:
                lat=computeLatency(i=self, j=a, m=100+len(block.txnIncluded))
                action = BlockRecv(time=event.time+lat, sender=self, receiver=a, block=block)
                pushq(action)
            



    
    def receiveSelfMinedBlock(self, event):
        self.blockReceived.add(event.block.bid)
        old_state=self.blockchain.add_self_block(block=event.block,time=event.time)
        if old_state>=-1:
            print(f"{event.block}, Time:{pretty(event.time,10)}")
            print(f"Adversary node state changed to {self.blockchain.state}")
            self.mineNewBlock(pblock=self.blockchain.private_head, start_time=event.time)
        # else:
            # self.mineNewBlock(pblock=self.blockchain.private_head, start_time=event.time)

    
    def release_all_private_blocks(self):
        private_blocks=[]
        if self.blockchain.private_lead==0:
            return private_blocks

        while(self.blockchain.private_lead>0):
            private_blocks.append(self.blockchain.first_private_block())
            self.blockchain.private_lead-=1
        
        return private_blocks

        
        
