#!/usr/bin/python3

""" Implementation of the interactive CNC Shell using the Complex class
    implemented in cnc.py.  Also the HP35Stack class implemented in
    hp35stack.py.  Also the Debug class implemented in debug.py

Started 2024-08-22 by Marc Donner

Copyright (C) 2024 Marc Donner

$Id$

"""

# libraries
import math
import re
import sys

# Complex class
from cnc import Complex
from hp35stack import HP35Stack
from debug import Debug

APPLICATION_NAME = 'CNC'

def handle_add(stack, debug):
    """ handle + """
    if debug.get():
        print(f"{debug.indent()}handle_add()")
    _old = debug.inc()
    stack.push(stack.pop(debug).add(stack.pop(debug), debug),
               debug)
    debug.reset(_old)


def handle_arccos(stack, debug):
    """ handle arccos """
    if debug.get():
        print(f"{debug.indent()}handle_arccos()")
    _old = debug.inc()
    stack.push(stack.pop(debug).arccos(debug), debug)
    debug.reset(_old)


def handle_arcsin(stack, debug):
    """ handle arcsin """
    if debug.get():
        print(f"{debug.indent()}handle_arcsin()")
    _old = debug.inc()
    stack.push(stack.pop(debug).arcsin(debug))
    debug.reset(_old)


def handle_arctan(stack, debug):
    """ handle arctan """
    if debug.get():
        print(f"{debug.indent()}handle_arctan()")
    _old = debug.inc()
    stack.push(stack.pop(debug).arctan(debug))
    debug.reset(_old)


def handle_arg(stack, debug):
    """ handle arg """
    if debug.get():
        print(f"{debug.indent()}handle_arg()")
    _old = debug.inc()
    stack.push(Complex(stack.pop(debug).arg(debug), 0, debug), debug)
    debug.reset(_old)


def handle_chs(stack, debug):
    """ handle chs - change sign of x """
    if debug.get():
        print(f"{debug.indent()}handle_chs()")
    _old = debug.inc()
    stack.push(stack.pop(debug).chs(debug), debug)
    debug.reset(_old)


def handle_clr(stack, debug):
    """ handle clr """
    if debug.get():
        print(f"{debug.indent()}handle_clr()")
    # philosophical question ... should I use the same instance
    # for all five settings or call Complex(...) for each one?
    _old = debug.inc()
    _zero = Complex(0.0, 0.0, debug)
    stack.push(_zero, debug) # x
    stack.push(_zero, debug) # y
    stack.push(_zero, debug) # z
    stack.push(_zero, debug) # t
    stack.sto(debug)
    debug.reset(_old)


def handle_clx(stack, debug):
    """ handle clx """
    if debug.get():
        print(f"{debug.indent()}handle_clx()")
    _old = debug.inc()
    stack.pop(debug)
    stack.push(Complex(0.0, 0.0, debug), debug)
    debug.reset(_old)


def handle_cos(stack, debug):
    """ handle cos """
    if debug.get():
        print(f"{debug.indent()}handle_cos()")
    _old = debug.inc()
    stack.push(stack.pop(debug).cos(debug),debug)
    debug.reset(_old)


def handle_debug(_stack, debug):
    """ handle debug """
    debug.toggle()
    print(f"debug: {debug.get()}")


def handle_down(stack, debug):
    """ handle roll down - rotate the stack downward """
    if debug.get():
        print(f"{debug.indent()}handle_down()")
    _old = debug.inc()
    stack.rolldown(debug)
    debug.reset(_old)


def handle_e(stack, debug):
    """ put the constant e on the stack """
    if debug.get():
        print(f"{debug.indent()}handle_e()")
    _old = debug.inc()
    stack.push(Complex(math.e, 0, debug), debug)
    debug.reset(_old)


def handle_enter(stack, debug):
    """ handle enter """
    if debug.get():
        print(f"{debug.indent()}handle_enter()")
    print(stack)


def handle_exch(stack, debug):
    """ handle exch """
    if debug.get():
        print(f"{debug.indent()}handle_exch()")
    _old = debug.inc()
    stack.exch(debug)
    debug.reset(_old)


def handle_exp(stack, debug):
    """ handle exp """
    if debug.get():
        print(f"{debug.indent()}handle_exp()")
    _old = debug.inc()
    stack.push(stack.pop(debug).exp(debug), debug)
    debug.reset(_old)


