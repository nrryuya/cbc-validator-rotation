from typing import Dict
from typing import TYPE_CHECKING
from cbc_casper_simulator.state import State
import random as r
if TYPE_CHECKING:
    from cbc_casper_simulator.validator import Validator


class Weight:
    @classmethod
    def weights(cls, state: State) -> Dict['Validator', float]:
        weights: Dict[Validator, float] = dict()
        # TODO: implement
        for validator in state.justification().latest_messages:
            weights[validator] = r.random()
        return weights
