from cbc_casper_simulator.simulator.config import Config
from cbc_casper_simulator.simulator.broadcast_and_receive_simulator import BroadCastAndReceiveSimulator
import yaml


def run(input, output):
    output_file = "output/output.yml" if output is None else output
    config = Config.default() if input is None else Config.from_yaml(input)
    simulator = BroadCastAndReceiveSimulator(config)

    print("start.")
    states = []
    for slot in range(config.max_slot):
        network_state = next(simulator)
        network_state_dict = network_state.dump()
        states.append(network_state_dict)

    with open(output_file, 'w') as f:
        f.write(yaml.dump(states))
    print("{} was created.".format(output_file))
    print("end.")
