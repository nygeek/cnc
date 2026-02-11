# HP-35 GUI Calculator - Detailed Design Document

*SPDX-License-Identifier: MIT*
*Copyright (C) 2026 NYGeek LLC*

## Document Overview

This design document provides implementation-ready specifications for the HP-35 GUI calculator. All coordinates, dimensions, colors, and algorithms are specified with exact values to enable direct implementation without ambiguity.

---

## 1. Button Layout and Coordinates

### 1.1 Window Dimensions

```python
WINDOW_WIDTH = 600   # pixels
WINDOW_HEIGHT = 1080 # pixels
ASPECT_RATIO = 1.8   # width:height (approximates HP-35 5.8":3.2")
```

### 1.2 Layout Regions

```python
DISPLAY_REGION = {
    'x': 0,
    'y': 0,
    'width': 600,
    'height': 200
}

BUTTON_REGION = {
    'x': 0,
    'y': 200,
    'width': 600,
    'height': 880
}
```

### 1.3 Button Grid Specifications

**Grid Parameters:**
```python
BUTTON_SPACING_X = 10    # pixels between buttons horizontally
BUTTON_SPACING_Y = 10    # pixels between buttons vertically
GRID_MARGIN_LEFT = 40    # left margin
GRID_MARGIN_RIGHT = 40   # right margin
GRID_MARGIN_TOP = 20     # top margin (relative to button region)
GRID_MARGIN_BOTTOM = 20  # bottom margin

# Usable grid area
GRID_WIDTH = WINDOW_WIDTH - GRID_MARGIN_LEFT - GRID_MARGIN_RIGHT  # 520 pixels
GRID_HEIGHT = BUTTON_REGION['height'] - GRID_MARGIN_TOP - GRID_MARGIN_BOTTOM  # 840 pixels
```

**Button Dimensions:**
```python
# Standard button
STANDARD_BUTTON_WIDTH = 90   # pixels
STANDARD_BUTTON_HEIGHT = 70  # pixels

# ENTER button (wider)
ENTER_BUTTON_WIDTH = 190     # pixels (2 × standard + spacing)
ENTER_BUTTON_HEIGHT = 70     # pixels

# Digit button (larger for easier clicking)
DIGIT_BUTTON_WIDTH = 90      # pixels
DIGIT_BUTTON_HEIGHT = 70     # pixels
```

### 1.4 HP-35 Original Button Layout (47 buttons total)

**Row 0 (Top Row - Scientific Functions):**
```python
ROW_0_Y = BUTTON_REGION['y'] + GRID_MARGIN_TOP  # Y = 220

buttons_row_0 = [
    {'label': 'sqrt',  'x': 40,  'y': 220, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'arcsin','x': 140, 'y': 220, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'arccos','x': 240, 'y': 220, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'arctan','x': 340, 'y': 220, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': '1/x',   'x': 440, 'y': 220, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
]
```

**Row 1 (Scientific Functions):**
```python
ROW_1_Y = 300  # pixels

buttons_row_1 = [
    {'label': 'x^y',   'x': 40,  'y': 300, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'ln',    'x': 140, 'y': 300, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'log',   'x': 240, 'y': 300, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'e^x',   'x': 340, 'y': 300, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'CLR',   'x': 440, 'y': 300, 'width': 90, 'height': 70, 'color': 'BLUE'},
]
```

**Row 2 (Stack Operations):**
```python
ROW_2_Y = 380  # pixels

buttons_row_2 = [
    {'label': 'STO',   'x': 40,  'y': 380, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'RCL',   'x': 140, 'y': 380, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'R↓',    'x': 240, 'y': 380, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'x↔y',   'x': 340, 'y': 380, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'CLx',   'x': 440, 'y': 380, 'width': 90, 'height': 70, 'color': 'BLUE'},
]
```

**Row 3 (ENTER and Special Functions):**
```python
ROW_3_Y = 460  # pixels

buttons_row_3 = [
    {'label': 'ENTER', 'x': 40,  'y': 460, 'width': 190, 'height': 70, 'color': 'BLUE'},  # WIDE!
    {'label': 'CHS',   'x': 240, 'y': 460, 'width': 90,  'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'EEX',   'x': 340, 'y': 460, 'width': 90,  'height': 70, 'color': 'BLACK_KEY'},
    {'label': 'CLR',   'x': 440, 'y': 460, 'width': 90,  'height': 70, 'color': 'BLUE'},
]
```

**Row 4 (Digits and Division):**
```python
ROW_4_Y = 540  # pixels

buttons_row_4 = [
    {'label': 'sin',   'x': 40,  'y': 540, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': '7',     'x': 140, 'y': 540, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '8',     'x': 240, 'y': 540, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '9',     'x': 340, 'y': 540, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '÷',     'x': 440, 'y': 540, 'width': 90, 'height': 70, 'color': 'BLUE'},
]
```

**Row 5 (Digits and Multiplication):**
```python
ROW_5_Y = 620  # pixels

buttons_row_5 = [
    {'label': 'cos',   'x': 40,  'y': 620, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': '4',     'x': 140, 'y': 620, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '5',     'x': 240, 'y': 620, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '6',     'x': 340, 'y': 620, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '×',     'x': 440, 'y': 620, 'width': 90, 'height': 70, 'color': 'BLUE'},
]
```

**Row 6 (Digits and Subtraction):**
```python
ROW_6_Y = 700  # pixels

buttons_row_6 = [
    {'label': 'tan',   'x': 40,  'y': 700, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': '1',     'x': 140, 'y': 700, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '2',     'x': 240, 'y': 700, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '3',     'x': 340, 'y': 700, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '−',     'x': 440, 'y': 700, 'width': 90, 'height': 70, 'color': 'BLUE'},
]
```

