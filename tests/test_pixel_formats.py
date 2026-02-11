#!/usr/bin/env python3
"""Test different SDL pixel formats"""

import sys
import ctypes
from ctypes import c_int
import sdl2
import sdl2.ext
from PIL import Image
import numpy as np

def test_format(format_name, format_const):
    """Test a specific pixel format"""
    print(f"\n{'='*60}")
    print(f"Testing: {format_name}")
    print('='*60)
    
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    
    window = sdl2.SDL_CreateWindow(
        b"Test",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        300, 100,
        sdl2.SDL_WINDOW_SHOWN
    )
    
    renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_SOFTWARE)
    
    # Draw test colors
    sdl2.SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)  # Red
    rect = sdl2.SDL_Rect(10, 10, 80, 80)
    sdl2.SDL_RenderFillRect(renderer, rect)
    
    sdl2.SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255)  # Green
    rect = sdl2.SDL_Rect(110, 10, 80, 80)
    sdl2.SDL_RenderFillRect(renderer, rect)
    
    sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255)  # Blue
    rect = sdl2.SDL_Rect(210, 10, 80, 80)
    sdl2.SDL_RenderFillRect(renderer, rect)
    
    sdl2.SDL_RenderPresent(renderer)
    sdl2.SDL_Delay(50)
    
    # Read pixels
    w, h = c_int(), c_int()
    sdl2.SDL_GetRendererOutputSize(renderer, ctypes.byref(w), ctypes.byref(h))
    width, height = w.value, h.value
    
    pitch = width * 4
    pixels = (ctypes.c_uint8 * (pitch * height))()
    
    result = sdl2.SDL_RenderReadPixels(
        renderer,
        None,
        format_const,
        pixels,
        pitch
    )
    
    if result != 0:
        print(f"❌ Error: {sdl2.SDL_GetError()}")
        sdl2.SDL_DestroyRenderer(renderer)
        sdl2.SDL_DestroyWindow(window)
        sdl2.SDL_Quit()
        return None
    
    arr = np.frombuffer(pixels, dtype=np.uint8).reshape((height, width, 4))
    
    red_px = arr[50, 50, :3]
    green_px = arr[50, 150, :3]
    blue_px = arr[50, 250, :3]
    
    print(f"Red:   {red_px}   Expected: [255,   0,   0]")
    print(f"Green: {green_px}   Expected: [  0, 255,   0]")
    print(f"Blue:  {blue_px}   Expected: [  0,   0, 255]")
    
    correct = (np.array_equal(red_px, [255, 0, 0]) and 
               np.array_equal(green_px, [0, 255, 0]) and
               np.array_equal(blue_px, [0, 0, 255]))
    
    if correct:
        print("✅ CORRECT!")
    else:
        print("❌ INCORRECT")
    
    sdl2.SDL_DestroyRenderer(renderer)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    
    return arr if correct else None

# Test formats
formats = [
    ("RGBA8888", sdl2.SDL_PIXELFORMAT_RGBA8888),
    ("ARGB8888", sdl2.SDL_PIXELFORMAT_ARGB8888),
    ("BGRA8888", sdl2.SDL_PIXELFORMAT_BGRA8888),
    ("ABGR8888", sdl2.SDL_PIXELFORMAT_ABGR8888),
]

for name, fmt in formats:
    test_format(name, fmt)
