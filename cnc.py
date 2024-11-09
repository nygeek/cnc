#!/usr/bin/python3

""" Implementation of the CNC calculator using the
    HP35Stack class implemented in hp35stack.py and the Debug
    class implemented in trace_debug.py

Started 2024-11-07 by Marc Donner

Copyright (C) 2024 Marc Donner

$Id$

"""

# ----- Python Libraries ----- #
import cmath
import sys

# ----- CNC libraries ----- #
from hp35stack import HP35Stack
from trace_debug import DebugTrace

# ----- Variables ----- #

DEBUG = DebugTrace(False)

"""
The two functions binary() and unary() are generic mechanisms for
most of the CNC calculator functionality.  They replace a raft of
machinery that I was able to rip out.  They are dispatched using
function references stored in the BUTTONS dictionary.

As of 2024-11-06 six buttons are bound to binary
As of 2024-11-06 sixteen buttons are bound to unary
As of 2024-11-06 seventeen buttons are bound to sixteen unique handlers
("help" and "?" are synonyms)
"""

class ComplexNumberCalculator:
    """ Class to implement the CNC-35 calculator """

    def __init__(self, stack_depth=4, clamp=1e-10):
        """ Set up the structure of the calculator. """
        self.stack = HP35Stack(stack_depth, rel_tol=clamp)
        self.clamp = clamp

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
                  lambda _x, _y: _y - _x],
            "/": [self.binary, "divide y by x",
                  lambda _x, _y: _y / _x if _x != 0 else _y],
            "*": [self.binary, "multiply y by x",
                  lambda _x, _y: _x * _y],
            "+": [self.binary, "add x and y",
                  lambda _x, _y: _x + _y],
            "arccos": [self.unary, "replace x with arccos(x)",
                    cmath.acos],
                    # lambda _x: cmath.acos(_x)],
            "arcsin": [self.unary, "replace x with arcsin(x)",
                    cmath.asin],
            "arctan": [self.unary, "replace x with arctan(x)",
                       cmath.atan],
            "arg": [self.unary, "replace x with arg(x)",
                    cmath.phase],
            "chs": [self.unary, "reverse the sign of x",
                    lambda _x: -(_x)],
            "clr": [self.clr, "clear the stack", self.no_op],
            "clx": [self.clx, "clear the x register", self.no_op],
            "cos": [self.unary, "replace x with cos(x)",
                    cmath.cos],
            "debug": [self.debug, "toggle the debug flag", self.no_op],
            "down": [self.down, "t to z, z to y, y to x, x to z",
                     self.no_op],
            "e": [self.e, "push e onto the stack", self.no_op],
            "eex": [self.binary, "push y * (10^x) onto the stack",
                    lambda _x, _y: _y * (10 ** int(_x.real))],
            "enter": [self.enter, "display the stack", self.no_op],
            "exch": [self.exch, "exchange x and y", self.no_op],
            "exp": [self.unary, "replace x with e^x",
                    cmath.exp],
            "getclamp": [self.get_clamp, "push the clamp value.",
                         self.no_op],
            "help": [self.help, "display documentation", self.no_op],
            "i": [self.i, "push i on to the stack", self.no_op],
            "imag": [self.unary, "put imag(x) into x",
                     lambda _x: _x.imag],
            "inv": [self.unary, "replace x with put 1/x",
                    lambda _x: 1 / _x if _x != 0 else _x],
            "log": [self.unary, "replace x with log(x) - log base 10",
                    cmath.log10],
            "ln": [self.unary, "replace x with ln(x) - natural log",
                   cmath.log],
            "mod": [self.unary, "replace x with mod(x)",
                    abs],
            "pi": [self.pi, "push pi onto the stack", self.no_op],
            "push": [self.push, "push everything up the stack",
                     self.no_op],
            "quit": [self.quit, "exit the calculator", self.no_op],
            "real": [self.unary, "put real(x) into x",
                     lambda _x: _x.real],
            "rcl": [self.rcl, "replace x with the value in M",
                    self.no_op],
            "setclamp": [self.set_clamp,
                         "set the clamp threshold.",
                         self.no_op],
            "sin": [self.unary, "replace x with sin(x)",
                    cmath.sin],
            "sqrt": [self.unary, "replace x with sqrt(x)",
                     cmath.sqrt],
            "sto": [self.sto, "store x into M", self.no_op],
            "tan": [self.unary, "replace x with tan(x)",
                    cmath.tan],
            "xtoy": [self.binary, "put x^y in x, removing both x and y",
                     lambda _x, _y: cmath.exp(cmath.log(_x) * _y)],
            }


    def handle_button_by_name(self, button):
        """ handle a button given its name """
        if button in self.buttons:
            self.stack.increment_count()
            (self.buttons[button][0](self.buttons[button][2]))
            return True
        else:
            return False


    def handle_string(self, text):
        """ handle a command string """
        tokens = text.split(None)
        for token in tokens:
            # is it a button?
            if token in self.buttons:
                # yes
                rc = self.handle_button_by_name(token)
            else:
                # no - assume it's a number
                _number = complex(token)
                self.stack.increment_count()
                self.number(_number)

        self.enter(self.no_op)


    def binary(self, _func):
        """ handle binary operator """
        _x = self.stack.pop()
        _y = self.stack.pop()
        _result = _func(_x, _y)
        self.stack.push(_result)
        return _result


    def unary(self, _func):
        """ handle unary operator """
        _x = self.stack.pop()
        _result = _func(_x)
        self.stack.push(_result)
        return _result


    def set_clamp(self, _func):
        """ set the clamp value """
        self.stack.rel_tol = self.stack.pop().real
        return self.stack.rel_tol


    def get_clamp(self, _func):
        """ push the clamp value onto the stack """
        self.stack.push(0+0j)
        # this avoids applying clamp to the clamp threshold :-)
        self.stack.set_x(self.stack.rel_tol)
        # Do not say "hack!"

# From here on down the methods are listed in alphabetical order #

    def clr(self, _func):
        """ handle clr """
        _zero = complex(0.0, 0.0)
        for _ in range(0, self.stack.depth):
            self.stack.push(_zero)
        return _zero


    def clx(self, _func):
        """ handle clx """
        _zero = complex(0.0, 0.0)
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
        self.stack.push(cmath.e)
        return cmath.e


    def enter(self, _func):
        """ handle enter """
        print(self.stack)
        return self.stack.stack[0]


    def exch(self, _func):
        """ handle exch """
        self.stack.exch()
        return self.stack.stack[0]


    def help(self, _func):
        """ handle help """
        print("Complex Calculator")
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
        return 100


    def i(self, _func):
        """ handle i (also handles j) """
        _result = complex(0, 1)
        self.stack.push(_result)
        return _result


    def number(self, number):
        """ handle a number entered """
        self.stack.push(number)
        return number


    def pi(self, _func):
        """ handle the pi button """
        _result = cmath.pi
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
