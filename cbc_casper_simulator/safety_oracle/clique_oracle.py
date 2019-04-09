import itertools
import networkx as nx
from typing import Dict, List, Tuple

from cbc_casper_simulator.state import State
from cbc_casper_simulator.block import Block
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.validator import Validator
from cbc_casper_simulator.validator_set import ValidatorSet


# Based on: https://github.com/ethereum/cbc-casper/blob/master/casper/safety_oracles/clique_oracle.py
class CliqueOracle:
    """A clique safety oracle detecting safety from validators committed to an estimate."""

    def __init__(self, block: Block, state: State, validator_set: ValidatorSet):
        if block is None:
            raise Exception("cannot decide if safe without an estimate")

        self.block: Block = block
        self.state: State = state
        # FIXME: Remove equivocating validators
        self.validators: List[Validator] = validator_set.validators
        # FIXME: Add latest_message member to Store
        self.latest_messages: Dict[Validator, Message] = state.store.latest_messages()

        # Only consider validators whose messages are compatible w/ candidate_estimate.
        self.candidates: List[Validator] = {v for v in self.validators if v in self.latest_messages
                                            and self.state.store.is_agreeing(block, self.latest_messages[v])}

    def _collect_edges(self):
        edges: List[Tuple[Validator, Validator]] = []
        # For each pair of validators, val1, val2, add an edge if:
        for val1, val2 in itertools.combinations(self.candidates, 2):
            # the latest message val1 has seen from val2 is on the candidate estimate,
            v1_msg: Message = self.latest_messages[val1]
            if val2 not in v1_msg.justification.latest_message_hashes:
                continue

            v2_latest_message_hash = v1_msg.justification.latest_message_hashes[val2]
            v2_msg_in_v1_view = self.state.store.messages[v2_latest_message_hash]
            if not self.state.store.is_agreeing(self.block, v2_msg_in_v1_view):
                continue

            # the latest block val2 has seen from val1 is on the candidate estimate
            v2_msg: Message = self.latest_messages[val2]
            if val1 not in v2_msg.justification.latest_message_hashes:
                continue

            v1_latest_message_hash = v2_msg.justification.latest_message_hashes[val1]
            v1_msg_in_v2_view = self.state.store.messages[v1_latest_message_hash]
            if not self.state.store.is_agreeing(self.block, v1_msg_in_v2_view):
                continue

            # there are no blocks from val2, that val1 has not seen;
            # that might change validators' estimate.
            if not self.no_later_disagreeing(val2, v2_msg_in_v1_view):
                continue

            # and if there are no blocks from val1, that val2 has not seen,
            # that might change val2's estimate.
            if not self.no_later_disagreeing(val1, v1_msg_in_v2_view):
                continue

            edges.append((val1, val2))

        return edges

    # Find biggest set of validators that
    # a) each of their latest messages is on the candidate_estimate
    # b) each of them have seen from each other a latest message on the candidate_estimate
    # c) none of them can see a new message from another not on the candidate_estimate
    # NOTE: if biggest clique can easily be determined to be < 50% by weight, will
    #       return with empty set and 0 weight.
    def find_biggest_clique(self):
        """Finds the biggest clique of validators committed to target estimate."""

        # Do not have finality if less than half have candidate_estimate.
        if sum({v.weight for v in self.candidates}) <= sum({v.weight for v in self.validators}) / 2:
            return set(), 0

        edges: List[Tuple[Validator, Validator]] = self._collect_edges()
        graph = nx.Graph()
        graph.add_edges_from(edges)
        cliques = nx.find_cliques(graph)

        max_clique = []
        max_weight = 0
        for clique in cliques:
            test_weight = sum({v.weight for v in clique})
            if test_weight > max_weight:
                max_clique = clique
                max_weight = test_weight

        return set(max_clique), max_weight

    def biggest_clique_weight(self) -> float:
        return self.find_biggest_clique()[1]

    def no_later_disagreeing(self, val: Validator, message: Message) -> bool:
        """Returns whether there exists a free message.
        A free message is a message later than the sequence number from some val,
        and conflicts with the estimate."""

        latest_slot: int = message.sender_slot
        from_sender_hashes: List[int] = self.state.store.message_history[val]

        for hash in from_sender_hashes:
            message: Message = self.state.store.messages[hash]
            if message.sender_slot > latest_slot:
                if not self.state.store.is_agreeing(self.block, message):
                    return False

        return True