def handle_div(stack, debug):
    """ handle / """
    if debug.get():
        print(f"{debug.indent()}handle_div()")
    _old = debug.inc()
    _x = stack.pop(debug)
    # the pop() below returns what *was* in y at the start
    stack.push(stack.pop(debug).div(_x, debug), debug)
    debug.reset(_old)


def handle_help(_stack, debug):
    """ handle help """
    if debug.get():
        print(f"{debug.indent()}handle_help()")
    print("Complex Calculator")
    print("")
    print("This calculator is constructed in honor of the late")
    print("George R Stibitz and of 1972's HP35 scientific calculator.")
    print("")
    print("Functionally it behaves like the HP35, but it operates on")
    print("complex numbers.")
    print("")
    for _button, _info in BUTTONS.items():
        print(f"Button: '{_button}' - '{_info[1]}'")
    print("")


def handle_i(stack, debug):
    """ handle i """
    if debug.get():
        print(f"{debug.indent()}handle_i()")
    _old = debug.inc()
    stack.push(Complex(0, 1, debug), debug)
    debug.reset(_old)


def handle_inv(stack, debug):
    """ handle inv """
    if debug.get():
        print(f"{debug.indent()}handle_inv()")
    _old = debug.inc()
    stack.push(stack.pop(debug).inv(debug), debug)
    debug.reset(_old)


def handle_ln(stack, debug):
    """ handle ln """
    if debug.get():
        print(f"{debug.indent()}handle_ln()")
    _old = debug.inc()
    stack.push(stack.pop(debug).ln(debug), debug)
    debug.reset(_old)


def handle_mod(stack, debug):
    """ handle mod """
    if debug.get():
        print(f"{debug.indent()}handle_mod()")
    _old = debug.inc()
    stack.push(Complex(stack.pop(debug).mod(debug), 0, debug), debug)
    debug.reset(_old)


def handle_mul(stack, debug):
    """ handle + """
    if debug.get():
        print(f"{debug.indent()}handle_mul()")
    _old = debug.inc()
    stack.push(stack.pop(debug).mul(stack.pop(debug), debug), debug)
    debug.reset(_old)


def handle_number(number, stack, debug):
    """ handle a number entered """
    if debug.get():
        print(f"{debug.indent()}handle_number({number})")
    _old = debug.inc()
    stack.push(Complex(number, 0.0, debug), debug)
    debug.reset(_old)


def handle_pi(stack, debug):
    """ handle the pi button """
    if debug.get():
        print("handle_pi()")
    _old = debug.inc()
    stack.push(Complex(math.pi, 0.0, debug), debug)
    debug.reset(_old)


def handle_push(stack, debug):
    """ handle push (x -> y, and the rest up) """
    if debug.get():
        print(f"{debug.indent()}handle_push()")
    _old = debug.inc()
    stack.push(stack.get_x(debug), debug)
    debug.reset(_old)


def handle_quit(_stack, debug):
    """ handle quit """
    if debug.get():
        print(f"{debug.indent()}handle_quit()")
    # print("count:", count)
    sys.exit()


def handle_rcl(stack, debug):
    """ handle rcl """
    if debug.get():
        print(f"{debug.indent()}handle_rcl()")
    _old = debug.inc()
    stack.rcl(debug)
    debug.reset(_old)


def handle_sin(stack, debug):
    """ handle sin """
    if debug.get():
        print(f"{debug.indent()}handle_sin()")
    _old = debug.inc()
    stack.push(stack.pop(debug).sin(debug), debug)
    debug.reset(_old)


def handle_sto(stack, debug):
    """ handle sto """
    if debug.get():
        print(f"{debug.indent()}handle_sto()")
    _old = debug.inc()
    _x = stack.sto(debug)
    if debug.get():
        print(f"{debug.indent()}==> _x: {_x}")
    debug.reset(_old)


def handle_sqrt(stack, debug):
    """ handle sqrt """
    if debug.get():
        print(f"{debug.indent()}handle_sqrt()")
    _old = debug.inc()
    stack.push(stack.pop(debug).sqrt(debug),debug)
    debug.reset(_old)


