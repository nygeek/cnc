#!/usr/bin/env python3
"""Quick color test iterations for HP-35 GUI."""

import subprocess
import sys

# Test different color configurations
COLOR_TESTS = {
    'test1_cyan_blue': {
        'BLUE': (90, 180, 220),     # Light cyan blue
        'CASE_BLACK': (80, 80, 80), # Medium gray
        'LED_ON': (255, 40, 40),    # Bright red
    },
    'test2_darker_blue': {
        'BLUE': (70, 150, 200),
        'CASE_BLACK': (70, 70, 70),
        'LED_ON': (255, 40, 40),
    },
    'test3_lighter': {
        'BLUE': (100, 190, 230),
        'CASE_BLACK': (90, 90, 90),
        'LED_ON': (255, 40, 40),
    },
}


def test_color_config(name, colors):
    """Test a color configuration and return comparison score."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    for color_name, rgb in colors.items():
        print(f"  {color_name}: {rgb}")

    # TODO: Update cnc_gui.py colors, render, compare
    # For now, just print the configuration
    print(f"\nRun this test manually:")
    print(f"  Update COLORS dict in cnc_gui.py")
    print(f"  .venv/bin/python ./cnc_gui.py --screenshot --output {name}.png")
    print(f"  .venv/bin/python ./compare_renders.py hp35_reference_cropped.jpg {name}.png")


if __name__ == '__main__':
    for name, colors in COLOR_TESTS.items():
        test_color_config(name, colors)
