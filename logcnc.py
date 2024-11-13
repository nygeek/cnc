"""

LogCNC class implementation

This module implements a log or "tape" for the ComplexNumberCalculator.

Started 2024-11-12 by Marc Donner
Copyright (c) 2024 Marc Donner

"""

class LogCNC:
    """ LogCNC Class """

    def __init__(self):
        self.log_list = []
        self.depth = 0

    def __str__(self):
        """ render the log """
        _result = ""
        for line in self.log_list:
            _result += line + "\n"
        return _result

    def log(self, line):
        """ append to the log """
        self.depth += 1
        self.log_list.append(str(line))
        print(f"log(line: {line}) ==> depth: {self.depth}")
        return self.depth

def main():
    """ unit test """
    log = LogCNC()
    log.log("one")
    log.log("two")
    log.log("three")
    print(f"log.depth: {log.depth}")
    print(log)

if __name__ == '__main__':
    main()
