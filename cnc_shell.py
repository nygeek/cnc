#!/usr/bin/python3

""" Implementation of the interactive CNC Shell using the Complex class
    implemented in cnc.py.  Also the HP35Stack class implemented in
    hp35stack.py.  Also the Debug class implemented in debug.py

Started 2024-08-22 by Marc Donner

Copyright (C) 2024 Marc Donner

$Id$

"""

# libraries
import cmath
import sys

# CNC libraries
from hp35stack import HP35Stack
from trace_debug import DebugTrace

APPLICATION_NAME = 'CNC'


def handle_binary(stack, _func):
    """ handle binary operator """
    _x = stack.pop()
    _y = stack.pop()
    _result = _func(_x, _y)
    stack.push(_result)
    return _result


def handle_unary(stack, _func):
    """ handle unary operator """
    _x = stack.pop()
    _result = _func(_x)
    stack.push(_result)
    return _result


def handle_set_clamp(stack, _func):
    """ set the clamp value """
    stack.rel_tol = stack.pop()
    return stack.rel_tol


def handle_get_clamp(stack, _func):
    """ push the clamp value onto the stack """
    stack.push(0+0j)
    # this avoids applying clamp to the clamp threshold :-)
    stack.set_x(stack.rel_tol)
    # Do not say "hack!"


def handle_clr(stack, _func):
    """ handle clr """
    _zero = complex(0.0, 0.0)
    for _ in range(0, stack.depth):
        stack.push(_zero)
    return _zero


def handle_clx(stack, _func):
    """ handle clx """
    _zero = complex(0.0, 0.0)
    stack.set_x(_zero)
    return _zero


def handle_debug(_stack, _func):
    """ handle debug """
    DEBUG.toggle()
    return DEBUG.flag


def handle_down(stack, _func):
    """ handle roll down - rotate the stack downward """
    stack.rolldown()
    return stack.get_x()


def handle_e(stack, _func):
    """ put the constant e on the stack """
    stack.push(cmath.e)
    return cmath.e


def handle_enter(stack, _func):
    """ handle enter """
    print(stack)
    return stack.get_x()


def handle_exch(stack, _func):
    """ handle exch """
    stack.exch()
    return stack.get_x()


def handle_help(_stack, _func):
    """ handle help """
    print("Complex Calculator")
    print("")
    print("This calculator is constructed in honor of the late")
    print("George R Stibitz and of 1972's HP35 scientific calculator.\n")
    print("Functionally it behaves like the HP35, but it operates on")
    print("complex numbers.\n")
    print("Euler's formula can be tested by typing 'i pi * exp 1 +'\n")
    print("Operations:")
    button_number = 1
    for _button, _info in BUTTONS.items():
        print(f"{button_number}: '{_button}' - '{_info[1]}'")
        button_number += 1
    print("")
    return 100


def handle_i(stack, _func):
    """ handle i """
    _result = complex(0, 1)
    stack.push(_result)
    return _result


def handle_number(number, stack):
    """ handle a number entered """
    stack.push(number)
    return number


def handle_pi(stack, _func):
    """ handle the pi button """
    _result = cmath.pi
    stack.push(_result)
    return _result


def handle_push(stack, _func):
    """ handle push (x -> y, and the rest up) """
    _result = stack.get_x()
    stack.push(_result)
    return _result


def handle_quit(stack, _func):
    """ handle quit """
    print(f"count: {stack.get_count()}")
    sys.exit()


def handle_rcl(stack, _func):
    """ handle rcl """
    stack.rcl()
    _result = stack.get_x()
    return _result


def handle_sto(stack):
    """ handle sto """
    _result = stack.sto()
    return _result


def no_op(_x):
    """ no_op """
    return _x


