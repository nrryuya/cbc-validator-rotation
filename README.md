# CBC Casper Validator Rotation

Simulation of validator rotation in CBC Casper

### CBC Casper?
[CBC Casper paper](https://github.com/cbc-casper/cbc-casper-paper)

### Validator rotation
See [this post](https://ethresear.ch/t/validator-rotation-in-cbc-casper/5200) in ethresearch.

### Requirements
* Python 3.7.2 or newer

### Getting started

```
pip install -r requirements.txt
python main.py
```

This will generate `output.yml` by default.
You can specify your simulation parameters file and output file via these options.

```
python main.py -i cbc_casper_simulator/examples/intput.yml -o output.yml
```

### Run tests

```
pip install -r requirements-test.txt -r requirements.txt
pytest
```