**Row 7 (Bottom Row - Digits and Addition):**
```python
ROW_7_Y = 780  # pixels

buttons_row_7 = [
    {'label': 'π',     'x': 40,  'y': 780, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '0',     'x': 140, 'y': 780, 'width': 90, 'height': 70, 'color': 'TAN'},
    {'label': '•',     'x': 240, 'y': 780, 'width': 90, 'height': 70, 'color': 'TAN'},  # decimal
    {'label': 'Σ+',    'x': 340, 'y': 780, 'width': 90, 'height': 70, 'color': 'BLACK_KEY'},
    {'label': '+',     'x': 440, 'y': 780, 'width': 90, 'height': 70, 'color': 'BLUE'},
]
```

### 1.5 Extended Buttons Layout (Quaternion/Octonion)

**Row 8 (Extended - Quaternion and Small Octonion):**
```python
ROW_8_Y = 870  # pixels

buttons_row_8 = [
    {'label': 'j',     'x': 40,  'y': 870, 'width': 90, 'height': 70, 'color': 'PURPLE'},
    {'label': 'k',     'x': 140, 'y': 870, 'width': 90, 'height': 70, 'color': 'PURPLE'},
    {'label': 'e0',    'x': 240, 'y': 870, 'width': 90, 'height': 70, 'color': 'ORANGE'},
    {'label': 'e1',    'x': 340, 'y': 870, 'width': 90, 'height': 70, 'color': 'ORANGE'},
    {'label': 'e2',    'x': 440, 'y': 870, 'width': 90, 'height': 70, 'color': 'ORANGE'},
]
```

**Row 9 (Extended - Octonion Basis and Conjugate):**
```python
ROW_9_Y = 950  # pixels

buttons_row_9 = [
    {'label': 'e3',    'x': 40,  'y': 950, 'width': 90, 'height': 70, 'color': 'ORANGE'},
    {'label': 'e4',    'x': 140, 'y': 950, 'width': 90, 'height': 70, 'color': 'ORANGE'},
    {'label': 'e5',    'x': 240, 'y': 950, 'width': 90, 'height': 70, 'color': 'ORANGE'},
    {'label': 'e6',    'x': 340, 'y': 950, 'width': 90, 'height': 70, 'color': 'ORANGE'},
    {'label': 'e7',    'x': 440, 'y': 950, 'width': 90, 'height': 70, 'color': 'ORANGE'},
]
```

**Row 10 (Extended - Conjugate):**
```python
ROW_10_Y = 1030  # pixels

buttons_row_10 = [
    {'label': 'conj',  'x': 240, 'y': 1030, 'width': 90, 'height': 70, 'color': 'PURPLE'},
]
```

### 1.6 Button Name to Calculator Command Mapping

```python
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
    'Σ+':     '+',  # Note: using + for addition
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
```

---

## 2. Seven-Segment LED Rendering Algorithm

### 2.1 Segment Definitions

Each digit is composed of 7 segments labeled A-G:

```
     AAA
    F   B
    F   B
     GGG
    E   C
    E   C
     DDD
```

**Segment Coordinate Offsets (relative to digit origin):**

```python
# For a digit with top-left at (x, y)
DIGIT_WIDTH = 20     # pixels
DIGIT_HEIGHT = 32    # pixels
SEGMENT_WIDTH = 3    # thickness of segment
SEGMENT_GAP = 1      # gap between segments

# Horizontal segment (A, G, D) as polygon points (clockwise from top-left)
def horizontal_segment(x, y, width):
    """Returns polygon points for horizontal segment"""
    return [
        (x + 2, y),                    # top-left
        (x + width - 2, y),            # top-right
        (x + width, y + 2),            # right tip
        (x + width - 2, y + 4),        # bottom-right
        (x + 2, y + 4),                # bottom-left
        (x, y + 2),                    # left tip
    ]

# Vertical segment (F, B, E, C) as polygon points
def vertical_segment(x, y, height):
    """Returns polygon points for vertical segment"""
    return [
        (x, y + 2),                    # top tip
        (x + 2, y),                    # top-left
        (x + 4, y),                    # top-right
        (x + 4, y + height - 2),       # bottom-right
        (x + 2, y + height),           # bottom tip
        (x, y + height - 2),           # bottom-left
    ]

# Segment positions relative to digit origin (x, y)
SEGMENT_POSITIONS = {
    'A': lambda x, y: horizontal_segment(x + 2, y, DIGIT_WIDTH - 4),
    'B': lambda x, y: vertical_segment(x + DIGIT_WIDTH - 4, y + 2, DIGIT_HEIGHT // 2 - 3),
    'C': lambda x, y: vertical_segment(x + DIGIT_WIDTH - 4, y + DIGIT_HEIGHT // 2 + 1, DIGIT_HEIGHT // 2 - 3),
    'D': lambda x, y: horizontal_segment(x + 2, y + DIGIT_HEIGHT - 4, DIGIT_WIDTH - 4),
    'E': lambda x, y: vertical_segment(x, y + DIGIT_HEIGHT // 2 + 1, DIGIT_HEIGHT // 2 - 3),
    'F': lambda x, y: vertical_segment(x, y + 2, DIGIT_HEIGHT // 2 - 3),
    'G': lambda x, y: horizontal_segment(x + 2, y + DIGIT_HEIGHT // 2 - 2, DIGIT_WIDTH - 4),
}
```

### 2.2 Character to Segment Mapping

