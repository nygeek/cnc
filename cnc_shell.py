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

def handle_add(stack):
    """ handle + """
    _x = stack.pop()
    _y = stack.pop()
    _result = _x + _y
    stack.push(_result)
    return _result


def handle_arccos(stack):
    """ handle arccos """
    _x = stack.pop()
    _result = cmath.acos(_x)
    stack.push(_result)
    return _result


def handle_arcsin(stack):
    """ handle arcsin """
    _x = stack.pop()
    _result = cmath.asin(_x)
    stack.push(_result)
    return _result


def handle_arctan(stack):
    """ handle arctan """
    _x = stack.pop()
    _result = cmath.atan(_x)
    stack.push(_result)
    return _result


def handle_arg(stack):
    """ handle arg """
    _x = stack.pop()
    _result = cmath.phase(_x)
    stack.push(_result)
    return _result


def handle_chs(stack):
    """ handle chs - change sign of x """
    _x = stack.pop()
    _result = -x
    stack.push(_result)
    return _result


def handle_clr(stack):
    """ handle clr """
    _zero = complex(0.0, 0.0)
    stack.push(_zero) # t
    stack.push(_zero) # z
    stack.push(_zero) # y
    stack.push(_zero) # x
    stack.sto()
    return _zero


def handle_clx(stack):
    """ handle clx """
    _zero = complex(0.0, 0.0)
    stack.push(_zero)
    return _zero


def handle_cos(stack):
    """ handle cos """
    _x = stack.pop()
    _result = cmath.cos(_x)
    stack.push(_result)
    return _result


def handle_debug(_stack):
    """ handle debug """
    global DEBUG
    DEBUG.toggle()
    return DEBUG.flag


def handle_down(stack):
    """ handle roll down - rotate the stack downward """
    stack.rolldown()
    return stack.get_x()


def handle_e(stack):
    """ put the constant e on the stack """
    stack.push(cmath.e)
    return cmath.e


def handle_eex(stack):
    """ accept an exponent for X """
    exponent = int(stack.pop().real)
    mantissa = stack.get_x()
    stack.set_x(mantissa * (10 ** exponent))
    return stack.get_x()


def handle_enter(stack):
    """ handle enter """
    print(stack)
    return stack.get_x()


def handle_exch(stack):
    """ handle exch """
    stack.exch()
    return stack.get_x()


def handle_exp(stack):
    """ handle exp """
    _x = stack.pop()
    _result = cmath.exp(_x)
    stack.push(_result)
    return _result


def handle_div(stack):
    """ handle / """
    _x = stack.pop()
    _y = stack.pop()
    _result = _y / _x
    stack.push(_result)
    return _result


def handle_help(_stack):
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


def handle_i(stack):
    """ handle i """
    _result = complex(0, 1)
    stack.push(_result)
    return _result


def handle_inv(stack):
    """ handle inv """
    _x = stack.pop()
    _result = 1 / _x
    stack.push(_result)
    return _result


def handle_log(stack):
    """ handle ln """
    _x = stack.pop()
    _result = cmath.log10(_x)
    stack.push(_result)
    return _result


def handle_ln(stack):
    """ handle ln """
    _x = stack.pop()
    _result = cmath.log(_x)
    stack.push(_result)
    return _result


def handle_mod(stack):
    """ handle mod """
    _x = stack.pop()
    _result = abs(_x)
    stack.push(_result)
    return _result


def handle_mul(stack):
    """ handle + """
    _x = stack.pop()
    _y = stack.pop()
    _result = _x * _y
    stack.push(_result)
    return _result


def handle_number(number, stack):
    """ handle a number entered """
    stack.push(number)
    return number


def handle_pi(stack):
    """ handle the pi button """
    _result = cmath.pi
    stack.push(_result)
    return _result


def handle_push(stack):
    """ handle push (x -> y, and the rest up) """
    _result = stack.get_x()
    stack.push(_result)
    return _result


def handle_quit(stack):
    """ handle quit """
    print(f"count: {stack.get_count()}")
    sys.exit()


def handle_rcl(stack):
    """ handle rcl """
    stack.rcl()
    _result = stack.get_x()
    return _result


def handle_sin(stack):
    """ handle sin """
    _x = stack.pop()
    _result = cmath.sin(_x)
    stack.push(_result)
    return _result


def handle_sto(stack):
    """ handle sto """
    _result = stack.sto()
    return _result


def handle_sqrt(stack):
    """ handle sqrt """
    _x = stack.pop()
    _result = cmath.sqrt(_x)
    stack.push(_result)
    return _result


def handle_sub(stack):
    """ handle + """
    _x = stack.pop()
    _y = stack.pop()
    _result = _y - _x
    stack.push(_result)
    return _result


def handle_tan(stack):
    """ handle tan """
    _x = stack.pop()
    _result = cmath.tan(_x)
    stack.push(_result)
    return _result


def handle_xtoy(stack):
    """ handle x to the power of y """
    _x = stack.pop()
    _y = stack.pop()
    _result = cmath.exp(cmath.log(_x) * _y)
    stack.push(_result)
    return _result


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
    "eex": [handle_eex, "multiply X by 10 ** <enter>"],
    "enter": [handle_enter, "display the stack"],
    "exch": [handle_exch, "exchange x and y"],
    "exp": [handle_exp, "replace x with e^x"],
    "down": [handle_down, "t to z, z to y, y to x, x to z"],
    "help": [handle_help, "display documentation"],
    "i": [handle_i, "push i on to the stack"],
    "inv": [handle_inv, "replace x with put 1/x"],
    "log": [handle_log, "replace x with log(x) - log base 10"],
    "ln": [handle_ln, "replace x with ln(x) - natural log"],
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
                    (BUTTONS[token][0](stack))
                    continue

                # is it a number?
                try:
                    _number = complex(token)
                    stack.increment_count()
                    handle_number(_number, stack)
                    continue
                except:
                    # it's not a number
                    print("not a number.")

                print(f"input '{token}' unrecognized.")

            # Nothing left
            handle_enter(stack)


        except EOFError:
            print(f"count[EOF]: {stack.get_count()}")
            running = False


DEBUG = DebugTrace(False)

def main():
    """Test code and basic CLI functionality."""
    cnc_shell()


if __name__ == "__main__":
    main()
