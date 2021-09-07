import copy 
class Block:
    def __init__(self, bid, pbid, txnIncluded,miner):
        self.bid = bid
        self.pbid = pbid
        if pbid != 0:
            self.txnIncluded=copy.deepcopy(txnIncluded)
        else:
            self.txnIncluded=set()
        self.miner=miner

        if pbid!=0:
            self.txnPool=copy.deepcopy(pbid.txnPool)
            self.length=pbid.length+1
        else:
            self.txnPool=set()
            self.length=1
        
        for a in txnIncluded:
            self.txnPool.add(a)

        if pbid!=0:
            self.balance=copy.deepcopy(pbid.balance)
        else:
            self.balance=[]
        for a in txnIncluded:
            if a.sender!=-1:
                self.balance[a.sender.nid]-=a.value
            self.balance[a.receiver.nid]+=a.value
            
    def __str__ (self):
        return f"Id:{self.bid},Parent:{self.pbid.bid}, Miner:{self.miner}, Txns:{len(self.txnIncluded)}"