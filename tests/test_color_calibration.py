#!/usr/bin/env python3
"""
Color calibration test - renders known RGB colors and checks what they produce.
This helps us figure out the color transformation happening in SDL.
"""

import sys
sys.path.insert(0, '/Users/jordanh/Src/cnc')

# Temporarily modify cnc_gui to render test colors
test_colors = {
    'pure_red': (255, 0, 0),
    'pure_green': (0, 255, 0),
    'pure_blue': (0, 0, 255),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'yellow': (255, 255, 0),
    'light_blue': (90, 180, 220),  # Target blue for HP-35
    'medium_gray': (85, 85, 85),   # Target case color
}

print("Color Calibration Test")
print("=" * 60)
print("\nTo use this:")
print("1. Modify cnc_gui.py to render test color patches")
print("2. Take screenshots")
print("3. Measure actual RGB values in the PNG")
print("4. Calculate the transformation matrix")
print("\nTest colors:")
for name, rgb in test_colors.items():
    print(f"  {name:15s}: RGB{rgb}")