```python
SEGMENT_MAP = {
    '0': ['A', 'B', 'C', 'D', 'E', 'F'],       # All except G
    '1': ['B', 'C'],                            # Right vertical
    '2': ['A', 'B', 'G', 'E', 'D'],            # Classic "2"
    '3': ['A', 'B', 'G', 'C', 'D'],            # Classic "3"
    '4': ['F', 'G', 'B', 'C'],                 # Classic "4"
    '5': ['A', 'F', 'G', 'C', 'D'],            # Classic "5"
    '6': ['A', 'F', 'G', 'E', 'D', 'C'],       # Classic "6"
    '7': ['A', 'B', 'C'],                       # Classic "7"
    '8': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],  # All segments
    '9': ['A', 'B', 'C', 'D', 'F', 'G'],       # Classic "9"

    # Hexadecimal (for future use)
    'A': ['A', 'B', 'C', 'E', 'F', 'G'],
    'B': ['C', 'D', 'E', 'F', 'G'],            # lowercase b
    'C': ['A', 'D', 'E', 'F'],
    'D': ['B', 'C', 'D', 'E', 'G'],            # lowercase d
    'E': ['A', 'D', 'E', 'F', 'G'],
    'F': ['A', 'E', 'F', 'G'],

    # Special characters
    '-': ['G'],                                 # Minus/negative
    ' ': [],                                    # Space (blank)
    '.': [],                                    # Decimal point (handled separately)
}
```

### 2.3 Rendering Algorithm Pseudocode

```python
def render_seven_segment_digit(surface, x, y, char, is_active=True):
    """
    Render a single seven-segment digit

    Args:
        surface: SDL surface to draw on
        x, y: Top-left position of digit
        char: Character to render ('0'-'9', 'A'-'F', '-', ' ')
        is_active: If True, render bright red; if False, render dim

    Returns:
        None (renders to surface)
    """
    # Choose color based on active state
    if is_active:
        segment_color = LED_ON   # Bright red (255, 0, 0)
    else:
        segment_color = LED_OFF  # Very dim red (32, 0, 0)

    # Get segments for this character
    if char in SEGMENT_MAP:
        segments_to_light = SEGMENT_MAP[char]
    else:
        segments_to_light = []  # Unknown character = blank

    # Render each segment
    for segment_name in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        # Get polygon points for this segment
        polygon_points = SEGMENT_POSITIONS[segment_name](x, y)

        # Determine segment color
        if segment_name in segments_to_light:
            color = segment_color  # Active segment
        else:
            color = LED_DIM        # Inactive segment (very dim)

        # Draw filled polygon
        SDL_DrawFilledPolygon(surface, polygon_points, color)


def render_decimal_point(surface, x, y, is_active=True):
    """
    Render decimal point (small filled circle)

    Args:
        surface: SDL surface
        x, y: Center position of decimal point
        is_active: Whether to light the decimal point
    """
    radius = 2  # pixels
    color = LED_ON if is_active else LED_DIM
    SDL_DrawFilledCircle(surface, x, y, radius, color)


def render_led_display_string(surface, x, y, text, max_digits=15):
    """
    Render complete LED display string

    Args:
        surface: SDL surface
        x, y: Top-left position of display
        text: String to display (e.g., "1234567890.12")
        max_digits: Maximum number of digit positions

    Algorithm:
        1. Parse text into mantissa, decimal, exponent
        2. Position each digit in its appropriate position
        3. Render each digit with seven-segment algorithm
        4. Render decimal point if present
    """
    digit_spacing = DIGIT_WIDTH + 4  # pixels between digit centers
    current_x = x

    # Display format: " -1.234567890 E-12"
    # Positions:       [0][1][2][3]...[14]

    for i in range(max_digits):
        if i < len(text):
            char = text[i]
            if char == '.':
                # Render decimal point (offset from previous digit)
                render_decimal_point(surface, current_x - 2, y + DIGIT_HEIGHT - 4, True)
                continue  # Don't advance position
            else:
                render_seven_segment_digit(surface, current_x, y, char, is_active=True)
        else:
            # Blank position (show dim segments)
            render_seven_segment_digit(surface, current_x, y, ' ', is_active=False)

        current_x += digit_spacing
```

---

## 3. Display Layout

### 3.1 Display Region Structure

```python
DISPLAY_AREA = {
    'x': 20,
    'y': 20,
    'width': 560,
    'height': 160,
    'background_color': (10, 10, 10),  # Very dark background
}

# X register (main display)
X_REGISTER_DISPLAY = {
    'x': 40,
    'y': 120,
    'digit_count': 15,
    'digit_width': 20,
    'digit_height': 32,
    'digit_spacing': 24,
}

# Stack register labels
STACK_LABELS = {
    'T': {'x': 40, 'y': 30},
    'Z': {'x': 40, 'y': 50},
    'Y': {'x': 40, 'y': 70},
    'X': {'x': 40, 'y': 90},
    'M': {'x': 40, 'y': 110},  # Memory register
}
```

### 3.2 Display Format

**Number Display Format:**

```
Position:   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
Example 1:  -  1  .  2  3  4  5  6  7  8  9  0  E  -  12
Example 2:     3  .  1  4  1  5  9  2  6  5  4  E  +  00
```

**Format Components:**
- Position 0: Sign (- or space)
- Position 1: First mantissa digit
- Position 2: Decimal point
- Positions 3-11: Mantissa digits (9 more digits)
- Position 12: Exponent indicator ('E')
- Position 13: Exponent sign (+ or -)
- Position 14-15: Exponent value (2 digits)

