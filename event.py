import copy 
from block import Block
from transaction import Transaction
class Event:

    def __init__(self, time,eventId, sender=-1, receiver=-1):
        self.time=time
        self.sender=sender
        self.receiver=receiver
        self.eventId=eventId
    
    # def getTime(self):
    #     return self.time

    



class TxnGen(Event):
    def __init__(self,time,txn):
        self.txn=txn #object of Transaction Class

        Event.__init__(time=time,eventId=1)

class TxnRecv(Event):
    def __init__(self, time,sender,receiver, txn):
        self.txn=txn

        Event.__init__(time=time,sender=sender,receiver=receiver, eventId=2)

class BlockRecv(Event):
    def __init__(self, time, sender, receiver, block):
        self.block=block

        Event.__init__(time=time,sender=sender,receiver=receiver, eventId=3)

class BlockMined(Event):
    def __init__(self,time,block):
        self.block=block

        Event.__init__(time=time, eventId=4)









    
