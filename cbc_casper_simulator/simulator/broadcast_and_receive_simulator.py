from __future__ import annotations
from typing import Iterator
import random as r

from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.network.model import Model as NetworkModel
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.simulator.config import Config
from cbc_casper_simulator.message import Message


class BroadCastAndReceiveSimulator(Iterator[NetworkModel]):
    """
    A simulator where at each slot, a single validator chosen randomly sends a message and all validators receive
    messages w.r.t. network latency.
    """
    def __init__(self, config: Config):
        self.config = config
        self.ticker = Ticker()
        self.network = NetworkModel(ValidatorSet.with_equal_weight(config.validator_num, self.ticker),
                                    config.validator_num, config.rotation_ratio, self.ticker)

    def __iter__(self):
        return self

    def __next__(self) -> NetworkModel:
        i = self.ticker.current()

        if i > self.config.max_slot:
            raise StopIteration

        self.broadcast_from_random_validator()
        self.all_validators_receive_messages()
        self.calc_clique_size()

        self.ticker.tick()
        return self.network

    def broadcast_from_random_validator(self):
        rn: int = r.randint(0, self.config.validator_num - 1)
        for validator in self.network.validator_set.validators:
            message: Message = validator.create_message(rn)
            if not message:  # This validator is not the proposer in this slot
                # FIXME: Remove this validator ("go offline") if she is confident of the success of exit
                continue
            if message.estimate.height > 0 and message.estimate.height % self.config.checkpoint_interval == 0:
                message.estimate.active_validators = self.network.validator_rotation(message.estimate.active_validators)
            res = validator.add_message(message)
            assert res.is_ok(), res.value
            self.network.broadcast(message, validator)

    def all_validators_receive_messages(self):
        for receiver in self.network.validator_set.all():
            self.network.receive(receiver)

    def calc_clique_size(self):
        self.network.update_clique_size()
