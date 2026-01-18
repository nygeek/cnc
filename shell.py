#!/usr/bin/python3

""" Implementation of the interactive decimal CNC Shell using the
    ComplexNumberCalculator class in cnc10.py, the CMath10 class
    implemented in cmath10.py and math10.py based on decimal.py,
    the HP35Stack class implemented in hp35stack.py and the DebugTrace
    class implemented in trace_debug.py

Started 2024-08-22 by Marc Donner
Forked from cnc_shell.py 2026-01-14 by Marc Donner

Copyright (C) 2026 Marc Donner

"""

# ----- Python Libraries ----- #
import argparse

# ----- Calculator libraries ----- #
from trace_debug import DebugTrace

# ----- Variables ----- #

DEBUG = DebugTrace(False)


def main():
    """ Handle command line arguments and then call the shell. """
    mode = "Decimal"
    parser = argparse.ArgumentParser(
            description='Decimal CNC complex number calculator.')
    parser.add_argument('-d', '--debug', dest='debug',
                        action='store_true',
                        help="Turn on debugging.")
    parser.add_argument('--depth', type=int, dest='depth',
                        help="Set stack depth.")
    parser.add_argument('-10', '--decimal', dest='mode',
                        action='store_const', const='decimal',
                        help="Use the decimal kernel.")
    parser.add_argument('-2', '--binary', dest='mode',
                        action='store_const', const='binary',
                        help="Use the binary kernel.")
    args = parser.parse_args()
    if args.debug:
        DEBUG.set()
    depth = 8
    if args.depth is not None and args.depth >= 4:
        depth = args.depth
    if args.mode == 'decimal':
        print(f"Using decimal kernel.")
        application_name = "cnc10"
        from cnc10 import ComplexNumberCalculator
    else:
        print(f"Using binary kernel.")
        application_name = "cnc"
        from cnc import ComplexNumberCalculator

    cnc_shell(ComplexNumberCalculator, depth, name=application_name)


def cnc_shell(kernel, depth=8, name=">"):
    """ The calculator's CLI.
    """

    # initialize the calculator
    cnc = kernel(depth)

    running = True
    while running:
        try:
            line = input(f"{name}[{cnc.stack.get_count()}]> ")
            _rc = cnc.handle_string(line)
            # Nothing left
            print(cnc.stack)

        except EOFError:
            print(f"count[EOF]: {cnc.stack.get_count()}")
            running = False


if __name__ == "__main__":
    main()
