# CBC Casper Validator Rotation

Simulation of validator rotation in CBC Casper

## Introduction
CBC Casper is one of the cutting-edge research of blockchain consensus protocol.
One of the open questions about CBC Casper is how to do validator rotation in CBC Casper.
(In the latest paper of CBC Casper, a static set (and weight mapping) of validators is assumed.)

We present a protocol of validator rotation in CBC Casper and implemented the simulator & visualizer to do experiments of that proposal.

## Validator rotation protocol
We modify CBC Casper in two ways. 

### Fork-choice rule
In this post, we assume the LMD GHOST for our fork-choice rule.
First, we modify LMD GHOST so that blocks are scored by the weight decided by the information (s.t. entry/exit transactions) included until the parent block in the “best children selection”.
(E.g. if a block `A` has children `B1` `B2`, ..., `Bn`, the weight in A is used to choose between `B1`, `B2`, ..., `Bn`.)
From this modification, the result of LMD GHOST does not change by validator rotation in the future.

### Finality detection 
Second, we modify the finality detection mechanism called [clique oracle](https://github.com/ethereum/cbc-casper/wiki/FAQ#clique-oracle).
Clique oracle is a way to detect the finality of a block by seeking a "clique" of the block i.e. a set of non-equivocating validators "locked" on that block.
A clique's weight is compared to a certain threshold. (We omit the detail of this here.) 
Because of the modification of the fork-choice, we weight a clique for a block by the weight of the block.
We can consider a block finalized if all the ancestors of the block have a clique larger than the threshold by the weight in themselves.

These are sufficient as the general rule for validator rotation.
However, for efficiency, we limit the change of weight for a certain range of blocks.
(Thanks Aditya for this input!)
### Checkpointing
We allow the weight to change only in pre-defined block heights called "checkpoints".
If the interval of checkpoints is constant number `N`, blocks at height `i * N` (e.g. `N`, `2N`, `3N`, ...) are the checkpoints and the weights in blocks at `i * N`,  `i * N + 1`, `i * N + 2`, ... are the same.
From this, an efficient algorithm for the verification of LMD GHOST called [Bitwise LMD GHOST](https://medium.com/@aditya.asgaonkar/bitwise-lmd-ghost-an-efficient-cbc-casper-fork-choice-rule-6db924e57d1f) can be performed from a checkpoint to the next checkpoint.
I.e. If the current block height is `H`, we use Bitwise LMD GHOST for `floor(H/N) + 1` times. 


### Requirements
* Python 3.7.2 or newer

### Getting started

```
pip install -r requirements.txt
python main.py
```

This generates `output/output.yml` by default.
You can set the parameters of simulation by a YAML file and the path of output as follows. 

```
python main.py -i cbc_casper_simulator/examples/intput.yml -o output.yml
```

### Run tests

```
pip install -r requirements-test.txt
pytest
```
 
 
### Resources
- [CBC Casper paper](https://github.com/cbc-casper/cbc-casper-paper)
- [CBC Caspre Wiki FAQ](https://github.com/ethereum/cbc-casper/wiki/FAQ)