### 3.3 Stack Display Layout

```python
def render_stack_display(surface, stack):
    """
    Render entire stack in display area

    Args:
        surface: SDL surface
        stack: HP35Stack object
    """
    # Display dimensions
    stack_display_x = 100
    stack_display_y = 30
    line_height = 20

    # Render each stack register
    registers = ['M', 'T', 'Z', 'Y', 'X']
    y_positions = [30, 50, 70, 90, 120]  # Y position for each register

    for i, reg_name in enumerate(registers):
        # Get value from stack
        if reg_name == 'M':
            value = stack.storcl
        else:
            index = {'X': 0, 'Y': 1, 'Z': 2, 'T': 3}[reg_name]
            value = stack.stack[index]

        # Format value as string
        formatted = format_number_for_display(value)

        # Render label
        render_text(surface, reg_name + ':', 40, y_positions[i], LABEL_FONT, LED_DIM)

        # Render value (only X register gets full LED treatment)
        if reg_name == 'X':
            render_led_display_string(surface, stack_display_x, y_positions[i], formatted, 15)
        else:
            # Smaller text for other registers
            render_text(surface, formatted, stack_display_x, y_positions[i], SMALL_FONT, LED_ON)


def format_number_for_display(value):
    """
    Format complex/quaternion/octonion number for display

    Args:
        value: Number to format (complex, Quaternion, or Octonion)

    Returns:
        String formatted for LED display
    """
    # Handle different types
    if isinstance(value, complex):
        if value.imag == 0:
            # Real number
            return format_scientific(value.real)
        else:
            # Complex number - show real part primarily
            return format_scientific(value.real) + "i"
    elif isinstance(value, Quaternion):
        # Show first component
        return format_scientific(value.w) + "q"
    elif isinstance(value, Octonion):
        # Show first component
        return format_scientific(value.components[0]) + "o"
    else:
        return format_scientific(float(value))


def format_scientific(num, precision=10):
    """
    Format number in scientific notation for display

    Args:
        num: Number to format
        precision: Number of significant digits

    Returns:
        String like "-1.2345678E-12"
    """
    if num == 0:
        return " 0.000000000 E+00"

    # Calculate exponent
    import math
    exponent = math.floor(math.log10(abs(num)))
    mantissa = num / (10 ** exponent)

    # Format string
    sign = '-' if num < 0 else ' '
    exp_sign = '+' if exponent >= 0 else '-'

    # Build display string
    mantissa_str = f"{abs(mantissa):.9f}"  # 1 digit + decimal + 9 digits
    exp_str = f"{abs(exponent):02d}"

    return f"{sign}{mantissa_str} E{exp_sign}{exp_str}"
```

---

## 4. Event Handling State Machine

### 4.1 Mouse Event Types

```python
SDL_EVENTS = {
    'MOUSEBUTTONDOWN': 1025,  # SDL constant
    'MOUSEBUTTONUP':   1026,  # SDL constant
    'MOUSEMOTION':     1024,  # SDL constant
    'QUIT':            256,   # SDL constant
}

MOUSE_BUTTONS = {
    'LEFT':   1,  # SDL_BUTTON_LEFT
    'MIDDLE': 2,  # SDL_BUTTON_MIDDLE
    'RIGHT':  3,  # SDL_BUTTON_RIGHT
}
```

### 4.2 Button States

```python
class ButtonState:
    """Enumeration of button states"""
    NORMAL = 0     # Default state, not interacting
    HOVER = 1      # Mouse hovering over button
    PRESSED = 2    # Button currently pressed down
    RELEASED = 3   # Button just released (triggers action)
```

### 4.3 Event Handler State Machine

```python
class EventHandler:
    """
    State machine for handling mouse events and button interactions
    """

    def __init__(self, button_grid):
        self.button_grid = button_grid
        self.hovered_button = None     # Button currently under mouse
        self.pressed_button = None     # Button currently pressed
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.state = 'IDLE'            # State: IDLE, HOVERING, PRESSING


    def handle_event(self, event):
        """
        Main event dispatch

        Args:
            event: SDL event object

        Returns:
            True to continue running, False to quit
        """
        if event.type == SDL_QUIT:
            return False  # Signal to quit

        elif event.type == SDL_MOUSEMOTION:
            self.handle_mouse_motion(event.x, event.y)

        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == MOUSE_BUTTONS['LEFT']:
                self.handle_mouse_down(event.x, event.y)

        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == MOUSE_BUTTONS['LEFT']:
                self.handle_mouse_up(event.x, event.y)

        return True  # Continue running


    def handle_mouse_motion(self, x, y):
        """
        Handle mouse movement (for hover effects)

        State transitions:
        - IDLE -> HOVERING (when mouse enters button)
        - HOVERING -> IDLE (when mouse leaves button)
        - HOVERING -> HOVERING (when mouse moves between buttons)
        """
        self.last_mouse_x = x
        self.last_mouse_y = y

        # Find button at current position
        button = self.button_grid.get_button_at(x, y)

        # Update hover state
        if button != self.hovered_button:
            # Mouse moved to different button (or none)
            if self.hovered_button is not None:
                self.hovered_button.state = ButtonState.NORMAL

            self.hovered_button = button

            if button is not None:
                button.state = ButtonState.HOVER
                self.state = 'HOVERING'
            else:
                self.state = 'IDLE'


    def handle_mouse_down(self, x, y):
        """
        Handle mouse button press

        State transitions:
        - HOVERING -> PRESSING (when mouse clicks on button)
        - IDLE -> IDLE (click on empty space does nothing)
        """
        button = self.button_grid.get_button_at(x, y)

        if button is not None:
            self.pressed_button = button
            button.state = ButtonState.PRESSED
            self.state = 'PRESSING'

            # Optional: Trigger press animation
            self.button_grid.animate_press(button, start=True)


    def handle_mouse_up(self, x, y):
        """
        Handle mouse button release

        State transitions:
        - PRESSING -> HOVERING (if released on same button)
        - PRESSING -> IDLE (if released off button)

        This is where button actions are executed!
        """
        button = self.button_grid.get_button_at(x, y)

        # Check if we released on the same button we pressed
        if button is not None and button == self.pressed_button:
            # Valid button click!
            button.state = ButtonState.RELEASED

            # Execute button callback
            if button.callback is not None:
                button.callback()

            # Transition to hover state
            button.state = ButtonState.HOVER
            self.state = 'HOVERING'

            # Optional: Trigger release animation
            self.button_grid.animate_press(button, start=False)

        elif self.pressed_button is not None:
            # Released off the button - cancel action
            self.pressed_button.state = ButtonState.NORMAL
            self.state = 'IDLE'

        # Clear pressed button
        self.pressed_button = None
```

