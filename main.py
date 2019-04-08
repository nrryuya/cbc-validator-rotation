# NOTE: Do not create png files for now
# from cbc_casper_simulator.examples.broadcast import simulate as broadcast
# from cbc_casper_simulator.examples.lmd_ghost import simulate as lmd_ghost
from cbc_casper_simulator.simulator.run import run
import argparse


def main():
    parser = argparse.ArgumentParser(description='CBC Casper Simulator')
    parser.add_argument(
        '-i', '--input', help='The file path of simulation parameters.'
    )
    parser.add_argument(
        '-o', '--output', help='The file path to output simulation result.'
    )
    args = parser.parse_args()
    run(args.input, args.output)


if __name__ == "__main__":
    main()
