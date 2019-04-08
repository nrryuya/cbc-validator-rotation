import dataclasses
from typing import Generic, TypeVar
T = TypeVar('T')
U = TypeVar('U')


@dataclasses.dataclass
class Packet(Generic[T, U]):
    message: T
    sender: U
    receiver: U
    slot: int
