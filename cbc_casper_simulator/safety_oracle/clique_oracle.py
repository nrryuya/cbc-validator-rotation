from result import Ok, Result
from cbc_casper_simulator.error import Error


class CliqueOracle:
    @classmethod
    def check_safety(cls, block, state, validator_set) -> Result[Error, bool]:
        # TODO: implement
        return Ok(True)
