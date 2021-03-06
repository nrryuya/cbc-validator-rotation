from __future__ import annotations
from typing import List
from cbc_casper_simulator.validator import Validator
from cbc_casper_simulator.message import Message
import random as r


class ValidatorSet:
    def __init__(self, validators: List[Validator]):
        assert len(validators) > 0, "At least one validator is required."
        self.validators = validators

        # FIXME: Genesis block should be in states by default
        self.genesis = Message.genesis(r.choice(self.validators))
        self.genesis.estimate.active_validators = validators

        # Add genesis message to all validators
        for validator in self.validators:
            res = validator.add_message(self.genesis)
            assert res.is_ok(), res.value

    def add(self, validator: Validator):
        self.validators.append(validator)
        res = validator.add_message(self.genesis)
        assert res.is_ok(), res.value

    def choose(self, num=1) -> List[Validator]:
        population = min(num, len(self.validators))
        return r.sample(self.validators, population)

    def choose_one(self) -> Validator:
        return r.choice(self.validators)

    def all(self) -> List[Validator]:
        # FIXME: Is this necessary?
        return self.validators

    def dump(self):
        return [validator.dump() for validator in self.all()]

    @classmethod
    def with_random_weight(cls, num, ticker) -> ValidatorSet:
        validators: List[Validator] = []
        for i in range(num):
            validators.append(Validator("v0.0.{}".format(i), r.random(), ticker))
        return ValidatorSet(validators)

    @classmethod
    def with_equal_weight(cls, num, ticker) -> ValidatorSet:
        validators: List[Validator] = []
        for i in range(num):
            validators.append(Validator("v0.0.{}".format(i), 1.0, ticker))
        return ValidatorSet(validators)
