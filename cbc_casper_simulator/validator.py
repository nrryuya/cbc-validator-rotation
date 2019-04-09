from __future__ import annotations
from cbc_casper_simulator.state import State
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.justification import Justification
from cbc_casper_simulator.block import Block
from cbc_casper_simulator.estimator.lmd_ghost_estimator import LMDGhostEstimator as Estimator
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.error import Error
from typing import Optional
import random as r
from result import Result


class Validator:
    def __init__(
            self,
            name: str,
            initial_weight: float,
            ticker: Ticker
    ):
        self.name: str = name
        self.weight: float = initial_weight
        self.state = State(ticker)  # FIXME: How about passing ticker to add_message and remove ticker from State?
        self.hash: int = r.randint(1, 100000000000000)  # FIXME: calc hash

    def create_message(self, rn: int) -> Optional[Message]:
        justification: Justification = self.state.justification()
        head: Block = Estimator.estimate(self.state, justification)
        if not self == head.active_validators[rn]:
            return None
        return Message(
            self,
            Block(head.height + 1, head.hash, head.active_validators),  # Block creation
            justification,
            self.state.current_slot()
        )

    def add_message(self, message: Message) -> Result[Error, bool]:
        return self.state.transition(message)

    def tick(self):
        self.state.tick()

    def dump(self):
        return {
            "name": self.name,
            "state": self.state.dump(),
            "current_slot": self.state.ticker.current()  # FIXME: Maybe we don't need this
        }

    def __eq__(self, other: Validator):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash
