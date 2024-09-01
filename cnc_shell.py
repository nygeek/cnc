#!/usr/bin/python3

""" Implementation of the interactive CNC Shell using the Complex class
    implemented in cnc.py

Started 2024-08-22 by Marc Donner

Copyright (C) 2024 Marc Donner

"""

import cnc

APPLICATION_NAME = 'CNC Shell'

def cnc_shell():
    """ The shell supporting interactive use of the Complex machinery.
    """

    running = True
    tokens = []
    while running:
        try:
            line = input("> ")
            tokens = line.split(None, 1)
            token = tokens[0].lower() if tokens else ""
            print("token: ", token)
        except EOFError:
            print("\n # EOF ...")
            running = False


def main():
    """Test code and basic CLI functionality."""
    cnc_shell()


if __name__ == "__main__":
    main()
