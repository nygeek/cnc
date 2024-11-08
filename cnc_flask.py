#!/usr/bin/python3

""" Implementation of the web UI for the CNC using:
    [1] ComplexNumberCalculator class in cnc.py,
    [2] HP35Stack class implemented in hp35stack.py
    [3] DebugTrace class implemented in trace_debug.py

Started 2024-08-22 by Marc Donner

Copyright (C) 2024 Marc Donner

$Id$

"""

# ----- Python Libraries ----- #
from flask import Flask, render_template

# ----- CNC libraries ----- #
from cnc import ComplexNumberCalculator
from trace_debug import DebugTrace

# ----- Variables ----- #

APPLICATION_NAME = 'CNC-WEB'
DEBUG = DebugTrace(False)

cnc = Flask(__name__)
cnc_engine = ComplexNumberCalculator(stack_depth=8, clamp=1e-10)

@cnc.route("/")
def index():
    """ display the calculator framework """
    cnc_engine.stack.push(complex(17))
    return render_template('cnc-35.html',
                           stack=cnc_engine.stack,
                           appname=APPLICATION_NAME)

def cnc_shell(depth=8, clamp=1e-10):
    """ The calculator's CLI.
    """

    # initialize the calculator
    cnc = ComplexNumberCalculator(depth, clamp)

    running = True
    while running:
        try:
            line = input(f"{APPLICATION_NAME}[{cnc.stack.get_count()}]> ")
            tokens = line.split(None)

            for token in tokens:

                # is it a button?
                if token in cnc.buttons:
                    cnc.stack.increment_count()
                    (cnc.buttons[token][0](cnc.buttons[token][2]))
                    continue

                # is it a number?
                try:
                    _number = complex(token)
                    cnc.stack.increment_count()
                    cnc.number(_number)
                    continue
                except ValueError:
                    # it's not a number
                    print("not a number.")

                print(f"input '{token}' unrecognized.")

            # Nothing left
            cnc.enter(cnc.no_op)


        except EOFError:
            print(f"count[EOF]: {cnc.stack.get_count()}")
            running = False


def main():
    """ Handle command line arguments and then call the shell. """
    # program_name = sys.argv[0]
    parser = argparse.ArgumentParser(
            description='CNC complex number calculator.')
    parser.add_argument('-d', '--debug', dest='debug',
                        action='store_true',
                        help="Turn on debugging.")
    parser.add_argument('--depth', type=int, dest='depth',
                        help="Set stack depth.")
    parser.add_argument('--clamp', type=float, dest='clamp',
                        help="Set the clamp threshold.")
    args = parser.parse_args()
    if args.debug:
        DEBUG.set()
    depth = 8
    if args.depth is not None and args.depth >= 4:
        depth = args.depth
    clamp = 1e-10
    if args.clamp is not None:
        clamp = args.clamp
    cnc_shell(depth, clamp)

