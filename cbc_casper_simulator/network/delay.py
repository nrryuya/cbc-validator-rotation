import random as r


class RandomDelay:
    @classmethod
    def get(cls, min=1, max=10):
        return r.randint(min, max)