### 4.4 Event Loop Integration

```python
def main_event_loop(window):
    """
    Main SDL event loop
    """
    running = True
    clock = SDL_CreateClock()  # For frame timing

    while running:
        # Process all pending events
        for event in SDL_PollEvents():
            running = window.event_handler.handle_event(event)
            if not running:
                break

        # Update game state (if needed)
        # ... none for calculator

        # Render frame
        window.render()

        # Maintain frame rate (60 FPS)
        SDL_Delay(16)  # ~60 FPS (1000ms / 60 = 16.67ms)

    # Cleanup
    window.cleanup()
```

---

## 5. Color Specifications

### 5.1 Exact RGB Values

```python
COLORS = {
    # Case and background
    'CASE_BLACK':       (20, 20, 20),      # Very dark gray (case body)
    'DISPLAY_BG':       (10, 10, 10),      # Almost black (LED background)

    # LED colors
    'LED_ON':           (255, 0, 0),       # Bright red (active LED)
    'LED_DIM':          (32, 0, 0),        # Very dim red (inactive segments)
    'LED_GLOW':         (255, 80, 80),     # Lighter red (glow effect)

    # Button colors - Original HP-35
    'TAN':              (210, 180, 140),   # Tan/beige for digit keys
    'BLUE':             (50, 100, 200),    # Blue for function keys
    'BLACK_KEY':        (30, 30, 30),      # Black for scientific keys

    # Button colors - Extended
    'PURPLE':           (150, 50, 200),    # Purple for quaternion buttons
    'ORANGE':           (255, 140, 0),     # Orange for octonion buttons

    # Text colors
    'WHITE_TEXT':       (255, 255, 255),   # White text on dark buttons
    'BLACK_TEXT':       (0, 0, 0),         # Black text on tan/light buttons

    # Button states
    'BUTTON_HOVER':     (200, 200, 200),   # Light gray highlight
    'BUTTON_PRESSED':   (100, 100, 100),   # Darker gray when pressed
}
```

### 5.2 Button Color by Type

```python
def get_button_color(button_label):
    """
    Return appropriate color for button based on label

    Args:
        button_label: String label of button

    Returns:
        RGB tuple
    """
    # Digit keys (0-9, decimal, π)
    if button_label in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '•', 'π']:
        return COLORS['TAN']

    # Arithmetic operators
    elif button_label in ['+', '-', '×', '÷', 'Σ+']:
        return COLORS['BLUE']

    # Control keys
    elif button_label in ['ENTER', 'CLR', 'CLx']:
        return COLORS['BLUE']

    # Scientific functions
    elif button_label in ['sin', 'cos', 'tan', 'sqrt', 'arcsin', 'arccos', 'arctan',
                           'ln', 'log', 'e^x', 'x^y', '1/x', 'STO', 'RCL', 'R↓',
                           'x↔y', 'CHS', 'EEX']:
        return COLORS['BLACK_KEY']

    # Quaternion buttons
    elif button_label in ['j', 'k', 'conj']:
        return COLORS['PURPLE']

    # Octonion buttons
    elif button_label in ['e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7']:
        return COLORS['ORANGE']

    # Default
    else:
        return COLORS['BLACK_KEY']


def get_text_color(button_color):
    """
    Return appropriate text color for given button color

    Args:
        button_color: RGB tuple of button background

    Returns:
        RGB tuple for text color
    """
    # Calculate brightness
    brightness = (button_color[0] + button_color[1] + button_color[2]) / 3

    # Light buttons get black text
    if brightness > 128:
        return COLORS['BLACK_TEXT']
    else:
        return COLORS['WHITE_TEXT']
```

### 5.3 LED Glow Effect

```python
def render_led_glow(surface, x, y, width, height):
    """
    Render subtle glow effect around active LEDs

    Args:
        surface: SDL surface
        x, y: Position of LED digit
        width, height: Size of LED digit

    Algorithm:
        Draw semi-transparent red rectangles with increasing alpha
        to create soft glow effect
    """
    glow_layers = [
        {'offset': 0, 'alpha': 255},  # Core (brightest)
        {'offset': 1, 'alpha': 180},  # Inner glow
        {'offset': 2, 'alpha': 120},  # Middle glow
        {'offset': 3, 'alpha': 60},   # Outer glow
        {'offset': 4, 'alpha': 30},   # Faint outer glow
    ]

    for layer in glow_layers:
        offset = layer['offset']
        alpha = layer['alpha']

        # Create color with alpha
        glow_color = (255, 0, 0, alpha)  # Red with alpha

        # Draw expanded rectangle
        SDL_SetRenderDrawBlendMode(surface, SDL_BLENDMODE_BLEND)
        SDL_SetRenderDrawColor(surface, *glow_color)
        SDL_RenderFillRect(surface, (
            x - offset,
            y - offset,
            width + 2 * offset,
            height + 2 * offset
        ))
```

