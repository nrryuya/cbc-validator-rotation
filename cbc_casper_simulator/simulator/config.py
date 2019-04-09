from __future__ import annotations
import yaml


class Config:
    def __init__(
        self,
        validator_num: int,
        max_slot: int,
        checkpoint_interval: int,
        rotation_ratio: float,
    ):
        self.validator_num = validator_num
        self.max_slot = max_slot
        self.checkpoint_interval = checkpoint_interval
        self.rotation_ratio = rotation_ratio

    @classmethod
    def default(cls) -> Config:
        return Config(5, 59, 20, 0.1)

    @classmethod
    def from_yaml(cls, name) -> Config:
        with open(name) as f:
            obj = yaml.safe_load(f)
        return Config(
            obj['validator_num'],
            obj['max_slot'],
            obj['checkpoint_interval'],
            obj['rotation_ratio'],
        )
