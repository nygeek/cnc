#!/usr/bin/env python3
"""Test HP-35 GUI calculator functionality"""

import sys
sys.path.insert(0, '/Users/jordanh/Src/cnc')

from cnc import ComplexNumberCalculator

def test_operations():
    """Test basic calculator operations"""
    calc = ComplexNumberCalculator(stack_depth=8)
    
    tests = [
        ("Basic addition", ["2", "3", "+"], 5.0),
        ("Basic subtraction", ["5", "3", "-"], 2.0),
        ("Basic multiplication", ["4", "5", "*"], 20.0),
        ("Basic division", ["10", "2", "/"], 5.0),
        ("Square root", ["16", "sqrt"], 4.0),
        ("Power", ["2", "3", "xtoy"], 8.0),
        ("Logarithm", ["100", "log"], 2.0),
        ("Natural log", ["2.71828", "ln"], 1.0),
        ("Exponential", ["1", "exp"], 2.71828),
        ("Sine", ["0", "sin"], 0.0),
        ("Cosine", ["0", "cos"], 1.0),
        ("Clear", ["5", "clr"], 0.0),
        ("Change sign", ["5", "chs"], -5.0),
        ("Exchange xy", ["2", "3", "exch"], 2.0),
        ("Roll down", ["1", "2", "3", "down"], 1.0),
    ]
    
    print("Testing HP-35 Calculator Operations")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, commands, expected in tests:
        calc = ComplexNumberCalculator(stack_depth=8)  # Fresh calc for each test
        
        try:
            for cmd in commands:
                calc.handle_string(cmd)
            
            # Access the stack correctly via calc.stack.stack
            result = calc.stack.stack[0].real if hasattr(calc.stack.stack[0], 'real') else calc.stack.stack[0]
            
            # Allow small floating point error
            if abs(result - expected) < 0.001:
                print(f"✓ {name:25s} = {result:.4f}")
                passed += 1
            else:
                print(f"✗ {name:25s} = {result:.4f} (expected {expected:.4f})")
                failed += 1
                
        except Exception as e:
            print(f"✗ {name:25s} ERROR: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == '__main__':
    success = test_operations()
    sys.exit(0 if success else 1)
