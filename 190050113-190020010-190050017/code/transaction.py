class Transaction:
    def __init__(self, tid, sender, receiver, value):
        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.tid = tid #transaction id
    
    def __str__(self):
        return f"Id: {pretty(self.tid)}, Sender:{pretty(self.sender.nid, 5)}, Receiver: {pretty(self.receiver.nid, 5)}, Value: {pretty(self.value, 8)}"
