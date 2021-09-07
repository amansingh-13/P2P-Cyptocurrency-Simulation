class Transaction:
    def __init__(self, tid, sender, receiver, value):
        self.sender=sender
        self.receiver=receiver
        self.value=value
        self.tid=tid #transaction id
    
    def __str__(self):
        return f"Id: {self.tid}, Sender:{self.sender.nid}, Receiver: {self.receiver.nid} Value: {self.value}"
