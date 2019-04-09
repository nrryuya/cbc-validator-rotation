from cbc_casper_simulator.block import Block
from cbc_casper_simulator.state import State
from cbc_casper_simulator.justification import Justification
from cbc_casper_simulator.store import Store
from typing import Dict


class LMDGhostEstimator:
    # FIXME: Fix for validator rotation.
    # Assume no "re-entry" and homogeneous weight for simplicity

    @classmethod
    def estimate(cls, state: State, justification: Justification) -> Block:
        scores: Dict[Block, float] = cls.score(state, justification)
        store: Store = state.store

        best_block = store.genesis_block()

        while store.has_children_blocks(best_block):
            # If "tie" exists, choose the block with the smallest hash.
            best_block = max(store.children_blocks(
                best_block), key=lambda block: (scores.get(block, 0), -block.hash))
        return Block(best_block.hash)

    @classmethod
    def verify(cls, state: State, block: Block, justification: Justification) -> bool:
        return cls.estimate(state, justification) == block

    @classmethod
    def score(cls, state: State, justification: Justification) -> Dict[Block, float]:
        scores: Dict[Block, float] = dict()
        store: Store = state.store
        for v, m in justification.latest_message_hashes.items():
            current_block = store.to_block(m)
            while not current_block.is_genesis():
                scores[current_block] = scores.get(
                    current_block, 0) + v.weight
                current_block = store.parent_block(current_block)
            scores[store.genesis.estimate] = scores.get(
                store.genesis.estimate, 0) + v.weight
        return scores
