
class Event:

    def __init__(self, time,type, sender=-1, receiver=-1):
        self.time=time
        self.sender=sender
        self.receiver=receiver
        self.type=type
    
    # def getTime(self):
    #     return self.time

    



class TxnGen(Event):
    def __init__(self,time,txn):
        self.txn=txn 

        Event.__init__(time=time,type=1)

class TxnRecv(Event):
    def __init__(self, time,sender,receiver, txn):
        self.txn=txn

        Event.__init__(time=time,sender=sender,receiver=receiver, type=2)

class BlockRecv(Event):
    def __init__(self, time, sender, receiver, block):
        self.block=block

        Event.__init__(time=time,sender=sender,receiver=receiver, type=3)

class BlockMined(Event):
    def __init__(self,time,block):
        self.block=block

        Event.__init__(time=time, type=4)









    
