#!/usr/bin/python3

""" Implementation of the decimal CNC calculator using the
    HP35Stack class implemented in hp35stack.py and the Debug
    class implemented in trace_debug.py

    If you are content with IEEE 754 floating point, you should
    use cnc.py.  This module, cnc10.py, uses the decimal.py
    library for arbitrary resolution decimal arithmetic.

Started 2024-11-07 by Marc Donner

SPDX-License-Identifier: MIT
Copyright (C) 2026 NYGeek LLC

ToDo:
    [2024-11-10] Add a log of actions ('tape') that we can display
    or save.
        [2024-11-12] Done
    [2024-11-10] Improve error / overflow handling

"""

# ----- Python Libraries ----- #
import re
import sys

# ----- CNC libraries ----- #
from trace_debug import DebugTrace
# import math10
from cmath10 import StdLibAdapter

from hp35stack import HP35Stack
from logcnc import LogCNC


# ----- Variables ----- #

DEBUG = DebugTrace(False)

# ----- Tokenizer ----- #

# NUM is a regular expression that matches an arbitrary
# number (integer, decimal, scientific notation)
NUM =r'[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([Ee][+-]?[0-9]+)?'

TOKEN_PATTERNS = [
    ('COMPLEX',   rf'\({NUM}+\s*,\s*+{NUM}\)'),
    ('NUMBER',    rf'{NUM}'),
    ('OPERATOR',  r'[+\-*/]'),
    ('ALPHA',     r'[a-zA-Z_][a-zA-Z0-9_]*'),
]

def tokenize(text):
    """
    Extract the first token from text.
    Returns (token_type, value, suffix) or (None, None, '')
    """
    # skip leading white space
    text = text.lstrip()
    if not text:
        return (None, None, '')

    # Try each pattern
    for token_type, pattern in TOKEN_PATTERNS:
        match = re.match(pattern, text)
        if match:
            value = match.group(0)
            suffix = text[match.end():]
            return (token_type, value, suffix)

    return ('INVALID', text, '')


#
# The two functions binary() and unary() are generic mechanisms for
# most of the CNC calculator functionality.  They replace a raft of
# machinery that I was able to rip out.  They are dispatched using
# function references stored in the BUTTONS dictionary.
#
# As of 2024-11-06 six buttons are bound to binary
# As of 2024-11-06 sixteen buttons are bound to unary
# As of 2024-11-06 seventeen buttons are bound to sixteen
#                  unique handlers
#

