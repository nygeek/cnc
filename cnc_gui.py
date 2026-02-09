#!/usr/bin/env python3

"""
HP-35 GUI Calculator Implementation using PySDL2

This module implements a faithful pixel-perfect GUI replica of the 1972 HP-35
calculator with extended functionality for quaternions and octonions.

SPDX-License-Identifier: MIT
Copyright (C) 2026 NYGeek LLC

Requirements:
    - Python 3.5+
    - PySDL2
    - SDL2 libraries (libSDL2, libSDL2_gfx, libSDL2_ttf)

Usage:
    python3 cnc_gui.py
"""

import sys
import math
import ctypes
from ctypes import c_int, c_uint8, POINTER

try:
    import sdl2
    import sdl2.ext
    import sdl2.sdlgfx
except ImportError:
    print("Error: PySDL2 not found. Install with: pip install pysdl2")
    sys.exit(1)

from cnc import ComplexNumberCalculator
from quaternion import Quaternion
from octonion import Octonion


# ===== Constants ===== #

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 1080

# Color palette - exact RGB values from design.md Section 5.1
COLORS = {
    # Case and background
    'CASE_BLACK':       (20, 20, 20),
    'DISPLAY_BG':       (10, 10, 10),

    # LED colors
    'LED_ON':           (255, 0, 0),
    'LED_DIM':          (32, 0, 0),
    'LED_GLOW':         (255, 80, 80),

    # Button colors - Original HP-35
    'TAN':              (210, 180, 140),
    'BLUE':             (50, 100, 200),
    'BLACK_KEY':        (30, 30, 30),

    # Button colors - Extended
    'PURPLE':           (150, 50, 200),
    'ORANGE':           (255, 140, 0),

    # Text colors
    'WHITE_TEXT':       (255, 255, 255),
    'BLACK_TEXT':       (0, 0, 0),

    # Button states
    'BUTTON_HOVER':     (200, 200, 200),
    'BUTTON_PRESSED':   (100, 100, 100),
}

