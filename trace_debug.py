""" Debug using the system trace facility

    Started 2024-09-03 by Marc Donner (marc.donner@gmail.com)

    Copyright (C) 2024 Marc Donner

    $Id$

"""

import sys


def trace_calls_and_returns(frame, event, arg):
    """ set up hooks for calls and returns """
    global debug
    frame_code = frame.f_code
    frame_locals = frame.f_locals
    method_name = frame_code.co_name
    if method_name in ("__init__", "__str__"):
        return
    if event == 'call':
        print(f"{debug.indent()}{method_name}()")
        debug.inc()
        return trace_calls_and_returns
    elif event == 'return':
        print(f"{debug.indent()}{method_name} => {arg}")
        debug.dec()
        return


class DebugTrace:
    """ class for debug traces """

    def __init__(self, _debug):
        """ Create a debug flag """
        if _debug:
            sys.settrace(trace_calls_and_returns)
        self.prefix_step = ".."
        self.indent_count = 0
        self.debug = _debug


    def __str__(self):
        """ render """
        return str(self.debug)


    def get(self):
        """ what is it? """
        return self.debug


    def set(self):
        """ make it True """
        self.debug = True
        sys.settrace(trace_calls_and_returns)

    def clear(self):
        """ make it False """
        self.debug = False
        sys.settrace(None)


    def toggle(self):
        """ flip it """
        if self.debug:
            self.debug = False
            sys.settrace(None)
        else:
            self.debug = True
            sys.settrace(trace_calls_and_returns)
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

debug = DebugTrace(True)

def b():
    """ b """
    print("in b()")
    a()
    return 17


def a():
    """ a """
    print("in a()")
    return 2.3


def main():
    """Test"""
    sys.settrace(trace_calls_and_returns)
    a()
    b()


if __name__ == "__main__":
    main()
