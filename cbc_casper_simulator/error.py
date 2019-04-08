from typing import List


class Error:
    def __init__(self, reason: str):
        self.reason: str = reason

    def __repr__(self):
        return self.reason


class MessageValidationError(Error):
    pass


class MessageNotJustifiedError(MessageValidationError):
    def __init__(self, message_hashes: List[int]):
        errors = ["{} is not justified.".format(
            message_hash) for message_hash in message_hashes]
        reason = " ".join(errors)
        super().__init__(reason)