---

## 6. Data Structures

### 6.1 Button Class

```python
class Button:
    """
    Data structure representing a single button
    """

    def __init__(self, x, y, width, height, label, command, color):
        """
        Initialize button

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
        self.callback = None  # Function to call on click


    def contains_point(self, px, py):
        """
        Check if point (px, py) is inside button bounds

        Returns:
            True if point is inside button, False otherwise
        """
        return (self.x <= px <= self.x + self.width and
                self.y <= py <= self.y + self.height)


    def get_render_color(self):
        """
        Get color to render based on current state

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
```

### 6.2 ButtonGrid Class

```python
class ButtonGrid:
    """
    Collection of buttons with rendering and hit detection
    """

    def __init__(self):
        self.buttons = []  # List of Button objects
        self._build_button_layout()


    def _build_button_layout(self):
        """
        Construct all buttons with positions and properties
        """
        # Row 0
        self.buttons.extend([
            Button(40, 220, 90, 70, 'sqrt', 'sqrt', COLORS['BLACK_KEY']),
            Button(140, 220, 90, 70, 'arcsin', 'asin', COLORS['BLACK_KEY']),
            Button(240, 220, 90, 70, 'arccos', 'acos', COLORS['BLACK_KEY']),
            Button(340, 220, 90, 70, 'arctan', 'atan', COLORS['BLACK_KEY']),
            Button(440, 220, 90, 70, '1/x', 'inv', COLORS['BLACK_KEY']),
        ])

        # Row 1
        self.buttons.extend([
            Button(40, 300, 90, 70, 'x^y', 'xtoy', COLORS['BLACK_KEY']),
            Button(140, 300, 90, 70, 'ln', 'ln', COLORS['BLACK_KEY']),
            Button(240, 300, 90, 70, 'log', 'log', COLORS['BLACK_KEY']),
            Button(340, 300, 90, 70, 'e^x', 'exp', COLORS['BLACK_KEY']),
            Button(440, 300, 90, 70, 'CLR', 'clr', COLORS['BLUE']),
        ])

        # ... (continue for all rows)

        # Row 3 (with ENTER wide button)
        self.buttons.extend([
            Button(40, 460, 190, 70, 'ENTER', 'enter', COLORS['BLUE']),  # WIDE
            Button(240, 460, 90, 70, 'CHS', 'chs', COLORS['BLACK_KEY']),
            Button(340, 460, 90, 70, 'EEX', 'eex', COLORS['BLACK_KEY']),
            Button(440, 460, 90, 70, 'CLR', 'clr', COLORS['BLUE']),
        ])

        # Extended buttons (quaternion/octonion)
        # Row 8
        self.buttons.extend([
            Button(40, 870, 90, 70, 'j', 'j', COLORS['PURPLE']),
            Button(140, 870, 90, 70, 'k', 'k', COLORS['PURPLE']),
            Button(240, 870, 90, 70, 'e0', 'e0', COLORS['ORANGE']),
            Button(340, 870, 90, 70, 'e1', 'e1', COLORS['ORANGE']),
            Button(440, 870, 90, 70, 'e2', 'e2', COLORS['ORANGE']),
        ])

        # ... etc


    def get_button_at(self, x, y):
        """
        Find button at pixel coordinates (x, y)

        Args:
            x, y: Pixel coordinates

        Returns:
            Button object or None if no button at position
        """
        for button in self.buttons:
            if button.contains_point(x, y):
                return button
        return None


    def render(self, surface):
        """
        Render all buttons to SDL surface

        Args:
            surface: SDL renderer
        """
        for button in self.buttons:
            # Get color based on state
            color = button.get_render_color()

            # Draw button rectangle
            SDL_SetRenderDrawColor(surface, *color)
            SDL_RenderFillRect(surface, (button.x, button.y, button.width, button.height))

            # Draw button border (darker)
            border_color = tuple(max(0, c - 40) for c in color)
            SDL_SetRenderDrawColor(surface, *border_color)
            SDL_RenderDrawRect(surface, (button.x, button.y, button.width, button.height))

            # Render text label
            self._render_button_label(surface, button)


    def _render_button_label(self, surface, button):
        """
        Render text label centered on button

        Args:
            surface: SDL renderer
            button: Button object
        """
        # Calculate text position (centered)
        text_x = button.x + button.width // 2
        text_y = button.y + button.height // 2

        # Render text (using SDL_ttf)
        render_text_centered(surface, button.label, text_x, text_y,
                           BUTTON_FONT, button.text_color)


    def animate_press(self, button, start=True):
        """
        Trigger button press animation

        Args:
            button: Button to animate
            start: True for press start, False for release
        """
        if start:
            button.state = ButtonState.PRESSED
        else:
            button.state = ButtonState.NORMAL
```

### 6.3 Display State Structure

