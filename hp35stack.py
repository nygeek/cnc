""" Implementation of the hp35 stack for the CNC calculator

    If I were properly ambitious I would make this class handle
    a stack of arbitrary type, but I will be lazy and make it
    handle only the cmath type complex.

Started 2024-08-30

SPDX-License-Identifier: MIT
Copyright (C) 2024 NYGeek LLC

ToDo:
    [2024-11-23] create a rendering of the stack that has [r, i]
    instead of complex.
    [2024-11-23] add a json serialize for the rendered stack
    [2024-11-23] add a json load for the stack

"""

# --------- Python Libraries --------- #

# import json
from trace_debug import DebugTrace
# import cmath
from cmath10 import StdLibAdapter

# ----- Variables ----- #

DEBUG = DebugTrace(False)

# --------- HP 35 Stack Class --------- #

class HP35Stack:
    """ Class to implement the HP35 Stack and sto/rcl register """

    def __init__(self, depth=4, math_mod=None):
        if math_mod is None:
            # Use Python's built-in
            self.make_complex = complex
        else: # CMath10 or other math module
            self.math = math_mod
            self.make_complex = math_mod.complex
        _zero = self.make_complex(0.0, 0.0)
        self.stack = [_zero] * depth
        self.depth = depth
        self.labels = ['0'] * depth
        for j in range(4, depth):
            self.labels[j] = str(j)
        self.labels[0] = "X"
        self.labels[1] = "Y"
        self.labels[2] = "Z"
        self.labels[3] = "T"
        self.storcl = _zero
        self.count = 0


    def __str__(self):
        _result = "M: " + str(self.storcl) + "\n\n"
        for j in range(self.depth - 1, -1, -1):
            _result += self.labels[j] + ": " + str(self.stack[j]) + "\n"
        return _result


    def push(self, cn):
        """ push a number on to the stack """
        # this destroys the value at the top of the stack
        for j in range(self.depth - 1, 0, -1):
            self.stack[j] = self.stack[j-1]
        self.set_x(cn)
        return cn


    def pop(self):
        """ pop the bottom element (x) from the stack and return it """
        # this rolls the stack down, thus replicating t into z
        _result = self.stack[0]
        for j in range(0, self.depth - 1):
            self.stack[j] = self.stack[j+1]
        return _result


    def rolldown(self):
        """ perform the roll down function """
        _t = self.stack[0]
        for j in range(0, self.depth - 1):
            self.stack[j] = self.stack[j+1]
        self.stack[self.depth - 1] = _t


    def get_count(self):
        """ return the count """
        return self.count


    def increment_count(self):
        """ increment the count of stack interactions """
        self.count += 1
        return self.count


    def set_x(self, new_x):
        """ retrieve the x value from the stack """
        self.stack[0] = new_x
        return self.stack[0]


    def sto(self):
        """ sto function - copy x to M """
        self.storcl = self.stack[0]
        return self.stack[0]


    def rcl(self):
        """ rcl function - copy M to x (push the rest up) """
        self.push(self.storcl)


    def exch(self):
        """ exchange the values of x and y """
        x = self.stack[0]
        self.stack[0] = self.stack[1]
        self.stack[1] = x

    def clear(self):
        """ clear the stack """
        _zero = self.make_complex(0,0)
        self.stack = [_zero] * self.depth
        self.storcl = _zero


#    def stack_to_json(self):
#        """ a json representation of the stack """
#        stack = [[0, 0]] * self.depth
#        result = {}
#        for i in range(0, self.depth):
#            stack[i] = [self.stack[i].real, self.stack[i].imag]
#        result['stack'] = stack
#        result['storcl'] = [self.storcl.real, self.storcl.imag]
#        result['depth'] = self.depth
#        result['count'] = self.count
#        return json.dumps(result)
#
#    @classmethod
#    def load_stack_from_json(cls, stack_as_json):
#        """ given a json string, reconstitute the stack """
#        new = json.loads(stack_as_json)
#        if 'depth' in new:
#            self.depth = new['depth']
#        if 'count' in new:
#            self.count = new['count']
#        if 'stack' in new:
#            for j in range(0, self.depth):
#                self.stack[j] = self.make_complex(new['stack'][j][0], new['stack'][j][1])
#        if 'storcl' in new:
#            self.storcl = self.make_complex(new['storcl'][0], new['storcl'][1])


def main():
    """ Simple unit tests. """

    stack = HP35Stack(8)
    print(f"Stack:\n{stack}")
    _three = complex(3, 3)
    stack.push(_three)
    _two = complex(2, 2)
    stack.push(_two)
    _one = complex(1, 1)
    stack.push(_one)
    _zero = complex(-1, -1)
    stack.push(_zero)
    print(f"Stack:\n{stack}")
    qq = stack.stack[0]
    print(f"x: {qq}")
    qq = stack.pop()
    print(f"pop =>: {qq}")
    print(f"Stack:\n{stack}")
    stack.push(_two)
    stack.push(_one)
    stack.sto()
    stack.exch()
    stack.rcl()


    print("\nNow trying with CMath10")
    # DEBUG = DebugTrace(False)
    stack10 = HP35Stack(8, math_mod=StdLibAdapter)
    print(f"Stack:\n{stack10}")
    _three = StdLibAdapter.complex(3, 3)
    stack10.push(_three)


if __name__ == '__main__':
    main()
