import copy 
class Node:

    blockChain={}
    txnPool=set()
    balance=0
    peer=set()
    txnReceived=set()

    def __init__(self, nid, type, lbid):
        self.nid=nid
        self.type=type # 0=fast, 1=slow
        self.lbid=lbid

    def addBlock(self,block):

        temp=copy.deepcopy(block)
        # temp.length=self.blockChain[temp.pbid].length+1
        self.blockChain[temp.bid]=temp
        if temp.length>self.blockChain[self.lbid].length:
            self.lbid=temp.bid

      
    def txnSend(self, event, hp,lat):
        pass

    def txnRecv(self,event,hp, lat):
        pass

    
    



        