def handle_sub(stack, debug):
    """ handle + """
    if debug.get():
        print(f"{debug.indent()}handle_sub(x:{stack[0]}, y:{stack[1]})")
    _old = debug.inc()
    _x = stack.pop(debug)
    # the pop() below returns what *was* in y at the start
    stack.push(stack.pop(debug).sub(_x, debug), debug)
    debug.reset(_old)


def handle_tan(stack, debug):
    """ handle tan """
    if debug.get():
        print(f"{debug.indent()}handle_tan()")
    _old = debug.inc()
    stack.push(stack.pop(debug).tan(debug), debug)
    debug.reset(_old)


def handle_xtoy(stack, debug):
    """ handle x to the power of y """
    if debug.get():
        print(f"{debug.indent()}handle_xtoy()")
    _old = debug.inc()
    _result = stack.pop(debug).ln(debug)
    _result = _result.mul(stack.pop(debug), debug)
    stack.push(_result.exp(debug), debug)
    debug.reset(_old)


BUTTONS = {
    "-": [handle_sub, "subtract x from y"],
    "/": [handle_div, "divide y by x"],
    "*": [handle_mul, "multiply y by x"],
    "+": [handle_add, "add x and y"],
    "arccos": [handle_arccos, "replace x with arccos(x)"],
    "arcsin": [handle_arcsin, "replace x with arcsin(x)"],
    "arctan": [handle_arctan, "replace x with arctan(x)"],
    "arg": [handle_arg, "replace x with arg(x)"],
    "chs": [handle_chs, "reverse the sign of x"],
    "clr": [handle_clr, "clear the stack"],
    "clx": [handle_clx, "clear the x register"],
    "cos": [handle_cos, "replace x with cos(x)"],
    "debug": [handle_debug, "toggle the debug flag"],
    "e": [handle_e, "push e onto the stack"],
    "enter": [handle_enter, "display the stack"],
    "exch": [handle_exch, "exchange x and y"],
    "exp": [handle_exp, "replace x with e^x"],
    "down": [handle_down, "t to z, z to y, y to x, x to z"],
    "help": [handle_help, "display documentation"],
    "i": [handle_i, "push i on to the stack"],
    "inv": [handle_inv, "replace x with put 1/x"],
    "ln": [handle_ln, "replace x with ln(x)"],
    "mod": [handle_mod, "replace x with mod(x)"],
    "pi": [handle_pi, "push pi onto the stack"],
    "push": [handle_push, "push everything up the stack"],
    "quit": [handle_quit, "exit the calculator"],
    "rcl": [handle_rcl, "replace x with the value in M"],
    "sin": [handle_sin, "replace x with sin(x)"],
    "sqrt": [handle_sqrt, "replace x with sqrt(x)"],
    "sto": [handle_sto, "store x into M"],
    "tan": [handle_tan, "replace x with tan(x)"],
    "xtoy": [handle_xtoy, "put x^y in x, removing both x and y"],
    }

def cnc_shell(debug):
    """ The shell supporting interactive use of the Complex machinery.
    """

    # initialize the calculator storage
    stack = HP35Stack(debug)

    count = 0

    number_compiled = re.compile(r"[+|-]?[0-9]+\.?[0-9]*")

    running = True
    while running:
        try:
            line = input(f"{APPLICATION_NAME}> ")
            tokens = line.split(None)

            if debug.get():
                print(f"{debug.indent()}line(pre): '{line}'")
                print(f"{debug.indent()}tokens: {tokens}")

            for token in tokens:
                if debug.get():
                    print(f"{debug.indent()}token: '{token}'")

                # is it a number?
                _r = re.match(number_compiled, token)
                if _r is not None:
                    # it is a number
                    if debug.get():
                        print(f"{debug.indent()}token(numP=T): '{token}'")
                    _number = float(token)
                    count += 1
                    handle_number(_number, stack, debug)
                    continue

                # ok, is it a button?
                if token in BUTTONS:
                    if debug.get():
                        print(f"{debug.indent()}token(buttonP=T):'{token}'")
                    count += 1
                    (BUTTONS[token][0](stack, debug))
                    continue

                print(f"input '{token}' unrecognized.")

            # Nothing left
            handle_enter(stack, debug)


        except EOFError:
            print("count[EOF]:", count)
            running = False


def main():
    """Test code and basic CLI functionality."""
    _debug = Debug(False)
    cnc_shell(_debug)


if __name__ == "__main__":
    main()
