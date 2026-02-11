#!/usr/bin/env python3
"""Test SDL color channel order"""

import sys
import ctypes
from ctypes import c_int, c_uint8

import sdl2
import sdl2.ext
from PIL import Image
import numpy as np

# Initialize SDL
sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

# Create small window
window = sdl2.SDL_CreateWindow(
    b"Color Test",
    sdl2.SDL_WINDOWPOS_CENTERED,
    sdl2.SDL_WINDOWPOS_CENTERED,
    300, 100,
    sdl2.SDL_WINDOW_SHOWN
)

# Software renderer
renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_SOFTWARE)

# Draw pure red, green, blue squares
# Red square (left)
sdl2.SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)
rect = sdl2.SDL_Rect(10, 10, 80, 80)
sdl2.SDL_RenderFillRect(renderer, rect)

# Green square (middle)
sdl2.SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255)
rect = sdl2.SDL_Rect(110, 10, 80, 80)
sdl2.SDL_RenderFillRect(renderer, rect)

# Blue square (right)
sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255)
rect = sdl2.SDL_Rect(210, 10, 80, 80)
sdl2.SDL_RenderFillRect(renderer, rect)

sdl2.SDL_RenderPresent(renderer)
sdl2.SDL_Delay(100)

# Read pixels
w, h = c_int(), c_int()
sdl2.SDL_GetRendererOutputSize(renderer, ctypes.byref(w), ctypes.byref(h))
width, height = w.value, h.value

pitch = width * 4
pixels = (ctypes.c_uint8 * (pitch * height))()

result = sdl2.SDL_RenderReadPixels(
    renderer,
    None,
    sdl2.SDL_PIXELFORMAT_RGBA8888,
    pixels,
    pitch
)

if result != 0:
    print(f"Error reading pixels: {sdl2.SDL_GetError()}")
    sys.exit(1)

# Convert to numpy
arr = np.frombuffer(pixels, dtype=np.uint8).reshape((height, width, 4))

# Check center pixel of each square
red_pixel = arr[50, 50, :3]
green_pixel = arr[50, 150, :3]
blue_pixel = arr[50, 250, :3]

print("Expected RGB values:")
print(f"  Red square:   [255,   0,   0]")
print(f"  Green square: [  0, 255,   0]")
print(f"  Blue square:  [  0,   0, 255]")
print()
print("Actual pixel values (as RGBA):")
print(f"  Red square:   {red_pixel}")
print(f"  Green square: {green_pixel}")
print(f"  Blue square:  {blue_pixel}")
print()

# Determine channel order
if np.array_equal(red_pixel, [255, 0, 0]):
    print("✓ Channel order: RGB (correct)")
elif np.array_equal(red_pixel, [0, 0, 255]):
    print("✗ Channel order: BGR (swapped)")
else:
    print(f"? Channel order: unknown pattern")

# Save image
rgb_arr = arr[:, :, :3]
img = Image.fromarray(rgb_arr, 'RGB')
img.save('color_test_current.png', 'PNG')
print("\nSaved: color_test_current.png")

# Also try BGR swap
bgr_arr = arr[:, :, [2, 1, 0]]
img_bgr = Image.fromarray(bgr_arr, 'RGB')
img_bgr.save('color_test_bgr_swap.png', 'PNG')
print("Saved: color_test_bgr_swap.png (with BGR->RGB swap)")

sdl2.SDL_DestroyRenderer(renderer)
sdl2.SDL_DestroyWindow(window)
sdl2.SDL_Quit()
