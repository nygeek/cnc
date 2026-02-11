#!/usr/bin/env python3
"""Test SDL_SaveBMP directly without pixel format conversion"""

import sys
sys.path.insert(0, '/Users/jordanh/Src/cnc')

# Modify cnc_gui temporarily to use SDL_SaveBMP on window surface
print("This would test SDL_SaveBMP on window surface directly")
print("to see if the issue is in pixel format conversion or rendering")
