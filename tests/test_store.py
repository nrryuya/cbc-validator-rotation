from cbc_casper_simulator.validator import Validator
from cbc_casper_simulator.store import Store
from cbc_casper_simulator.message import Message
from cbc_casper_simulator.util.ticker import Ticker
from cbc_casper_simulator.justification import Justification
from cbc_casper_simulator.block import Block


def test_store():
    ticker = Ticker()
    validator = Validator("v0", 1.0, ticker)
    genesis = Message.genesis(validator)
    store = Store()
    store.add(genesis)
    b1 = Block(genesis.estimate.hash)
    child = Message(validator, b1, Justification(store.latest_messages()), 0)
    store.add(child)

    message_history = {
        validator: [genesis.hash, child.hash]
    }
    assert store.message_history == message_history

    messages = {
        genesis.hash: genesis,
        child.hash: child
    }
    assert store.messages == messages

    children = {
        genesis.hash: [child.hash]
    }
    assert store.children == children

    parent = {
        child.hash: genesis.hash
    }
    assert store.parent == parent

    block_to_message_in_hash = {
        genesis.estimate.hash: genesis.hash,
        child.estimate.hash: child.hash
    }
    assert store.block_to_message_in_hash == block_to_message_in_hash

    assert store.genesis == genesis

    assert store.message(child.hash) == child
    assert store.message(genesis.hash) == genesis
    assert store.message(000) is None

    latest_message_hashes = {
        validator: child.hash
    }
    assert store.latest_message_hashes() == latest_message_hashes

    latest_messages = {
        validator: child
    }
    assert store.latest_messages() == latest_messages

    assert store.parent_message(child) == genesis
    assert store.parent_message(genesis) is None

    assert store.children_messages(child) == []
    assert store.children_messages(genesis) == [child]

    assert store.parent_block(genesis.estimate) is None
    assert store.parent_block(child.estimate) == genesis.estimate

    assert store.children_blocks(child.estimate) == []
    assert store.children_blocks(genesis.estimate) == [child.estimate]

    assert store.has_children_blocks(genesis.estimate)
    assert not store.has_children_blocks(child.estimate)

    assert store.justified(genesis)
    assert store.justified(child)
    assert not store.justified(000)

    assert store.genesis_block() == genesis.estimate
