import copy 
class Block:
    # txnPool=set()
    def __init__(self, bid, pbid, txnIncluded,miner):
        self.bid=bid
        self.pbid=pbid
        self.txnIncluded=copy.deepcopy(txnIncluded)
        self.miner=miner

        self.txnPool=copy.deepcopy(pbid.txnPool)
        for a in txnIncluded:
            self.txnPool.add(a)

        self.balance=copy.deepcopy(pbid.balance)
        for a in txnIncluded:
            self.balance[a.sender]-=a.value
            self.balance[a.receiver]+=a.value
        
        self.length=pbid.length+1




