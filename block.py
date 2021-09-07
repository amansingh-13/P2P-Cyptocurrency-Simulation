import copy 
class Block:
    # txnPool=set()
    def __init__(self, bid, pbid, txnIncluded,miner):
        self.bid=bid
        self.pbid=pbid
        if pbid!=0 :
            self.txnIncluded=copy.deepcopy(txnIncluded)
        else:
            self.txnIncluded=set()
        self.miner=miner

        if pbid!=0:
            self.txnPool=copy.deepcopy(pbid.txnPool)
        else:
            self.txnPool=set()

        for a in txnIncluded:
            self.txnPool.add(a)

        if pbid!=0:
            self.balance=copy.deepcopy(pbid.balance)
        else:
            self.balance=[]
        for a in txnIncluded:
            self.balance[a.sender]-=a.value
            self.balance[a.receiver]+=a.value
        
        self.length=pbid.length+1




