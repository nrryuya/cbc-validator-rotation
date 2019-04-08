from __future__ import annotations
from result import Ok, Err, Result
# FIXME: Resolve circular reference
# from cbc_casper_simulator.state import State
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.error import Error, MessageNotJustifiedError
from cbc_casper_simulator.justification import Justification


class MessageValidator:
    @classmethod
    def validate(cls, state: 'State', message: Message) -> Result[Error, bool]:
        justified = cls.justification_is_justified(
            state, message.justification)
        if justified.is_err():
            return justified
        # TOOD: implement

        return Ok(True)

    @classmethod
    def justification_is_justified(cls, state: 'State', justification: Justification) -> Result[Error, bool]:
        not_justified = [h for h in justification.latest_messages.values(
            ) if not state.store.justified(h)]

        if len(not_justified) > 0:
            return Err(MessageNotJustifiedError(not_justified))
        else:
            return Ok(True)