BUTTONS = {
    "?": [handle_help, "display documentation", no_op],
    "-": [handle_binary, "subtract x from y",
          lambda _x, _y: _y - _x],
    "/": [handle_binary, "divide y by x",
          lambda _x, _y: _y / _x if _x != 0 else _y],
    "*": [handle_binary, "multiply y by x",
          lambda _x, _y: _x * _y],
    "+": [handle_binary, "add x and y",
          lambda _x, _y: _x + _y],
    "arccos": [handle_unary, "replace x with arccos(x)",
            cmath.acos],
            # lambda _x: cmath.acos(_x)],
    "arcsin": [handle_unary, "replace x with arcsin(x)",
            cmath.asin],
    "arctan": [handle_unary, "replace x with arctan(x)",
               cmath.atan],
    "arg": [handle_unary, "replace x with arg(x)",
            cmath.phase],
    "chs": [handle_unary, "reverse the sign of x",
            lambda _x: -(_x)],
    "clr": [handle_clr, "clear the stack", no_op],
    "clx": [handle_clx, "clear the x register", no_op],
    "cos": [handle_unary, "replace x with cos(x)",
            cmath.cos],
    "debug": [handle_debug, "toggle the debug flag", no_op],
    "down": [handle_down, "t to z, z to y, y to x, x to z", no_op],
    "e": [handle_e, "push e onto the stack", no_op],
    "eex": [handle_binary, "push y * (10^x) onto the stack",
            lambda _x, _y: _y * (10 ** int(_x.real))],
    "enter": [handle_enter, "display the stack", no_op],
    "exch": [handle_exch, "exchange x and y", no_op],
    "exp": [handle_unary, "replace x with e^x",
            cmath.exp],
    "getclamp": [handle_get_clamp, "push the clamp value.", no_op],
    "help": [handle_help, "display documentation", no_op],
    "i": [handle_i, "push i on to the stack", no_op],
    "imag": [handle_unary, "put imag(x) into x",
             lambda _x: _x.imag],
    "inv": [handle_unary, "replace x with put 1/x",
            lambda _x: 1 / _x if _x != 0 else _x],
    "log": [handle_unary, "replace x with log(x) - log base 10",
            cmath.log10],
    "ln": [handle_unary, "replace x with ln(x) - natural log",
           cmath.log],
    "mod": [handle_unary, "replace x with mod(x)",
            abs],
    "pi": [handle_pi, "push pi onto the stack", no_op],
    "push": [handle_push, "push everything up the stack", no_op],
    "quit": [handle_quit, "exit the calculator", no_op],
    "real": [handle_unary, "put real(x) into x",
             lambda _x: _x.real],
    "rcl": [handle_rcl, "replace x with the value in M", no_op],
    "setclamp": [handle_set_clamp, "set the clamp threshold.", no_op],
    "sin": [handle_unary, "replace x with sin(x)",
            cmath.sin],
    "sqrt": [handle_unary, "replace x with sqrt(x)",
             cmath.sqrt],
    "sto": [handle_sto, "store x into M", no_op],
    "tan": [handle_unary, "replace x with tan(x)",
            cmath.tan],
    "xtoy": [handle_binary, "put x^y in x, removing both x and y",
             lambda _x, _y: cmath.exp(cmath.log(_x) * _y)],
    }


def cnc_shell():
    """ The shell supporting interactive use of the Complex machinery.
    """

    # initialize the calculator storage
    stack = HP35Stack(8)

    running = True
    while running:
        try:
            line = input(f"{APPLICATION_NAME}[{stack.get_count()}]> ")
            tokens = line.split(None)

            for token in tokens:

                # is it a button?
                if token in BUTTONS:
                    stack.increment_count()
                    (BUTTONS[token][0](stack, BUTTONS[token][2]))
                    continue

                # is it a number?
                try:
                    _number = complex(token)
                    stack.increment_count()
                    handle_number(_number, stack)
                    continue
                except ValueError:
                    # it's not a number
                    print("not a number.")

                print(f"input '{token}' unrecognized.")

            # Nothing left
            handle_enter(stack, no_op)


        except EOFError:
            print(f"count[EOF]: {stack.get_count()}")
            running = False


DEBUG = DebugTrace(False)

def main():
    """Test code and basic CLI functionality."""
    cnc_shell()


if __name__ == "__main__":
    main()
