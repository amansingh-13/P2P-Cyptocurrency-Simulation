from adversary import * 


class StubBlockchain(AdvBlockchain):
    def __init__(self, gblock):
        super().__init__(gblock)
    
    def add_others_block(self, block, time):
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