# Display dimensions from design.md Section 3.1
DISPLAY_AREA = {
    'x': 20,
    'y': 20,
    'width': 560,
    'height': 160,
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

    # Row 8 - Quaternion
    'j':      'j',
    'k':      'k',
    'e0':     'e0',
    'e1':     'e1',
    'e2':     'e2',

    # Row 9 - Octonion
    'e3':     'e3',
    'e4':     'e4',
    'e5':     'e5',
    'e6':     'e6',
    'e7':     'e7',

    # Row 10
    'conj':   'conj',
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
    Format number for LED display (handles complex, quaternion, octonion).

    Args:
        value: Number to format

    Returns:
        String formatted for LED display (up to 15 characters)
    """
    if isinstance(value, Octonion):
        # Show first component with 'o' suffix
        return format_scientific(value.components[0])[:13] + " o"
    elif isinstance(value, Quaternion):
        # Show w component with 'q' suffix
        return format_scientific(value.w)[:13] + " q"
    elif isinstance(value, complex):
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
        # Row 0 (Y=220)
        self.buttons.extend([
            Button(40,  220, 90, 70, 'sqrt',   'sqrt',   COLORS['BLACK_KEY']),
            Button(140, 220, 90, 70, 'arcsin', 'asin',   COLORS['BLACK_KEY']),
            Button(240, 220, 90, 70, 'arccos', 'acos',   COLORS['BLACK_KEY']),
            Button(340, 220, 90, 70, 'arctan', 'atan',   COLORS['BLACK_KEY']),
            Button(440, 220, 90, 70, '1/x',    'inv',    COLORS['BLACK_KEY']),
        ])

        # Row 1 (Y=300)
        self.buttons.extend([
            Button(40,  300, 90, 70, 'x^y',    'xtoy',   COLORS['BLACK_KEY']),
            Button(140, 300, 90, 70, 'ln',     'ln',     COLORS['BLACK_KEY']),
            Button(240, 300, 90, 70, 'log',    'log',    COLORS['BLACK_KEY']),
            Button(340, 300, 90, 70, 'e^x',    'exp',    COLORS['BLACK_KEY']),
            Button(440, 300, 90, 70, 'CLR',    'clr',    COLORS['BLUE']),
        ])

        # Row 2 (Y=380)
        self.buttons.extend([
            Button(40,  380, 90, 70, 'STO',    'sto',    COLORS['BLACK_KEY']),
            Button(140, 380, 90, 70, 'RCL',    'rcl',    COLORS['BLACK_KEY']),
            Button(240, 380, 90, 70, 'R↓',     'down',   COLORS['BLACK_KEY']),
            Button(340, 380, 90, 70, 'x↔y',    'exch',   COLORS['BLACK_KEY']),
            Button(440, 380, 90, 70, 'CLx',    'clx',    COLORS['BLUE']),
        ])

        # Row 3 (Y=460) - Note: ENTER is wide (190 pixels)
        self.buttons.extend([
            Button(40,  460, 190, 70, 'ENTER', 'enter',  COLORS['BLUE']),
            Button(240, 460, 90,  70, 'CHS',   'chs',    COLORS['BLACK_KEY']),
            Button(340, 460, 90,  70, 'EEX',   'eex',    COLORS['BLACK_KEY']),
            Button(440, 460, 90,  70, 'CLR',   'clr',    COLORS['BLUE']),
        ])

        # Row 4 (Y=540)
        self.buttons.extend([
            Button(40,  540, 90, 70, 'sin',    'sin',    COLORS['BLACK_KEY']),
            Button(140, 540, 90, 70, '7',      '7',      COLORS['TAN']),
            Button(240, 540, 90, 70, '8',      '8',      COLORS['TAN']),
            Button(340, 540, 90, 70, '9',      '9',      COLORS['TAN']),
            Button(440, 540, 90, 70, '÷',      '/',      COLORS['BLUE']),
        ])

        # Row 5 (Y=620)
        self.buttons.extend([
            Button(40,  620, 90, 70, 'cos',    'cos',    COLORS['BLACK_KEY']),
            Button(140, 620, 90, 70, '4',      '4',      COLORS['TAN']),
            Button(240, 620, 90, 70, '5',      '5',      COLORS['TAN']),
            Button(340, 620, 90, 70, '6',      '6',      COLORS['TAN']),
            Button(440, 620, 90, 70, '×',      '*',      COLORS['BLUE']),
        ])

        # Row 6 (Y=700)
        self.buttons.extend([
            Button(40,  700, 90, 70, 'tan',    'tan',    COLORS['BLACK_KEY']),
            Button(140, 700, 90, 70, '1',      '1',      COLORS['TAN']),
            Button(240, 700, 90, 70, '2',      '2',      COLORS['TAN']),
            Button(340, 700, 90, 70, '3',      '3',      COLORS['TAN']),
            Button(440, 700, 90, 70, '−',      '-',      COLORS['BLUE']),
        ])

        # Row 7 (Y=780)
        self.buttons.extend([
            Button(40,  780, 90, 70, 'π',      'pi',     COLORS['TAN']),
            Button(140, 780, 90, 70, '0',      '0',      COLORS['TAN']),
            Button(240, 780, 90, 70, '•',      '.',      COLORS['TAN']),
            Button(340, 780, 90, 70, 'Σ+',     '+',      COLORS['BLACK_KEY']),
            Button(440, 780, 90, 70, '+',      '+',      COLORS['BLUE']),
        ])

        # Row 8 (Y=870) - Extended quaternion/octonion buttons
        self.buttons.extend([
            Button(40,  870, 90, 70, 'j',      'j',      COLORS['PURPLE']),
            Button(140, 870, 90, 70, 'k',      'k',      COLORS['PURPLE']),
            Button(240, 870, 90, 70, 'e0',     'e0',     COLORS['ORANGE']),
            Button(340, 870, 90, 70, 'e1',     'e1',     COLORS['ORANGE']),
            Button(440, 870, 90, 70, 'e2',     'e2',     COLORS['ORANGE']),
        ])

        # Row 9 (Y=950)
        self.buttons.extend([
            Button(40,  950, 90, 70, 'e3',     'e3',     COLORS['ORANGE']),
            Button(140, 950, 90, 70, 'e4',     'e4',     COLORS['ORANGE']),
            Button(240, 950, 90, 70, 'e5',     'e5',     COLORS['ORANGE']),
            Button(340, 950, 90, 70, 'e6',     'e6',     COLORS['ORANGE']),
            Button(440, 950, 90, 70, 'e7',     'e7',     COLORS['ORANGE']),
        ])

        # Row 10 (Y=1030) - Conjugate button
        self.buttons.extend([
            Button(240, 1030, 90, 70, 'conj',  'conj',   COLORS['PURPLE']),
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

            # Draw button rectangle
            sdl2.SDL_SetRenderDrawColor(renderer, *color, 255)
            rect = sdl2.SDL_Rect(button.x, button.y, button.width, button.height)
            sdl2.SDL_RenderFillRect(renderer, rect)

            # Draw button border (darker)
            border_color = tuple(max(0, c - 40) for c in color)
            sdl2.SDL_SetRenderDrawColor(renderer, *border_color, 255)
            sdl2.SDL_RenderDrawRect(renderer, rect)

            # Draw text label (centered)
            self._render_button_label(renderer, button)

    def _render_button_label(self, renderer, button):
        """
        Render text label centered on button.

        Args:
            renderer: SDL renderer
            button: Button object
        """
        # For now, use simple text rendering
        # In a full implementation, would use SDL_ttf for better text
        pass


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
        x_display_x = self.x + 100
        x_display_y = self.y + 120
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
        vx = (c_int * len(points))(*[p[0] for p in points])
        vy = (c_int * len(points))(*[p[1] for p in points])

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

    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        """
        Initialize SDL window and all components.

        Args:
            width, height: Window dimensions in pixels
        """
        # Initialize SDL
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            raise RuntimeError(f"SDL initialization failed: {sdl2.SDL_GetError()}")

        # Create window
        self.window = sdl2.SDL_CreateWindow(
            b"CNC - HP-35 Calculator",
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            width, height,
            sdl2.SDL_WINDOW_SHOWN
        )

        if not self.window:
            raise RuntimeError(f"Window creation failed: {sdl2.SDL_GetError()}")

        # Create renderer
        self.renderer = sdl2.SDL_CreateRenderer(
            self.window, -1,
            sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
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

        while running:
            # Process all pending events
            event = sdl2.SDL_Event()
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                running = self.event_handler.handle_event(event, self.button_grid)
                if not running:
                    break

            # Render frame
            self.render()

            # Frame rate limiting (60 FPS)
            sdl2.SDL_Delay(16)

    def render(self):
        """Orchestrate rendering of all components."""
        # Clear screen with case color
        sdl2.SDL_SetRenderDrawColor(self.renderer, *COLORS['CASE_BLACK'], 255)
        sdl2.SDL_RenderClear(self.renderer)

        # Render LED display
        self.led_display.render(self.renderer)

        # Render buttons
        self.button_grid.render(self.renderer)

        # Present frame
        sdl2.SDL_RenderPresent(self.renderer)

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
    window = None
    try:
        # Create and run window
        window = HP35Window()
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
