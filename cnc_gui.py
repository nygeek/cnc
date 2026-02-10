#!/usr/bin/env python3

"""
HP-35 GUI Calculator Implementation using PySDL2

This module implements a faithful pixel-perfect GUI replica of the 1972 HP-35
calculator.

SPDX-License-Identifier: MIT
Copyright (C) 2026 NYGeek LLC

Requirements:
    - Python 3.5+
    - PySDL2
    - SDL2 libraries (libSDL2, libSDL2_gfx)

Usage:
    python3 cnc_gui.py
"""

import sys
import math
import ctypes
from ctypes import c_int, c_short, c_uint8, POINTER

try:
    import sdl2
    import sdl2.ext
    import sdl2.sdlgfx
except ImportError:
    print("Error: PySDL2 not found. Install with: pip install pysdl2")
    sys.exit(1)

from cnc import ComplexNumberCalculator


# ===== Constants ===== #

WINDOW_WIDTH = 380
WINDOW_HEIGHT = 800  # Authentic HP-35 proportions matching reference aspect ratio

# Color palette - Based on authentic HP-35 reference photo
COLORS = {
    # Case and background
    'CASE_BLACK':       (85, 82, 78),  # Medium gray-brown metal case
    'DISPLAY_BG':       (15, 5, 5),    # Very dark red-tinted background

    # LED colors - Classic red LEDs
    'LED_ON':           (255, 60, 40),
    'LED_DIM':          (40, 10, 8),
    'LED_GLOW':         (255, 100, 80),

    # Button colors - Original HP-35 (from reference photo)
    'TAN':              (240, 235, 220),   # Off-white/cream digit buttons (slightly lighter)
    'BLUE':             (90, 170, 210),    # Light cyan operator buttons (slightly darker)
    'BLACK_KEY':        (60, 58, 56),      # Dark charcoal function buttons (lighter than before)

    # Text colors
    'WHITE_TEXT':       (255, 255, 255),
    'BLACK_TEXT':       (0, 0, 0),

    # Button states
    'BUTTON_HOVER':     (200, 200, 200),
    'BUTTON_PRESSED':   (100, 100, 100),
}

# Display dimensions from design.md Section 3.1
DISPLAY_AREA = {
    'x': 25,
    'y': 30,
    'width': 330,
    'height': 170,
}

# Display bezel (frame around display)
DISPLAY_BEZEL = {
    'x': 20,
    'y': 20,
    'width': 340,
    'height': 180,
    'border_width': 3,
}

# Seven-segment digit dimensions from design.md Section 2.1
DIGIT_WIDTH = 20
DIGIT_HEIGHT = 32
SEGMENT_WIDTH = 3
SEGMENT_GAP = 1

# Button name to calculator command mapping from design.md Section 1.6
BUTTON_COMMANDS = {
    # Row 0
    'sqrt':   'sqrt',
    'arcsin': 'asin',
    'arccos': 'acos',
    'arctan': 'atan',
    '1/x':    'inv',

    # Row 1
    'x^y':    'xtoy',
    'ln':     'ln',
    'log':    'log',
    'e^x':    'exp',
    'CLR':    'clr',

    # Row 2
    'STO':    'sto',
    'RCL':    'rcl',
    'R↓':     'down',
    'x↔y':    'exch',
    'CLx':    'clx',

    # Row 3
    'ENTER':  'enter',
    'CHS':    'chs',
    'EEX':    'eex',

    # Row 4
    'sin':    'sin',
    '7':      '7',
    '8':      '8',
    '9':      '9',
    '÷':      '/',

    # Row 5
    'cos':    'cos',
    '4':      '4',
    '5':      '5',
    '6':      '6',
    '×':      '*',

    # Row 6
    'tan':    'tan',
    '1':      '1',
    '2':      '2',
    '3':      '3',
    '−':      '-',

    # Row 7
    'π':      'pi',
    '0':      '0',
    '•':      '.',
    'Σ+':     '+',
    '+':      '+',
}

# Character to seven-segment mapping from design.md Section 2.2
SEGMENT_MAP = {
    '0': ['A', 'B', 'C', 'D', 'E', 'F'],
    '1': ['B', 'C'],
    '2': ['A', 'B', 'G', 'E', 'D'],
    '3': ['A', 'B', 'G', 'C', 'D'],
    '4': ['F', 'G', 'B', 'C'],
    '5': ['A', 'F', 'G', 'C', 'D'],
    '6': ['A', 'F', 'G', 'E', 'D', 'C'],
    '7': ['A', 'B', 'C'],
    '8': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    '9': ['A', 'B', 'C', 'D', 'F', 'G'],
    'A': ['A', 'B', 'C', 'E', 'F', 'G'],
    'B': ['C', 'D', 'E', 'F', 'G'],
    'C': ['A', 'D', 'E', 'F'],
    'D': ['B', 'C', 'D', 'E', 'G'],
    'E': ['A', 'D', 'E', 'F', 'G'],
    'F': ['A', 'E', 'F', 'G'],
    '-': ['G'],
    ' ': [],
    '.': [],
}

