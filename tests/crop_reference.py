#!/usr/bin/env python3
"""
Crop the HP-35 reference photo to just the calculator face panel.
"""

import sys
from PIL import Image


def crop_calculator_face(input_path, output_path):
    """Crop reference image to just the display + buttons area."""
    img = Image.open(input_path)
    width, height = img.size

    print(f"Original image: {width}×{height}")

    # Approximate crop coordinates (adjust based on reference image)
    # Looking at the reference, the calculator face starts around x=200, y=100
    # and extends to roughly x=1330, y=2450

    # These coordinates should capture just the display + button panel
    left = 200
    top = 100
    right = 1330
    bottom = 2450

    cropped = img.crop((left, top, right, bottom))
    cropped.save(output_path)

    print(f"Cropped to: {cropped.size[0]}×{cropped.size[1]}")
    print(f"Saved: {output_path}")

    return cropped.size


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python crop_reference.py <input.jpg> <output.jpg>")
        sys.exit(1)

    crop_calculator_face(sys.argv[1], sys.argv[2])
