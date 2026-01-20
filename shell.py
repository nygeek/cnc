#!/usr/bin/python3

""" Implementation of the interactive CNC Shell.

    The calculator is polymorphic:

    With the --binary command-line argument it runs with a kernel
    based on the native Python complex type and the cmath library.

    With the --decimal command-line argument it runs with a kernel
    based on the decimal.py module plus two math modules built
    on top of that: math10, which augments the decimal module
    with functions from the math module, and cmath10, which
    adds decimal versions of the functions from cmath.

    It uses the hp35stack module to implement the stack behavior
    of the original HP35 calculator from 1972.

    It also incorporates the DebugTrace class implemented in
    trace_debug.py

Started 2024-08-22 by Marc Donner
Derived from cnc_shell.py 2026-01-14 by Marc Donner

Copyright (C) 2026 Marc Donner

"""

# ----- Python Libraries ----- #
import argparse

# ----- Calculator libraries ----- #
from trace_debug import DebugTrace
from cnc import ComplexNumberCalculator
from cnc10 import ComplexNumberCalculator as ComplexNumberCalculator10

# ----- Variables ----- #

DEBUG = DebugTrace(False)


def main():
    """ Handle command line arguments and then call the shell. """
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
        print("Using decimal kernel.")
        application_name = "cnc10"
        cnc_shell(ComplexNumberCalculator10, depth, name=application_name)
    else:
        print("Using binary kernel.")
        application_name = "cnc"
        cnc_shell(ComplexNumberCalculator, depth, name=application_name)


def cnc_shell(kernel, depth=8, name=">"):
    """ The calculator's CLI.
    """

    # initialize the calculator
    cnc = kernel(depth)

    running = True
    while running:
        try:
            line = input(f"{name}[{cnc.stack.get_count()}]> ").lower()
            _rc = cnc.handle_string(line)
            # Nothing left
            print(cnc.stack)

        except EOFError:
            print(f"count[EOF]: {cnc.stack.get_count()}")
            running = False


if __name__ == "__main__":
    main()
