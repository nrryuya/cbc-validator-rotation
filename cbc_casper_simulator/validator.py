from __future__ import annotations
from cbc_casper_simulator.state import State
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.estimator.lmd_ghost_estimator import LMDGhostEstimator as Estimator
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.error import Error
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
        self.state = State(ticker)
        # TODO: implement
        self.hash: int = r.randint(1, 100000000000000)

    def create_message(self) -> Message:
        sender = self
        justification = self.state.justification()
        estimate = Estimator.estimate(self.state, justification)
        message = Message(
            sender,
            estimate,
            justification,
            self.state.current_slot()
        )
        return message

    def add_message(self, message: Message) -> Result[Error, bool]:
        return self.state.transition(message)

    def tick(self):
        self.state.tick()

    def dump(self):
        return {
            "name": self.name,
            "state": self.state.dump(),
            "current_slot": self.state.ticker.current()
        }

    def __eq__(self, other: Validator):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash
