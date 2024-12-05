""" Debug using the system trace facility

    Started 2024-09-03 by Marc Donner (marc.donner@gmail.com)

    Copyright (C) 2024 Marc Donner

"""

# ----- Python Library ----- #
import sys

# ----- Function ----- #

# Notice that this function and the variable DEBUG are
# required for the functioning of the DebugTrace class.
# As such, this module is inherently not well structured.

def trace_calls_and_returns(frame, event, arg):
    """ set up hooks for calls and returns """
    # global DEBUG
    frame_code = frame.f_code
    # frame_locals = frame.f_locals
    method_name = frame_code.co_name
    if method_name in ("__init__", "__str__"):
        return None
    if event == 'call':
        print(f"{DEBUG.indent()}{method_name}()")
        DEBUG.inc()
        return trace_calls_and_returns
    if event == 'return':
        print(f"{DEBUG.indent()}{method_name} => {arg}")
        DEBUG.dec()
        return None
    return None

# ----- Class ----- #

class DebugTrace:
    """ class for debug traces """

    def __init__(self, _flag = False, tracer = trace_calls_and_returns):
        """ Create a debug flag """
        self.tracer = tracer
        self.prefix_step = ".."
        self.indent_count = 0
        self.flag = _flag
        if _flag:
            sys.settrace(self.tracer)


    def __str__(self):
        """ render """
        return str(self.flag)


    def get(self):
        """ what is it? """
        return self.flag


    def set(self):
        """ make it True """
        self.flag = True
        self.indent_count = 0
        sys.settrace(trace_calls_and_returns)

    def clear(self):
        """ make it False """
        self.flag = False
        sys.settrace(None)


    def toggle(self):
        """ flip it """
        if self.flag:
            self.flag = False
            sys.settrace(None)
        else:
            self.flag = True
            self.indent_count = 0
            sys.settrace(self.tracer)
        print(f"Debug is {self}")


    def indent(self):
        """ indent a debug string """
        return self.prefix_step * self.indent_count


    def inc(self):
        """ increment the indent """
        _result = self.indent_count
        self.indent_count += 1
        return _result


    def dec(self):
        """ decrement the indent """
        _result = self.indent_count
        self.indent_count -= 1
        return _result


    def reset(self, _reset = 0):
        """ reset the indent """
        self.indent_count = max(0, _reset)
        return self

# ----- Variable -----#

DEBUG = DebugTrace(False)
