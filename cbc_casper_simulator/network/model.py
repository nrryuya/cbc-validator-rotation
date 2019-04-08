from cbc_casper_simulator.validator_set import ValidatorSet
from cbc_casper_simulator.validator import Validator
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.network.packet import Packet
from cbc_casper_simulator.network.delay import RandomDelay as Delay
from typing import Dict, List


class Model:
    def __init__(self, validator_set: ValidatorSet, validator_num: int, ticker: Ticker = None):
        self.validator_set: ValidatorSet = validator_set
        self.validator_num = validator_num
        self.broadcast_slot_to_message: Dict[int, Message] = dict()
        self.arrival_slot_to_messages: Dict[Validator, Dict[int, List[Message]]] = dict()
        if ticker is None:
            self.ticker = Ticker()
        else:
            self.ticker = ticker

    def send(self, message: Message, sender: Validator, receiver: Validator):
        current_slot = self.ticker.current()
        packet = Packet(message, sender, receiver, current_slot)
        # TODO: Decide delay w.r.t. network topology
        arrival_slot = packet.slot + Delay.get(1, 2)
        self.add_message_to_be_arrived(receiver, arrival_slot, packet.message)

    def receive(self, receiver: Validator):
        # FIXME: Rename this with Validator.add_message()
        messages = self.arrival_slot_to_messages.get(receiver, dict()).get(self.ticker.current(), [])
        for message in messages:
            self.add_message_or_pending(receiver, message)

    def broadcast(self, message: Message, sender: Validator):
        self.broadcast_slot_to_message[self.ticker.current()] = message
        for receiver in self.validator_set.all():
            if sender != receiver:  # NOTE: Sender already received this message in broadcast_from_random_validator()
                self.send(message, sender, receiver)

    def validator_rotation(self, rotation_ratio: int):
        validators: List[Validator] = \
            self.validator_set.choose(int(self.validator_num * (1 - rotation_ratio / 100)))

        for i in range(self.validator_num - len(validators)):
            validator = Validator("v{}.{}".format(self.ticker.current(), i), 1.0, self.ticker)

            res = validator.add_message(self.validator_set.genesis)
            assert res.is_ok(), res.value

            delay = Delay.get(1, 2)
            latest_arrival_slot = self.ticker.current() - delay
            # NOTE: No reordering for new validator
            for broadcast_slot in range(self.ticker.current()):
                broadcast_message = self.broadcast_slot_to_message[broadcast_slot]
                if broadcast_slot <= latest_arrival_slot:
                    # FIXME: Reordering occur here?
                    res = validator.add_message(broadcast_message)
                    assert res.is_ok()
                    continue
                self.add_message_to_be_arrived(validator, broadcast_slot + delay + 1, broadcast_message)

            validators.append(validator)

    def add_message_or_pending(self, receiver: Validator, message: Message):
        res = receiver.add_message(message)
        if not res.is_ok():
            # If the message is not valid, skip that for the next round (assuming the reason is reordering)
            self.add_message_to_be_arrived(receiver, self.ticker.current() + 1, message)

    def add_message_to_be_arrived(self, receiver: Validator, arrival_slot: int, message: Message):
        if receiver in self.arrival_slot_to_messages:
            self.arrival_slot_to_messages[receiver][arrival_slot] = \
                self.arrival_slot_to_messages[receiver].get(arrival_slot, []) + [message]
        self.arrival_slot_to_messages[receiver] = {arrival_slot: [message]}

    def dump(self):
        return {
            "validators": self.validator_set.dump(),
            "slot": self.ticker.current()
        }