class ComplexNumberCalculator:
    """ Class to implement the decimal CNC-35 calculator """

    def __init__(self, stack_depth=4):
        """ Set up the structure of the calculator. """
        self.stack = HP35Stack(stack_depth, math_mod=StdLibAdapter)
        self.input_number = ""
        self.log = LogCNC()

        # ----- BUTTONS - Dispatch Table ----- #
        # For this dictionary the key is the button name.  In the CLI
        # one simply types the button name to invoke it.
        #
        # The value is a list with three elements:
        # [0] is the function to be invoked to handle the button.
        # [1] is the description of the button for the help documentation
        # [2] is the function to be passed to handle_unary()
        # or handle_binary()
        self.buttons = {
            "?": [self.help, "display documentation", self.no_op],
            "-": [self.binary, "subtract x from y",
                  lambda _x, _y: _y.sub(_x)],
            "/": [self.binary, "divide y by x",
                  lambda _x, _y: _y / _x if _x != 0 else _y],
            "div": [self.binary, "divide y by x",
                  lambda _x, _y: _y.div(_x) if _x != 0 else _y],
            "*": [self.binary, "multiply y by x",
                  lambda _x, _y: _x * _y],
            "mul": [self.binary, "multiply y by x",
                  lambda _x, _y: _x.mul(_y)],
            "+": [self.binary, "add x and y",
                  lambda _x, _y: _x + _y],
            "abs": [self.unary, "replace x with mod(x) [absolute value]",
                    StdLibAdapter.abs],
            "mod": [self.unary, "replace x with mod(x) [absolute value]",
                    StdLibAdapter.abs],
            "acos": [self.unary, "replace x with acos(x)",
                    StdLibAdapter.acos],
            "acosh": [self.unary, "replace x with acosh(x)",
                    StdLibAdapter.acosh],
            "asin": [self.unary, "replace x with asin(x)",
                    StdLibAdapter.asin],
            "asinh": [self.unary, "replace x with asinh(x)",
                    StdLibAdapter.asinh],
            "atan": [self.unary, "replace x with atan(x)",
                       StdLibAdapter.atan],
            "atanh": [self.unary, "replace x with atanh(x)",
                       StdLibAdapter.atanh],
            "arg": [self.unary, "replace x with arg(x)",
                    StdLibAdapter.phase],
            "chs": [self.unary, "reverse the sign of x",
                    lambda _x: _x.mul(StdLibAdapter.complex(-1,0))],
            "clear": [self.clr, "clear the stack", self.no_op],
            "clr": [self.clr, "clear the stack", self.no_op],
            "clx": [self.clx, "clear the x register", self.no_op],
            "cos": [self.unary, "replace x with cos(x)",
                    StdLibAdapter.cos],
            "cosh": [self.unary, "replace x with cosh(x)",
                    StdLibAdapter.cosh],
            "debug": [self.debug, "toggle the debug flag", self.no_op],
            "down": [self.down, "t to z, z to y, y to x, x to z",
                     self.no_op],
            "e": [self.nullary, 
                  "push e onto the stack", StdLibAdapter.e],
            "eex": [self.binary, "push y * (10^x) onto the stack",
                    lambda _x, _y: _y * (10 ** int(_x.real))],
            "enter": [self.enter, "display the stack", self.no_op],
            "exch": [self.exch, "exchange x and y", self.no_op],
            "exp": [self.unary, "replace x with e^x",
                    StdLibAdapter.exp],
            "help": [self.help, "display documentation", self.no_op],
            "i": [self.i, "push i on to the stack", self.no_op],
            "imag": [self.unary, "put imag(x) into x",
                     lambda _x: _x.imag],
            "inv": [self.unary, "replace x with put 1/x",
                    lambda _x: StdLibAdapter.complex(1,0).div(_x) if _x != 0 else _x],
            "j": [self.i, "push i on to the stack", self.no_op],
#           "json": [self.handle_render_stack,
#                    "render the stack as json.",
#                    self.no_op],
            "log": [self.unary, "replace x with log(x) - log base 10",
                    StdLibAdapter.log10],
            "ln": [self.unary, "replace x with ln(x) - natural log",
                   StdLibAdapter.log],
            "pi": [self.nullary, 
                   "push pi onto the stack", StdLibAdapter.pi],
            "push": [self.push, "push everything up the stack",
                     self.no_op],
            "quit": [self.quit, "exit the calculator", self.no_op],
            "real": [self.unary, "put real(x) into x",
                     lambda _x: _x.real],
            "rcl": [self.rcl, "replace x with the value in M",
                    self.no_op],
            "sin": [self.unary, "replace x with sin(x)",
                    StdLibAdapter.sin],
            "sqrt": [self.unary, "replace x with sqrt(x)",
                     StdLibAdapter.sqrt],
            "sto": [self.sto, "store x into M", self.no_op],
            "tan": [self.unary, "replace x with tan(x)",
                    StdLibAdapter.tan],
            "tape": [self.handle_dump_log,
                     "dump the tape.",
                     self.no_op],
            "xtoy": [self.binary, "put x^y in x, removing both x and y",
                     lambda _x, _y:
                     StdLibAdapter.exp(StdLibAdapter.log(_x).mul(_y))],
            }


    def handle_button_by_name(self, button):
        """ handle a button given its name """
        # Caller must validate the name - this code assumes a valid name
        self.input_number = ""
        self.log.log(button)
        if button in self.buttons:
            self.stack.increment_count()
            (self.buttons[button][0](self.buttons[button][2]))
            return True
        return False


    def handle_string(self, text):
        """ handle a command string """
        _result = -1
        while text:
            (ttype, token, rest) = tokenize(text)
            if ttype in ("ALPHA", "OPERATOR") and token in self.buttons:
                # it is a button
                _result = (self.handle_button_by_name(token), token)
            elif ttype == "COMPLEX":
                match = re.match(r'\(([^,]+),([^)]+)\)', token)
                _real_str = match.group(1).strip()
                _imag_str = match.group(2).strip()
                _number = StdLibAdapter.complex(_real_str, _imag_str)
                self.stack.increment_count()
                _result = (self.number(_number), "")
            elif ttype == "NUMBER":
                _number = StdLibAdapter.complex(token)
                self.stack.increment_count()
                _result = (self.number(_number), "")
            else:
                # it is an error
                _result = (-1, "Unrecognized: '" + text + "'")
            text = rest
        return _result


    def binary(self, _func):
        """ handle binary operator """
        _x = self.stack.pop()
        _y = self.stack.pop()
        _result = _func(_x, _y)
        self.stack.push(_result)
        return _result


    def digit(self, _digit):
        """ handle a digit clicked on a 'keyboard' """
        _zero = StdLibAdapter.complex(0, 0)
        _x = self.stack.stack[0]
        if self.input_number == "":
            self.stack.push(_zero)
        if _digit != "dot":
            self.input_number += str(_digit)
        else:
            self.input_number += "."
        _x = complex(float(self.input_number),0)
        self.stack.stack[0] = _x
        return (_x, self.input_number)


    def unary(self, _func):
        """ handle unary operator """
        _x = self.stack.pop()
        # print(f"DEBUG unary(self: {self}, _func: {_func}")
        _result = _func(_x)
        self.stack.push(_result)
        return _result


    def nullary(self, _func):
        """ handle nullary operator """
        _result = _func()
        self.stack.push(_result)
        return _result


