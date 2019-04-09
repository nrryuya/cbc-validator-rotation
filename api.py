from cbc_casper_simulator.simulator.run import run
from cbc_casper_simulator.simulator.config import Config
from cbc_casper_simulator.simulator.broadcast_and_receive_simulator import BroadCastAndReceiveSimulator

from flask import Flask, request, jsonify
import yaml
import json

app = Flask(__name__)

@app.route('/simulator', methods=['POST'])
def run_simulator():
    data = request.data.decode('utf-8')
    request_data = json.loads(data)

    input = request_data.get('input')

    config = Config.default() if input is None else Config.from_yaml(input)
    simulator = BroadCastAndReceiveSimulator(config)

    states = []
    for slot in range(config.max_slot):
        network_state = next(simulator)
        network_state_dict = network_state.dump()
        states.append(network_state_dict)

    return jsonify({ 'status': 'ok', 'output': yaml.dump(states) }), 200

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3033)

