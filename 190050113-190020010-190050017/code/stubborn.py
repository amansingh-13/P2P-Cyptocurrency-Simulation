from adversary import * 


class StubBlockchain(AdvBlockchain):
    def __init__(self, gblock):
        super().__init__(gblock)
    