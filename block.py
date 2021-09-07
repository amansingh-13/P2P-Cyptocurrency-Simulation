import copy 
#This data structure contains all the details of a single block

class Block:
    time=0
    def __init__(self, bid, pbid, txnIncluded,miner):
        self.bid = bid # block id
        self.pbid = pbid #parent block id
        if pbid != 0: #to check if it is not genesis block
            self.txnIncluded=copy.deepcopy(txnIncluded)
        else:
            self.txnIncluded=set()
        self.miner=miner

        # txnPool stores all the txn mined till now 
        # length shows the length of chain from genesis block till current block 
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
        for a in txnIncluded: #updating balance of all the user 
            if a.sender!=-1:
                self.balance[a.sender.nid]-=a.value
            self.balance[a.receiver.nid]+=a.value
            
    def __str__ (self):
        return f"Id:{self.bid},Parent:{self.pbid.bid}, Miner:{self.miner}, Txns:{len(self.txnIncluded)}, Time:{self.time}"