```python
class LEDDisplay:
    """
    LED display state and rendering
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.current_value = 0.0
        self.stack_values = [0.0] * 4  # X, Y, Z, T
        self.memory_value = 0.0
        self.display_string = " 0.000000000 E+00"


    def update(self, stack):
        """
        Update display from calculator stack

        Args:
            stack: HP35Stack object
        """
        self.current_value = stack.stack[0]  # X register
        self.stack_values = stack.stack[:4]
        self.memory_value = stack.storcl

        # Format for display
        self.display_string = format_number_for_display(self.current_value)


    def render(self, surface):
        """
        Render LED display to surface

        Args:
            surface: SDL renderer
        """
        # Draw background
        SDL_SetRenderDrawColor(surface, *COLORS['DISPLAY_BG'])
        SDL_RenderFillRect(surface, (self.x, self.y, self.width, self.height))

        # Render stack display
        render_stack_display(surface, self.stack_values, self.memory_value)

        # Render main X register (large LED digits)
        x_display_x = self.x + 100
        x_display_y = self.y + 120
        render_led_display_string(surface, x_display_x, x_display_y,
                                 self.display_string, max_digits=15)
```

---

## 7. Rendering Pipeline

### 7.1 Frame-by-Frame Rendering Sequence

```python
def render_frame(window):
    """
    Render complete frame

    Rendering order (back to front):
    1. Clear screen (case background)
    2. Render display background
    3. Render LED display
    4. Render buttons
    5. Present frame to screen

    Args:
        window: HP35Window object containing all components
    """
    # Step 1: Clear entire window with case color
    SDL_SetRenderDrawColor(window.renderer, *COLORS['CASE_BLACK'])
    SDL_RenderClear(window.renderer)

    # Step 2: Render display region background
    SDL_SetRenderDrawColor(window.renderer, *COLORS['DISPLAY_BG'])
    SDL_RenderFillRect(window.renderer, DISPLAY_AREA)

    # Step 3: Render LED display
    window.led_display.render(window.renderer)

    # Step 4: Render all buttons
    window.button_grid.render(window.renderer)

    # Step 5: Present final frame
    SDL_RenderPresent(window.renderer)
```

### 7.2 Double Buffering Approach

SDL2 automatically provides double buffering:

```python
# Rendering to back buffer
SDL_RenderClear(renderer)
# ... draw operations ...
SDL_RenderPresent(renderer)  # Swap buffers, present to screen
```

No manual buffer management needed - SDL handles this internally.

### 7.3 Update Regions (Optimization)

For initial implementation, full-frame rendering is sufficient at 60 FPS. Future optimization could use dirty rectangles:

```python
class DirtyRectManager:
    """
    Track which regions need redrawing (optimization)
    """

    def __init__(self):
        self.dirty_rects = []


    def mark_dirty(self, x, y, width, height):
        """Mark rectangular region as needing redraw"""
        self.dirty_rects.append((x, y, width, height))


    def clear(self):
        """Clear all dirty regions"""
        self.dirty_rects = []


    def render_dirty_regions_only(self, renderer, render_func):
        """Render only dirty regions"""
        for rect in self.dirty_rects:
            SDL_RenderSetClipRect(renderer, rect)
            render_func(renderer)
        SDL_RenderSetClipRect(renderer, None)
        self.clear()
```

---

## 8. Integration with Calculator

### 8.1 Calculator Instantiation

```python
class HP35Window:
    """
    Main window class integrating all components
    """

    def __init__(self, width=600, height=1080):
        # Initialize SDL
        SDL_Init(SDL_INIT_VIDEO)

        # Create window
        self.window = SDL_CreateWindow(
            "CNC - HP-35 Calculator",
            SDL_WINDOWPOS_CENTERED,
            SDL_WINDOWPOS_CENTERED,
            width, height,
            SDL_WINDOW_SHOWN
        )

        # Create renderer
        self.renderer = SDL_CreateRenderer(
            self.window, -1,
            SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC
        )

        # Initialize calculator engine
        self.calculator = ComplexNumberCalculator(stack_depth=8)

        # Initialize GUI components
        self.button_grid = ButtonGrid()
        self.led_display = LEDDisplay(20, 20, 560, 160)
        self.event_handler = EventHandler(self.button_grid)

        # Connect button callbacks
        self._setup_button_callbacks()


    def _setup_button_callbacks(self):
        """
        Connect each button to calculator command
        """
        for button in self.button_grid.buttons:
            # Create closure to capture button's command
            def make_callback(cmd):
                return lambda: self.on_button_press(cmd)

            button.callback = make_callback(button.command)


    def on_button_press(self, command):
        """
        Handle button press by executing calculator command

        Args:
            command: Calculator command string (e.g., 'sqrt', '7', '+')
        """
        # Execute command on calculator
        self.calculator.handle_string(command)

        # Update display
        self.led_display.update(self.calculator.stack)


    def run(self):
        """Main event loop"""
        running = True
        while running:
            # Process events
            for event in SDL_PollEvents():
                running = self.event_handler.handle_event(event)
                if not running:
                    break

            # Render frame
            render_frame(self)

            # Frame rate limiting (60 FPS)
            SDL_Delay(16)


    def cleanup(self):
        """Clean up SDL resources"""
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
        SDL_Quit()
```

### 8.2 Stack Update Flow

```
User clicks button
     ↓
Button.callback() invoked
     ↓
HP35Window.on_button_press(command)
     ↓
ComplexNumberCalculator.handle_string(command)
     ↓
Calculator processes command
  • Tokenizes input
  • Executes operation
  • Updates HP35Stack
     ↓
LEDDisplay.update(stack)
     ↓
Display updated on next render frame
```

### 8.3 Error Handling Flow

