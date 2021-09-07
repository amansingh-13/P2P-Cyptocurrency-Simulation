class Transaction:
    def __init__(self, tid, sender, receiver, value):
        self.sender=sender
        self.receiver=receiver
        self.value=value
        self.tid=tid