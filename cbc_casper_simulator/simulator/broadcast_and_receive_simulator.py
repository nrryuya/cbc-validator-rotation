from __future__ import annotations
from typing import Iterator
from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.network.model import Model as NetworkModel
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.simulator.config import Config


class BroadCastAndReceiveSimulator(Iterator[NetworkModel]):
    """
    A simulator where at each slot, a single validator chosen randomly sends a message and all validators receive
    messages w.r.t. network latency.
    """
    def __init__(self, config: Config):
        self.config = config
        self.ticker = Ticker()
        self.network = NetworkModel(ValidatorSet.with_equal_weight(config.validator_num, self.ticker),
                                    config.validator_num, self.ticker)

    def __iter__(self):
        return self

    def __next__(self) -> NetworkModel:
        i = self.ticker.current()

        # TODO: Is it correct to do validator rotation from Simulator object?
        if i % self.config.checkpoint_interval == 0:
            self.network.validator_rotation(self.config.rotation_ratio)

        if i > self.config.max_slot:
            raise StopIteration

        self.broadcast_from_random_validator()
        self.all_validators_receive_messages()

        self.ticker.tick()
        return self.network

    def broadcast_from_random_validator(self):
        sender = self.network.validator_set.choose_one()
        message = sender.create_message()
        res = sender.add_message(message)
        assert res.is_ok(), res.value
        self.network.broadcast(message, sender)

    def all_validators_receive_messages(self):
        for receiver in self.network.validator_set.all():
            self.network.receive(receiver)
