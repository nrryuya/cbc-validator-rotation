class Ticker:
    def __init__(self, initial_slot: int = 0):
        self.slot = initial_slot

    def tick(self):
        self.slot = self.slot + 1

    def current(self):
        return self.slot