```python
def on_button_press(self, command):
    """
    Handle button press with error handling
    """
    try:
        # Execute command
        result = self.calculator.handle_string(command)

        # Check for error result
        if isinstance(result, tuple) and result[0] == -1:
            # Error occurred
            self.display_error(result[1])
        else:
            # Success - update display
            self.led_display.update(self.calculator.stack)

    except ZeroDivisionError:
        self.display_error("ERROR: DIV/0")
    except OverflowError:
        self.display_error("ERROR: OVERFLOW")
    except Exception as e:
        self.display_error(f"ERROR: {str(e)[:10]}")


def display_error(self, message):
    """
    Display error message in LED display

    Args:
        message: Error message string
    """
    self.led_display.display_string = message.center(15)

    # Optional: Schedule error clear after 2 seconds
    # (would need timer mechanism)
```

---

## 9. Rendering Pipeline Details

### 9.1 SDL Initialization

```python
def initialize_sdl():
    """
    Initialize SDL subsystems

    Returns:
        True on success, False on failure
    """
    # Initialize SDL video subsystem
    if SDL_Init(SDL_INIT_VIDEO) != 0:
        print(f"SDL initialization failed: {SDL_GetError()}")
        return False

    # Initialize SDL_ttf (for text rendering)
    if TTF_Init() != 0:
        print(f"SDL_ttf initialization failed: {TTF_GetError()}")
        SDL_Quit()
        return False

    return True


def load_fonts():
    """
    Load TrueType fonts for button labels

    Returns:
        Dictionary of font handles
    """
    fonts = {}

    # Button label font (medium size)
    fonts['BUTTON'] = TTF_OpenFont("fonts/Arial.ttf", 14)

    # Display label font (small size)
    fonts['LABEL'] = TTF_OpenFont("fonts/Arial.ttf", 10)

    # Check for errors
    for name, font in fonts.items():
        if font is None:
            print(f"Failed to load font {name}: {TTF_GetError()}")

    return fonts
```

### 9.2 Text Rendering Helper

```python
def render_text_centered(surface, text, x, y, font, color):
    """
    Render text centered at position (x, y)

    Args:
        surface: SDL renderer
        text: String to render
        x, y: Center position
        font: TTF font handle
        color: RGB tuple
    """
    # Create text surface
    text_surface = TTF_RenderText_Blended(font, text, color)

    if text_surface is None:
        return  # Failed to render

    # Get text dimensions
    text_width = text_surface.w
    text_height = text_surface.h

    # Calculate top-left position to center text
    text_x = x - text_width // 2
    text_y = y - text_height // 2

    # Create texture from surface
    texture = SDL_CreateTextureFromSurface(surface, text_surface)

    # Render texture
    dest_rect = (text_x, text_y, text_width, text_height)
    SDL_RenderCopy(surface, texture, None, dest_rect)

    # Clean up
    SDL_DestroyTexture(texture)
    SDL_FreeSurface(text_surface)
```

---

## 10. Implementation Checklist

### Phase 1: Basic Structure
- [ ] Set up SDL window and renderer
- [ ] Implement main event loop
- [ ] Create basic button data structures
- [ ] Implement button hit detection
- [ ] Render simple button rectangles

### Phase 2: Display
- [ ] Implement seven-segment digit rendering
- [ ] Create segment position calculations
- [ ] Implement character-to-segment mapping
- [ ] Render complete LED display string
- [ ] Add stack register display

### Phase 3: Button Layout
- [ ] Define all button positions and sizes
- [ ] Implement button color scheme
- [ ] Add button text labels
- [ ] Create ENTER wide button
- [ ] Add extended buttons (quaternion/octonion)

### Phase 4: Event Handling
- [ ] Implement mouse motion tracking
- [ ] Add hover state visual feedback
- [ ] Implement button press/release logic
- [ ] Connect button callbacks to calculator

### Phase 5: Calculator Integration
- [ ] Instantiate ComplexNumberCalculator
- [ ] Map button commands to calculator operations
- [ ] Update display after each operation
- [ ] Handle error conditions

### Phase 6: Polish
- [ ] Add LED glow effect
- [ ] Implement button press animation
- [ ] Fine-tune colors to match HP-35
- [ ] Optimize rendering performance
- [ ] Add cleanup and exit handling

---

## 11. File Structure

```
cnc/
├── cnc_gui.py              # Main GUI implementation (this design)
├── cnc.py                  # Calculator engine (existing)
├── hp35stack.py            # Stack implementation (existing)
├── quaternion.py           # Quaternion class (existing)
├── octonion.py             # Octonion class (existing)
├── fonts/
│   └── Arial.ttf           # Font for button labels
└── Makefile                # Build system with SDL setup target
```

---

## 12. Performance Targets

- **Frame Rate**: 60 FPS (16.67ms per frame)
- **Click Response**: < 100ms from mouse up to display update
- **Startup Time**: < 2 seconds to show window
- **Memory Usage**: < 50 MB total

---

## 13. Testing Considerations

### Visual Tests
- Compare rendered calculator to HP-35 photos
- Verify button colors match original
- Check LED display authenticity
- Validate button proportions

### Functional Tests
- Test all 47 button clicks
- Verify calculator operations work correctly
- Test stack display updates
- Validate error handling

### Platform Tests
- Test on macOS (latest version)
- Test on Linux (Ubuntu, Fedora)
- Verify SDL installation instructions work

---

## Document Metadata

- **Version**: 1.0
- **Date**: 2026-02-09
- **Author**: Generated for CNC HP-35 GUI Project
- **Status**: Design phase - ready for implementation
- **Related Documents**:
  - `/Users/jordanh/Src/cnc/.vibe/docs/requirements.md`
  - `/Users/jordanh/Src/cnc/.vibe/docs/architecture.md`
