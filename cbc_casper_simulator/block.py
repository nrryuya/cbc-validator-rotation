from __future__ import annotations
from typing import Optional
import random as r


class Block:
    def __init__(
        self,
        parent_hash: Optional[int] = None,
    ):
        self.parent_hash: Optional[int] = parent_hash
        # TODO: random_number is appropriate?
        self.hash: int = r.randint(1, 100000000000000)

    @classmethod
    def genesis(cls) -> Block:
        return Block()

    def is_genesis(self) -> bool:
        return self.parent_hash is None

    def dump(self):
        return {
            "parent_hash": self.parent_hash,
            "hash": self.hash
        }
