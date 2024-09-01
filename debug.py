#!/usr/bin/python3

""" Implementation of the Debug class for the CNC calculator

Started 2024-08-27 by Marc Donner

Copyright (C) 2024 Marc Donner

$Id$

"""

class Debug:
    """ class to hold my debug flag """

    def __init__(self, _debug):
        """ Create a debug flag """
        self.prefix_step = ".."
        self.indent_count = 0
        self.debug = _debug


    def get(self):
        """ what is it? """
        return self.debug


    def set(self):
        """ make it True """
        self.debug = True


    def clear(self):
        """ make it False """
        self.debug = False


    def toggle(self):
        """ flip it """
        if self.debug:
            self.debug = False
        else:
            self.debug = True
        print(f"Debug is {self}")


    def indent(self):
        """ indent a debug string """
        return self.prefix_step * self.indent_count


    def inc(self):
        """ increment the indent """
        _result = self.indent_count
        self.indent_count += 1
        return _result


    def reset(self, _reset = 0):
        """ reset the indent """
        self.indent_count = max(0, _reset)
        return self


    def __str__(self):
        """ render """
        return str(self.debug)