# Simple 5x7 bitmap font for button labels
CHAR_PATTERNS = {
    '0': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    '1': [[0,0,1,0,0], [0,1,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,1,1,1,0]],
    '2': [[0,1,1,1,0], [1,0,0,0,1], [0,0,0,0,1], [0,0,1,1,0], [0,1,0,0,0], [1,0,0,0,0], [1,1,1,1,1]],
    '3': [[1,1,1,1,0], [0,0,0,0,1], [0,0,0,1,0], [0,0,1,1,0], [0,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    '4': [[0,0,0,1,0], [0,0,1,1,0], [0,1,0,1,0], [1,0,0,1,0], [1,1,1,1,1], [0,0,0,1,0], [0,0,0,1,0]],
    '5': [[1,1,1,1,1], [1,0,0,0,0], [1,1,1,1,0], [0,0,0,0,1], [0,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    '6': [[0,0,1,1,0], [0,1,0,0,0], [1,0,0,0,0], [1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    '7': [[1,1,1,1,1], [0,0,0,0,1], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [0,1,0,0,0], [0,1,0,0,0]],
    '8': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    '9': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,1], [0,0,0,0,1], [0,0,0,1,0], [0,1,1,0,0]],
    'A': [[0,0,1,0,0], [0,1,0,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1]],
    'C': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,1], [0,1,1,1,0]],
    'D': [[1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,0]],
    'E': [[1,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [1,1,1,1,0], [1,0,0,0,0], [1,0,0,0,0], [1,1,1,1,1]],
    'H': [[1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1]],
    'I': [[1,1,1,1,1], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [1,1,1,1,1]],
    'L': [[1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,1,1,1,1]],
    'N': [[1,0,0,0,1], [1,1,0,0,1], [1,0,1,0,1], [1,0,0,1,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1]],
    'O': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    'R': [[1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,0], [1,0,1,0,0], [1,0,0,1,0], [1,0,0,0,1]],
    'S': [[0,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [0,1,1,1,0], [0,0,0,0,1], [0,0,0,0,1], [1,1,1,1,0]],
    'T': [[1,1,1,1,1], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0]],
    'X': [[1,0,0,0,1], [1,0,0,0,1], [0,1,0,1,0], [0,0,1,0,0], [0,1,0,1,0], [1,0,0,0,1], [1,0,0,0,1]],
    'a': [[0,0,0,0,0], [0,0,0,0,0], [0,1,1,1,0], [0,0,0,0,1], [0,1,1,1,1], [1,0,0,0,1], [0,1,1,1,1]],
    'c': [[0,0,0,0,0], [0,0,0,0,0], [0,1,1,1,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,1], [0,1,1,1,0]],
    'd': [[0,0,0,0,1], [0,0,0,0,1], [0,1,1,0,1], [1,0,0,1,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,1]],
    'e': [[0,0,0,0,0], [0,0,0,0,0], [0,1,1,1,0], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,0], [0,1,1,1,0]],
    'g': [[0,0,0,0,0], [0,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,1], [0,0,0,0,1], [0,1,1,1,0]],
    'i': [[0,0,1,0,0], [0,0,0,0,0], [0,1,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,1,1,1,0]],
    'j': [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,1,0], [0,0,0,0,0], [0,0,0,1,0], [1,0,0,1,0], [0,1,1,0,0]],
    'k': [[1,0,0,0,0], [1,0,0,0,0], [1,0,0,1,0], [1,0,1,0,0], [1,1,0,0,0], [1,0,1,0,0], [1,0,0,1,0]],
    'l': [[0,1,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,1,1,1,0]],
    'n': [[0,0,0,0,0], [0,0,0,0,0], [1,0,1,1,0], [1,1,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1]],
    'o': [[0,0,0,0,0], [0,0,0,0,0], [0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
    'r': [[0,0,0,0,0], [0,0,0,0,0], [1,0,1,1,0], [1,1,0,0,1], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0]],
    's': [[0,0,0,0,0], [0,0,0,0,0], [0,1,1,1,0], [1,0,0,0,0], [0,1,1,1,0], [0,0,0,0,1], [1,1,1,1,0]],
    't': [[0,1,0,0,0], [0,1,0,0,0], [1,1,1,0,0], [0,1,0,0,0], [0,1,0,0,0], [0,1,0,0,0], [0,0,1,1,0]],
    'x': [[0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,1], [0,1,0,1,0], [0,0,1,0,0], [0,1,0,1,0], [1,0,0,0,1]],
    'y': [[0,0,0,0,0], [0,0,0,0,0], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,1], [0,0,0,0,1], [0,1,1,1,0]],
    '/': [[0,0,0,0,1], [0,0,0,1,0], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [0,1,0,0,0], [1,0,0,0,0]],
    '+': [[0,0,0,0,0], [0,0,1,0,0], [0,0,1,0,0], [1,1,1,1,1], [0,0,1,0,0], [0,0,1,0,0], [0,0,0,0,0]],
    '−': [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,1,1,1,1], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
    '×': [[0,0,0,0,0], [1,0,0,0,1], [0,1,0,1,0], [0,0,1,0,0], [0,1,0,1,0], [1,0,0,0,1], [0,0,0,0,0]],
    '÷': [[0,0,0,0,0], [0,0,1,0,0], [0,0,0,0,0], [1,1,1,1,1], [0,0,0,0,0], [0,0,1,0,0], [0,0,0,0,0]],
    '•': [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,1,1,0,0], [0,1,1,0,0]],
    'π': [[0,0,0,0,0], [1,1,1,1,1], [0,1,0,1,0], [0,1,0,1,0], [0,1,0,1,0], [0,1,0,1,0], [0,1,0,1,0]],
    '^': [[0,0,1,0,0], [0,1,0,1,0], [1,0,0,0,1], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
    '↓': [[0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [1,0,1,0,1], [0,1,1,1,0], [0,0,1,0,0], [0,0,0,0,0]],
    '↔': [[0,0,0,0,0], [0,1,0,1,0], [1,1,1,1,1], [0,1,0,1,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
    'Σ': [[1,1,1,1,1], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [0,0,1,0,0], [0,0,0,1,0], [1,1,1,1,1]],
    '√': [[0,0,0,0,1], [0,0,0,0,1], [1,0,0,0,1], [1,0,0,1,0], [0,1,1,0,0], [0,0,0,0,0], [0,0,0,0,0]],
    ' ': [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
}


# ===== Helper Functions ===== #

def get_text_color(button_color):
    """
    Return appropriate text color for given button color.

    Args:
        button_color: RGB tuple of button background

    Returns:
        RGB tuple for text color
    """
    brightness = sum(button_color) / 3
    if brightness > 128:
        return COLORS['BLACK_TEXT']
    else:
        return COLORS['WHITE_TEXT']


def format_number_for_display(value):
    """
    Format number for LED display (handles complex numbers).

    Args:
        value: Number to format

    Returns:
        String formatted for LED display (up to 15 characters)
    """
    if isinstance(value, complex):
        if value.imag == 0:
            # Real number
            return format_scientific(value.real)
        else:
            # Complex number - show magnitude and phase or real/imag
            return format_scientific(value.real)[:13] + " i"
    else:
        return format_scientific(float(value))


def format_scientific(num, precision=9):
    """
    Format number in scientific notation for display.

    Args:
        num: Number to format
        precision: Number of mantissa digits after decimal

    Returns:
        String like " 1.234567890 E+00"
    """
    if num == 0:
        return " 0.000000000 E+00"

    # Calculate exponent and mantissa
    exponent = math.floor(math.log10(abs(num)))
    mantissa = num / (10 ** exponent)

    # Format components
    sign = '-' if num < 0 else ' '
    exp_sign = '+' if exponent >= 0 else '-'

    # Build display string
    mantissa_str = f"{abs(mantissa):.{precision}f}"
    exp_str = f"{abs(exponent):02d}"

    return f"{sign}{mantissa_str} E{exp_sign}{exp_str}"


# ===== Button Class ===== #

class ButtonState:
    """Enumeration of button states"""
    NORMAL = 0
    HOVER = 1
    PRESSED = 2
    RELEASED = 3


class Button:
    """
    Data structure representing a single calculator button.
    """

    def __init__(self, x, y, width, height, label, command, color):
        """
        Initialize button.

        Args:
            x, y: Top-left position (pixels)
            width, height: Button dimensions (pixels)
            label: Display text on button
            command: Calculator command string
            color: RGB tuple for button background
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.command = command
        self.color = color
        self.text_color = get_text_color(color)
        self.state = ButtonState.NORMAL
        self.callback = None

    def contains_point(self, px, py):
        """
        Check if point (px, py) is inside button bounds.

        Returns:
            True if point is inside button, False otherwise
        """
        return (self.x <= px <= self.x + self.width and
                self.y <= py <= self.y + self.height)

    def get_render_color(self):
        """
        Get color to render based on current state.

        Returns:
            RGB tuple
        """
        if self.state == ButtonState.PRESSED:
            # Darken button when pressed
            return tuple(max(0, c - 50) for c in self.color)
        elif self.state == ButtonState.HOVER:
            # Lighten button when hovering
            return tuple(min(255, c + 30) for c in self.color)
        else:
            # Normal color
            return self.color


# ===== ButtonGrid Class ===== #

class ButtonGrid:
    """
    Collection of buttons with rendering and hit detection.
    """

    def __init__(self):
        self.buttons = []
        self._build_button_layout()

    def _build_button_layout(self):
        """
        Construct all 47 buttons with exact positions from design.md Section 1.4-1.5.
        """
        # Compact button dimensions matching authentic HP-35
        btn_w = 59   # Button width
        btn_h = 54   # Button height
        gap = 7      # Gap between buttons (very tight)
        x_start = 27   # Left margin (adjusted for wider buttons)
        y_start = 245  # Top margin (below display, room for labels)

        # Calculate column positions
        x0 = x_start
        x1 = x0 + btn_w + gap
        x2 = x1 + btn_w + gap
        x3 = x2 + btn_w + gap
        x4 = x3 + btn_w + gap

        # Calculate row positions
        y0 = y_start
        y1 = y0 + btn_h + gap
        y2 = y1 + btn_h + gap
        y3 = y2 + btn_h + gap
        y4 = y3 + btn_h + gap
        y5 = y4 + btn_h + gap
        y6 = y5 + btn_h + gap
        y7 = y6 + btn_h + gap

        # Row 0 - Top function row (authentic HP-35 layout)
        self.buttons.extend([
            Button(x0, y0, btn_w, btn_h, 'x^y',    'xtoy',   COLORS['BLACK_KEY']),
            Button(x1, y0, btn_w, btn_h, 'log',    'log',    COLORS['BLACK_KEY']),
            Button(x2, y0, btn_w, btn_h, 'ln',     'ln',     COLORS['BLACK_KEY']),
            Button(x3, y0, btn_w, btn_h, 'e^x',    'exp',    COLORS['BLACK_KEY']),
            Button(x4, y0, btn_w, btn_h, 'CLR',    'clr',    COLORS['BLUE']),
        ])

        # Row 1 - Second function row (trig functions)
        self.buttons.extend([
            Button(x0, y1, btn_w, btn_h, 'sqrt',   'sqrt',   COLORS['BLACK_KEY']),
            Button(x1, y1, btn_w, btn_h, 'arc',    'asin',   COLORS['BLACK_KEY']),  # arc is inverse trig
            Button(x2, y1, btn_w, btn_h, 'sin',    'sin',    COLORS['BLACK_KEY']),
            Button(x3, y1, btn_w, btn_h, 'cos',    'cos',    COLORS['BLACK_KEY']),
            Button(x4, y1, btn_w, btn_h, 'tan',    'tan',    COLORS['BLACK_KEY']),
        ])

        # Row 2 - Third function row (STO/RCL row)
        self.buttons.extend([
            Button(x0, y2, btn_w, btn_h, 'x↔y',    'exch',   COLORS['BLACK_KEY']),
            Button(x1, y2, btn_w, btn_h, 'R↓',     'down',   COLORS['BLACK_KEY']),
            Button(x2, y2, btn_w, btn_h, 'STO',    'sto',    COLORS['BLACK_KEY']),
            Button(x3, y2, btn_w, btn_h, 'RCL',    'rcl',    COLORS['BLACK_KEY']),
            Button(x4, y2, btn_w, btn_h, 'CLx',    'clx',    COLORS['BLUE']),
        ])

        # Row 3 - ENTER is double-wide
        enter_w = btn_w * 2 + gap
        self.buttons.extend([
            Button(x0, y3, enter_w, btn_h, 'ENTER', 'enter',  COLORS['BLUE']),
            Button(x2, y3, btn_w,   btn_h, 'CHS',   'chs',    COLORS['BLACK_KEY']),
            Button(x3, y3, btn_w,   btn_h, 'EEX',   'eex',    COLORS['BLACK_KEY']),
            Button(x4, y3, btn_w,   btn_h, 'CLR',   'clr',    COLORS['BLUE']),
        ])

        # Row 4 - Number pad (authentic HP-35: operators on left and right)
        self.buttons.extend([
            Button(x0, y4, btn_w, btn_h, '−',      '-',      COLORS['BLUE']),
            Button(x1, y4, btn_w, btn_h, '7',      '7',      COLORS['TAN']),
            Button(x2, y4, btn_w, btn_h, '8',      '8',      COLORS['TAN']),
            Button(x3, y4, btn_w, btn_h, '9',      '9',      COLORS['TAN']),
            Button(x4, y4, btn_w, btn_h, '÷',      '/',      COLORS['BLUE']),
        ])

        # Row 5
        self.buttons.extend([
            Button(x0, y5, btn_w, btn_h, '+',      '+',      COLORS['BLUE']),
            Button(x1, y5, btn_w, btn_h, '4',      '4',      COLORS['TAN']),
            Button(x2, y5, btn_w, btn_h, '5',      '5',      COLORS['TAN']),
            Button(x3, y5, btn_w, btn_h, '6',      '6',      COLORS['TAN']),
            Button(x4, y5, btn_w, btn_h, '×',      '*',      COLORS['BLUE']),
        ])

        # Row 6
        self.buttons.extend([
            Button(x0, y6, btn_w, btn_h, '×',      '*',      COLORS['BLUE']),
            Button(x1, y6, btn_w, btn_h, '1',      '1',      COLORS['TAN']),
            Button(x2, y6, btn_w, btn_h, '2',      '2',      COLORS['TAN']),
            Button(x3, y6, btn_w, btn_h, '3',      '3',      COLORS['TAN']),
            Button(x4, y6, btn_w, btn_h, '−',      '-',      COLORS['BLUE']),
        ])

        # Row 7
        self.buttons.extend([
            Button(x0, y7, btn_w, btn_h, '÷',      '/',      COLORS['BLUE']),
            Button(x1, y7, btn_w, btn_h, '0',      '0',      COLORS['TAN']),
            Button(x2, y7, btn_w, btn_h, '•',      '.',      COLORS['TAN']),
            Button(x3, y7, btn_w, btn_h, 'π',      'pi',     COLORS['TAN']),
            Button(x4, y7, btn_w, btn_h, '+',      '+',      COLORS['BLUE']),
        ])

    def get_button_at(self, x, y):
        """
        Find button at pixel coordinates (x, y).

        Args:
            x, y: Pixel coordinates

        Returns:
            Button object or None if no button at position
        """
        for button in self.buttons:
            if button.contains_point(x, y):
                return button
        return None

    def render(self, renderer):
        """
        Render all buttons to SDL renderer.

        Args:
            renderer: SDL renderer
        """
        for button in self.buttons:
            # Get color based on state
            color = button.get_render_color()

            # Draw simple rectangle button
            sdl2.SDL_SetRenderDrawColor(renderer, *color, 255)
            rect = sdl2.SDL_Rect(button.x, button.y, button.width, button.height)
            sdl2.SDL_RenderFillRect(renderer, rect)

            # Draw border (darker)
            border_color = tuple(max(0, c - 60) for c in color)
            sdl2.SDL_SetRenderDrawColor(renderer, *border_color, 255)
            sdl2.SDL_RenderDrawRect(renderer, rect)

            # Draw text label (centered)
            self._render_button_label(renderer, button)

    def _draw_rounded_rect(self, renderer, x, y, width, height, radius, color):
        """
        Draw a filled rounded rectangle.

        Args:
            renderer: SDL renderer
            x, y: Top-left position
            width, height: Dimensions
            radius: Corner radius
            color: RGB tuple
        """
        # Draw main rectangle body
        sdl2.SDL_SetRenderDrawColor(renderer, *color, 255)

        # Top and bottom rectangles (full width minus corners)
        top_rect = sdl2.SDL_Rect(x + radius, y, width - 2 * radius, radius)
        middle_rect = sdl2.SDL_Rect(x, y + radius, width, height - 2 * radius)
        bottom_rect = sdl2.SDL_Rect(x + radius, y + height - radius, width - 2 * radius, radius)

        sdl2.SDL_RenderFillRect(renderer, top_rect)
        sdl2.SDL_RenderFillRect(renderer, middle_rect)
        sdl2.SDL_RenderFillRect(renderer, bottom_rect)

        # Draw corner circles
        self._draw_filled_circle(renderer, x + radius, y + radius, radius, color)  # Top-left
        self._draw_filled_circle(renderer, x + width - radius, y + radius, radius, color)  # Top-right
        self._draw_filled_circle(renderer, x + radius, y + height - radius, radius, color)  # Bottom-left
        self._draw_filled_circle(renderer, x + width - radius, y + height - radius, radius, color)  # Bottom-right

    def _draw_rounded_rect_outline(self, renderer, x, y, width, height, radius, color, thickness):
        """
        Draw a rounded rectangle outline.

        Args:
            renderer: SDL renderer
            x, y: Top-left position
            width, height: Dimensions
            radius: Corner radius
            color: RGB tuple
            thickness: Line thickness in pixels
        """
        sdl2.SDL_SetRenderDrawColor(renderer, *color, 255)

        for t in range(thickness):
            offset = t
            # Draw four straight edges
            # Top edge
            for px in range(x + radius, x + width - radius):
                sdl2.SDL_RenderDrawPoint(renderer, px, y + offset)
            # Bottom edge
            for px in range(x + radius, x + width - radius):
                sdl2.SDL_RenderDrawPoint(renderer, px, y + height - 1 - offset)
            # Left edge
            for py in range(y + radius, y + height - radius):
                sdl2.SDL_RenderDrawPoint(renderer, x + offset, py)
            # Right edge
            for py in range(y + radius, y + height - radius):
                sdl2.SDL_RenderDrawPoint(renderer, x + width - 1 - offset, py)

    def _draw_filled_circle(self, renderer, cx, cy, radius, color):
        """
        Draw a filled circle using midpoint circle algorithm.

        Args:
            renderer: SDL renderer
            cx, cy: Center position
            radius: Circle radius
            color: RGB tuple
        """
        sdl2.SDL_SetRenderDrawColor(renderer, *color, 255)

        for y in range(-radius, radius + 1):
            for x in range(-radius, radius + 1):
                if x * x + y * y <= radius * radius:
                    sdl2.SDL_RenderDrawPoint(renderer, cx + x, cy + y)

    def _render_button_label(self, renderer, button):
        """
        Render silk-screen label ABOVE button (authentic HP-35 style).

        Args:
            renderer: SDL renderer
            button: Button object
        """
        label = button.label
        if not label:
            return

        # Silk-screen labels are rendered ABOVE the button, not on it
        # Balance visibility with accuracy
        pixel_size = 1  # Smaller for better reference matching
        label_color = (200, 195, 180)  # Muted cream text

        # Handle special multi-character labels
        if label in ('sqrt', 'arcsin', 'arccos', 'arctan', 'x^y', 'e^x', '1/x'):
            self._render_silkscreen_special(renderer, button, label, pixel_size, label_color)
            return

        # Calculate text dimensions
        char_width = 5 * pixel_size
        char_height = 7 * pixel_size
        char_spacing = pixel_size

        # Total width of the label
        total_width = len(label) * char_width + (len(label) - 1) * char_spacing

        # Position label ABOVE the button (silk-screen style)
        start_x = button.x + (button.width - total_width) // 2
        start_y = button.y - char_height - 4  # 4 pixels above button

        # Render each character
        current_x = start_x
        for char in label:
            self._render_char(renderer, char, current_x, start_y, pixel_size, label_color)
            current_x += char_width + char_spacing

    def _render_char(self, renderer, char, x, y, pixel_size, color):
        """
        Render a single character using its bitmap pattern.

        Args:
            renderer: SDL renderer
            char: Character to render
            x, y: Top-left position
            pixel_size: Size of each pixel in the pattern
            color: RGB tuple for character color
        """
        pattern = CHAR_PATTERNS.get(char)
        if not pattern:
            return

        sdl2.SDL_SetRenderDrawColor(renderer, *color, 255)

        for row_idx, row in enumerate(pattern):
            for col_idx, pixel in enumerate(row):
                if pixel:
                    px = x + col_idx * pixel_size
                    py = y + row_idx * pixel_size
                    rect = sdl2.SDL_Rect(px, py, pixel_size, pixel_size)
                    sdl2.SDL_RenderFillRect(renderer, rect)

    def _render_silkscreen_special(self, renderer, button, label, pixel_size, color):
        """
        Render special silk-screen labels above buttons.

        Args:
            renderer: SDL renderer
            button: Button object
            label: Label string
            pixel_size: Size multiplier
            color: RGB tuple for text color
        """
        char_width = 5 * pixel_size
        char_height = 7 * pixel_size

        if label == 'sqrt':
            # Render "√x" above button
            text = '√x'
            total_width = len(text) * char_width
            start_x = button.x + (button.width - total_width) // 2
            start_y = button.y - char_height - 4

            current_x = start_x
            for char in text:
                self._render_char(renderer, char, current_x, start_y, pixel_size, color)
                current_x += char_width + pixel_size

        elif label in ('x^y', 'e^x'):
            # Render with superscript above button
            base = label[0]
            superscript = label[2]

            start_x = button.x + button.width // 2 - char_width
            start_y = button.y - char_height - 4

            self._render_char(renderer, base, start_x, start_y, pixel_size, color)
            self._render_char(renderer, superscript, start_x + char_width, start_y - 2, pixel_size, color)

        elif label == '1/x':
            # Render fraction above button
            text = '1/x'
            total_width = len(text) * char_width
            start_x = button.x + (button.width - total_width) // 2
            start_y = button.y - char_height - 4

            current_x = start_x
            for char in text:
                self._render_char(renderer, char, current_x, start_y, pixel_size, color)
                current_x += char_width + pixel_size

    def _render_special_label(self, renderer, button, label):
        """
        Render special multi-line or complex labels (legacy - now uses silk-screen).

        Args:
            renderer: SDL renderer
            button: Button object
            label: Label string
        """
        # This is now handled by _render_silkscreen_special
        pass

    def _render_superscript(self, renderer, button, base, superscript, pixel_size):
        """Render text with superscript."""
        char_width = 5 * pixel_size
        char_height = 7 * pixel_size
        super_size = 1  # Smaller size for superscript

        # Center position
        center_x = button.x + button.width // 2
        center_y = button.y + button.height // 2

        # Render base character
        base_x = center_x - char_width // 2
        base_y = center_y - char_height // 4
        self._render_char(renderer, base, base_x, base_y, pixel_size, button.text_color)

        # Render superscript (smaller, raised)
        super_x = base_x + char_width
        super_y = base_y - char_height // 4
        self._render_char(renderer, superscript, super_x, super_y, super_size, button.text_color)

    def _render_two_line_label(self, renderer, button, line1, line2, pixel_size):
        """Render two-line label."""
        char_width = 5 * pixel_size
        char_height = 7 * pixel_size
        char_spacing = pixel_size

        # Line 1 (top)
        total_width1 = len(line1) * char_width + (len(line1) - 1) * char_spacing
        start_x1 = button.x + (button.width - total_width1) // 2
        start_y1 = button.y + (button.height - char_height * 2) // 2

        current_x = start_x1
        for char in line1:
            self._render_char(renderer, char, current_x, start_y1, pixel_size, button.text_color)
            current_x += char_width + char_spacing

        # Line 2 (bottom)
        total_width2 = len(line2) * char_width + (len(line2) - 1) * char_spacing
        start_x2 = button.x + (button.width - total_width2) // 2
        start_y2 = start_y1 + char_height + pixel_size

        current_x = start_x2
        for char in line2:
            self._render_char(renderer, char, current_x, start_y2, pixel_size, button.text_color)
            current_x += char_width + char_spacing

    def _render_simple_text(self, renderer, button, text, pixel_size):
        """Render simple centered text."""
        char_width = 5 * pixel_size
        char_height = 7 * pixel_size
        char_spacing = pixel_size

        total_width = len(text) * char_width + (len(text) - 1) * char_spacing
        start_x = button.x + (button.width - total_width) // 2
        start_y = button.y + (button.height - char_height) // 2

        current_x = start_x
        for char in text:
            self._render_char(renderer, char, current_x, start_y, pixel_size, button.text_color)
            current_x += char_width + char_spacing


# ===== LEDDisplay Class ===== #

class LEDDisplay:
    """
    LED display state and seven-segment rendering.
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display_string = " 0.000000000 E+00"
        self.stack_values = [0.0] * 4
        self.memory_value = 0.0

    def update(self, stack):
        """
        Update display from calculator stack.

        Args:
            stack: HP35Stack object
        """
        self.stack_values = stack.stack[:4]
        self.memory_value = stack.storcl

        # Format X register for display
        if len(stack.stack) > 0:
            self.display_string = format_number_for_display(stack.stack[0])
        else:
            self.display_string = " 0.000000000 E+00"

    def render(self, renderer):
        """
        Render LED display to surface.

        Args:
            renderer: SDL renderer
        """
        # Draw background
        sdl2.SDL_SetRenderDrawColor(renderer, *COLORS['DISPLAY_BG'], 255)
        rect = sdl2.SDL_Rect(self.x, self.y, self.width, self.height)
        sdl2.SDL_RenderFillRect(renderer, rect)

        # Render main X register (large LED digits)
        x_display_x = self.x + 20
        x_display_y = self.y + 100
        self._render_led_string(renderer, x_display_x, x_display_y, self.display_string)

    def _render_led_string(self, renderer, x, y, text):
        """
        Render complete LED display string.

        Args:
            renderer: SDL renderer
            x, y: Top-left position
            text: String to display
        """
        digit_spacing = DIGIT_WIDTH + 4
        current_x = x

        for char in text:
            if char == '.':
                # Render decimal point
                self._render_decimal_point(renderer, current_x - 2, y + DIGIT_HEIGHT - 4)
                continue
            else:
                self._render_seven_segment(renderer, current_x, y, char)
            current_x += digit_spacing

    def _render_seven_segment(self, renderer, x, y, char):
        """
        Render a single seven-segment digit.

        Args:
            renderer: SDL renderer
            x, y: Top-left position of digit
            char: Character to render
        """
        # Get segments for this character
        segments_to_light = SEGMENT_MAP.get(char.upper(), [])

        # Define segment positions (lambdas from design.md Section 2.1)
        segment_positions = {
            'A': self._horizontal_segment(x + 2, y, DIGIT_WIDTH - 4),
            'B': self._vertical_segment(x + DIGIT_WIDTH - 4, y + 2, DIGIT_HEIGHT // 2 - 3),
            'C': self._vertical_segment(x + DIGIT_WIDTH - 4, y + DIGIT_HEIGHT // 2 + 1, DIGIT_HEIGHT // 2 - 3),
            'D': self._horizontal_segment(x + 2, y + DIGIT_HEIGHT - 4, DIGIT_WIDTH - 4),
            'E': self._vertical_segment(x, y + DIGIT_HEIGHT // 2 + 1, DIGIT_HEIGHT // 2 - 3),
            'F': self._vertical_segment(x, y + 2, DIGIT_HEIGHT // 2 - 3),
            'G': self._horizontal_segment(x + 2, y + DIGIT_HEIGHT // 2 - 2, DIGIT_WIDTH - 4),
        }

        # Render each segment
        for segment_name in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            if segment_name in segments_to_light:
                color = COLORS['LED_ON']
            else:
                color = COLORS['LED_DIM']

            points = segment_positions[segment_name]
            self._draw_filled_polygon(renderer, points, color)

    def _horizontal_segment(self, x, y, width):
        """
        Calculate polygon points for horizontal segment.

        Returns:
            List of (x, y) tuples
        """
        return [
            (x + 2, y),
            (x + width - 2, y),
            (x + width, y + 2),
            (x + width - 2, y + 4),
            (x + 2, y + 4),
            (x, y + 2),
        ]

    def _vertical_segment(self, x, y, height):
        """
        Calculate polygon points for vertical segment.

        Returns:
            List of (x, y) tuples
        """
        return [
            (x, y + 2),
            (x + 2, y),
            (x + 4, y),
            (x + 4, y + height - 2),
            (x + 2, y + height),
            (x, y + height - 2),
        ]

    def _draw_filled_polygon(self, renderer, points, color):
        """
        Draw a filled polygon using SDL_gfx.

        Args:
            renderer: SDL renderer
            points: List of (x, y) tuples
            color: RGB tuple
        """
        if len(points) < 3:
            return

        # Extract x and y coordinates
        vx = (c_short * len(points))(*[p[0] for p in points])
        vy = (c_short * len(points))(*[p[1] for p in points])

        # Draw filled polygon
        sdl2.sdlgfx.filledPolygonRGBA(
            renderer,
            vx, vy, len(points),
            color[0], color[1], color[2], 255
        )

    def _render_decimal_point(self, renderer, x, y):
        """
        Render decimal point (small filled circle).

        Args:
            renderer: SDL renderer
            x, y: Center position
        """
        radius = 2
        sdl2.sdlgfx.filledCircleRGBA(
            renderer, x, y, radius,
            COLORS['LED_ON'][0], COLORS['LED_ON'][1], COLORS['LED_ON'][2], 255
        )


# ===== EventHandler Class ===== #

class EventHandler:
    """
    State machine for handling mouse events and button interactions.
    """

    def __init__(self, button_grid):
        self.button_grid = button_grid
        self.hovered_button = None
        self.pressed_button = None
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.state = 'IDLE'

    def handle_event(self, event, button_grid):
        """
        Main event dispatch.

        Args:
            event: SDL event object
            button_grid: ButtonGrid instance

        Returns:
            True to continue running, False to quit
        """
        if event.type == sdl2.SDL_QUIT:
            return False

        elif event.type == sdl2.SDL_MOUSEMOTION:
            self.handle_mouse_motion(event.motion.x, event.motion.y)

        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            if event.button.button == sdl2.SDL_BUTTON_LEFT:
                self.handle_mouse_down(event.button.x, event.button.y)

        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            if event.button.button == sdl2.SDL_BUTTON_LEFT:
                self.handle_mouse_up(event.button.x, event.button.y)

        return True

    def handle_mouse_motion(self, x, y):
        """Handle mouse movement for hover effects."""
        self.last_mouse_x = x
        self.last_mouse_y = y

        button = self.button_grid.get_button_at(x, y)

        if button != self.hovered_button:
            if self.hovered_button is not None:
                self.hovered_button.state = ButtonState.NORMAL

            self.hovered_button = button

            if button is not None:
                button.state = ButtonState.HOVER
                self.state = 'HOVERING'
            else:
                self.state = 'IDLE'

    def handle_mouse_down(self, x, y):
        """Handle mouse button press."""
        button = self.button_grid.get_button_at(x, y)

        if button is not None:
            self.pressed_button = button
            button.state = ButtonState.PRESSED
            self.state = 'PRESSING'

    def handle_mouse_up(self, x, y):
        """Handle mouse button release - executes button action."""
        button = self.button_grid.get_button_at(x, y)

        if button is not None and button == self.pressed_button:
            # Valid button click
            button.state = ButtonState.RELEASED

            # Execute button callback
            if button.callback is not None:
                button.callback()

            # Transition to hover state
            button.state = ButtonState.HOVER
            self.state = 'HOVERING'

        elif self.pressed_button is not None:
            # Released off button - cancel action
            self.pressed_button.state = ButtonState.NORMAL
            self.state = 'IDLE'

        self.pressed_button = None


# ===== HP35Window Class ===== #

class HP35Window:
    """
    Main window class integrating all components.
    """

    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, screenshot_mode=False):
        """
        Initialize SDL window and all components.

        Args:
            width, height: Window dimensions in pixels
            screenshot_mode: If True, create hidden window for screenshots
        """
        # Initialize SDL
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise RuntimeError(f"SDL initialization failed: {sdl2.SDL_GetError()}")

        # Create window (always shown - hiding prevents proper rendering on some platforms)
        self.window = sdl2.SDL_CreateWindow(
            b"CNC - HP-35 Calculator",
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            width, height,
            sdl2.SDL_WINDOW_SHOWN
        )

        if not self.window:
            raise RuntimeError(f"Window creation failed: {sdl2.SDL_GetError()}")

        # Create renderer (use software rendering in screenshot mode for reliable pixel reading)
        if screenshot_mode:
            renderer_flags = sdl2.SDL_RENDERER_SOFTWARE
        else:
            renderer_flags = sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC

        self.renderer = sdl2.SDL_CreateRenderer(
            self.window, -1,
            renderer_flags
        )

        if not self.renderer:
            raise RuntimeError(f"Renderer creation failed: {sdl2.SDL_GetError()}")

        # Initialize calculator engine
        self.calculator = ComplexNumberCalculator(stack_depth=8)

        # Initialize GUI components
        self.button_grid = ButtonGrid()
        self.led_display = LEDDisplay(
            DISPLAY_AREA['x'],
            DISPLAY_AREA['y'],
            DISPLAY_AREA['width'],
            DISPLAY_AREA['height']
        )
        self.event_handler = EventHandler(self.button_grid)

        # Connect button callbacks
        self._setup_button_callbacks()

        # Initial display update
        self.led_display.update(self.calculator.stack)

        # Screenshot mode flag
        self.screenshot_mode = screenshot_mode
        self.screenshot_file = None

    def _setup_button_callbacks(self):
        """Connect each button to calculator command."""
        for button in self.button_grid.buttons:
            # Create closure to capture button's command
            def make_callback(cmd):
                return lambda: self.on_button_press(cmd)

            button.callback = make_callback(button.command)

    def on_button_press(self, command):
        """
        Handle button press by executing calculator command.

        Args:
            command: Calculator command string
        """
        try:
            # Execute command on calculator
            self.calculator.handle_string(command)

            # Update display
            self.led_display.update(self.calculator.stack)

        except ZeroDivisionError:
            self.led_display.display_string = "  ERROR: DIV/0  "
        except OverflowError:
            self.led_display.display_string = "ERROR: OVERFLOW "
        except Exception as e:
            error_msg = str(e)[:15].center(15)
            self.led_display.display_string = error_msg

    def run(self):
        """Main event loop."""
        running = True
        frame_count = 0

        while running:
            # Process all pending events
            event = sdl2.SDL_Event()
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                running = self.event_handler.handle_event(event, self.button_grid)
                if not running:
                    break

            # Render frame
            self.render()

            # Screenshot mode: capture after first frame and exit
            if self.screenshot_mode and frame_count == 0 and self.screenshot_file:
                # Small delay to ensure render completes
                sdl2.SDL_Delay(100)
                try:
                    self.save_screenshot(self.screenshot_file)
                    print(f"Screenshot saved to: {self.screenshot_file}")
                except Exception as e:
                    print(f"Screenshot failed: {e}", file=sys.stderr)
                    import traceback
                    traceback.print_exc()
                running = False

            frame_count += 1

            # Frame rate limiting (60 FPS)
            if not self.screenshot_mode:
                sdl2.SDL_Delay(16)
            elif frame_count > 0:
                # Exit after first frame in screenshot mode
                running = False

    def render(self):
        """Orchestrate rendering of all components."""
        # Clear screen with case color
        sdl2.SDL_SetRenderDrawColor(self.renderer, *COLORS['CASE_BLACK'], 255)
        sdl2.SDL_RenderClear(self.renderer)

        # Render display bezel (raised frame around display)
        self._render_display_bezel()

        # Render LED display
        self.led_display.render(self.renderer)

        # Render buttons
        self.button_grid.render(self.renderer)

        # Present frame
        sdl2.SDL_RenderPresent(self.renderer)

    def _render_display_bezel(self):
        """Render the frame around the LED display."""
        bezel = DISPLAY_BEZEL

        # Outer bezel (dark metallic frame)
        outer_color = (60, 55, 50)
        sdl2.SDL_SetRenderDrawColor(self.renderer, *outer_color, 255)
        outer_rect = sdl2.SDL_Rect(
            bezel['x'], bezel['y'],
            bezel['width'], bezel['height']
        )
        sdl2.SDL_RenderFillRect(self.renderer, outer_rect)

        # Inner frame (subtle metallic highlight)
        inner_color = (90, 85, 80)
        sdl2.SDL_SetRenderDrawColor(self.renderer, *inner_color, 255)
        for i in range(bezel['border_width']):
            frame_rect = sdl2.SDL_Rect(
                bezel['x'] + i,
                bezel['y'] + i,
                bezel['width'] - i * 2,
                bezel['height'] - i * 2
            )
            sdl2.SDL_RenderDrawRect(self.renderer, frame_rect)

    def save_screenshot(self, filename):
        """
        Save a screenshot of the current renderer to a file.

        Note: Requires software renderer for reliable pixel reading.

        Args:
            filename: Output file path (PNG format)
        """
        from PIL import Image
        import numpy as np

        # Get window dimensions
        w, h = c_int(), c_int()
        sdl2.SDL_GetRendererOutputSize(self.renderer, ctypes.byref(w), ctypes.byref(h))
        width, height = w.value, h.value

        # Create buffer for pixels (RGBA format, 4 bytes per pixel)
        pitch = width * 4
        pixels = (ctypes.c_uint8 * (pitch * height))()

        # Read pixels from renderer (use ABGR8888 for correct colors on macOS software renderer)
        result = sdl2.SDL_RenderReadPixels(
            self.renderer,
            None,
            sdl2.SDL_PIXELFORMAT_ABGR8888,
            pixels,
            pitch
        )

        if result != 0:
            raise RuntimeError(f"Could not read pixels: {sdl2.SDL_GetError()}")

        # Convert to numpy array
        arr = np.frombuffer(pixels, dtype=np.uint8).reshape((height, width, 4))

        # Extract RGB channels (drop alpha)
        rgb_arr = arr[:, :, :3]

        # Create PIL image and save
        img = Image.fromarray(rgb_arr, 'RGB')
        img.save(filename, 'PNG')

    def cleanup(self):
        """Clean up SDL resources."""
        if self.renderer:
            sdl2.SDL_DestroyRenderer(self.renderer)
        if self.window:
            sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()


# ===== Main Entry Point ===== #

def main():
    """
    Main entry point for the HP-35 GUI calculator.
    """
    import argparse

    parser = argparse.ArgumentParser(description="HP-35 GUI Calculator")
    parser.add_argument('--screenshot', metavar='FILE',
                       help='Take a screenshot and save to FILE (PNG format), then exit')
    args = parser.parse_args()

    window = None
    try:
        # Create window with appropriate mode
        if args.screenshot:
            window = HP35Window(screenshot_mode=True)
            window.screenshot_file = args.screenshot
        else:
            window = HP35Window(screenshot_mode=False)

        # Run event loop (will exit after one frame in screenshot mode)
        window.run()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

    finally:
        # Cleanup
        if window:
            window.cleanup()

    return 0


if __name__ == "__main__":
    sys.exit(main())
