from __future__ import annotations
from typing import Optional, List
import random as r
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cbc_casper_simulator.validator import Validator


class Block:
    def __init__(
        self,
        height: int,
        parent_hash: Optional[int] = None,
        active_validators: List[Validator] = None
    ):
        self.height = height
        self.parent_hash: Optional[int] = parent_hash
        # FIXME: random_number is appropriate?
        self.hash: int = r.randint(1, 100000000000000)
        self.active_validators = active_validators

    @classmethod
    def genesis(cls) -> Block:
        return Block(0)

    def is_genesis(self) -> bool:
        return self.parent_hash is None

    def dump(self):
        return {
            "height": self.height,
            "parent_hash": self.parent_hash,
            "hash": self.hash,
            "active_validators": [v.name for v in self.active_validators]
        }