# From here on down the methods are listed in alphabetical order #

    def clr(self, _func):
        """ handle clr """
        self.stack.clear()


    def clx(self, _func):
        """ handle clx """
        _zero = StdLibAdapter.complex(0.0, 0.0)
        self.stack.set_x(_zero)
        return _zero


    def debug(self, _func):
        """ handle debug """
        DEBUG.toggle()
        return DEBUG.flag


    def down(self, _func):
        """ handle roll down - rotate the stack downward """
        self.stack.rolldown()
        return self.stack.stack[0]


    def e(self, _func):
        """ put the constant e on the stack """
        self.stack.push(StdLibAdapter.e)
        return StdLibAdapter.e


    def enter(self, _func):
        """ handle enter """
        print("enter()")
        # print(self.stack)
        return self.stack.stack[0]


    def exch(self, _func):
        """ handle exch """
        self.stack.exch()
        return self.stack.stack[0]


    def help(self, _func):
        """ handle help """
        print("Decimal Complex Calculator")
        print("")
        print("This calculator is constructed in honor of the late")
        print("George R Stibitz and 1972's HP35 scientific calculator.\n")
        print("Functionally it behaves like the HP35, but it operates on")
        print("complex numbers.\n")
        print("Euler's identity can be demonstrated by typing")
        print("    'i pi * exp 1 +'\n")
        print("Operations:")
        button_number = 1
        for _button, _info in self.buttons.items():
            print(f"{button_number}: '{_button}' - '{_info[1]}'")
            button_number += 1
        print("")
        print("You may enter a complex number directly by")
        print("surrounding the components with parentheses and")
        print("separating the real and imaginary parts with a comma.")
        print("e.g. (1,1) produces 1+1i")
        return 100


    def i(self, _func):
        """ handle i (also handles j) """
        _result = StdLibAdapter.complex(0, 1)
        self.stack.push(_result)
        return _result


    def number(self, number):
        """ handle a number entered """
        self.log.log(number)
        self.stack.push(number)
        return number


    def pi(self, _func):
        """ handle the pi button """
        _result = StdLibAdapter.pi
        self.stack.push(_result)
        return _result


    def push(self, _func):
        """ handle push (x -> y, and the rest up) """
        _result = self.stack.stack[0]
        self.stack.push(_result)
        return _result


    def quit(self, _func):
        """ handle quit """
        print(f"count: {self.stack.get_count()}")
        print("----- log -----")
        print(self.log)
        sys.exit()


    def rcl(self, _func):
        """ handle rcl """
        self.stack.rcl()
        _result = self.stack.stack[0]
        return _result


    def sto(self, _func):
        """ handle sto """
        _result = self.stack.sto()
        return _result


    def no_op(self, _x):
        """ no_op """
        return _x


#    def handle_render_stack(self, _func):
#        """ Render the stack as JSON """
#        print(self.stack.stack_to_json())


    def handle_dump_log(self, _func):
        """ dump the 'tape' """
        print(f"Tape: {self.log}")
