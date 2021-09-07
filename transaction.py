class Transaction:
    def __init__(self, tid, sender, receiver, value,time):
        self.sender=sender
        self.receiver=receiver
        self.value=value
        self.tid=tid
        self.time=time