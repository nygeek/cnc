""" CNC - Complex Number Calculator

Started 2024-08-17 by Marc Donner
Part of the Stibitz project
Copyright (C) 2024 Marc Donner

This class and the test code in the main() function at the bottom
are written as part of my Complex Number Calculator project.

"""

import math

PREFIX = "  "

class Complex:
    """The core of our Complex Number Calculator."""
    def __init__(self, realpart, imagpart, _debug=False):
        self.r = realpart
        self.i = imagpart
        if _debug:
            print(PREFIX * _debug,
                  "Complex(realpart:", realpart,
                  ", imagpart:", imagpart,
                  ")")
            print(PREFIX * _debug, "Complex => ", self)

    # These methods return Complex results

    def add(self, addend, _debug=False):
        """Add addend to self."""
        if _debug:
            print(PREFIX * _debug,
                  "add(self:", self,
                  ", addend:", addend)
        _result = Complex(
                self.r + addend.r,
                self.i + addend.i,
                _debug + 1 if _debug else False)
        if _debug:
            print(PREFIX * _debug, "add =>", _result)
        return _result

    def sub(self, diminuend, _debug=False):
        """Subtract diminuend from self."""
        if _debug:
            print(PREFIX * _debug,
                  "sub(self:", self,
                  ", diminuend:", diminuend)
        _result = Complex(
                self.r - diminuend.r,
                self.i - diminuend.i,
                _debug + 1 if _debug else False)
        if _debug:
            print(PREFIX * _debug, "sub =>", _result)
        return _result

    def mul(self, multiplicand, _debug=False):
        """Multiply self with multiplicand"""
        if _debug:
            print(PREFIX * _debug,
                  "mul(self:", self,
                  ", multiplicand:", multiplicand, ")")
        _result = Complex(
                float(self.r * multiplicand.r - self.i * multiplicand.i),
                float(self.r * multiplicand.i + self.i * multiplicand.r),
                _debug + 1 if _debug else False)
        if _debug:
            print(PREFIX * _debug, "mul =>", _result)
        return _result

    def conj(self, _debug=False):
        """Conjugate of self"""
        if _debug:
            print(PREFIX * _debug, "conj(self:", self, ")")
        _result = Complex(self.r, -self.i,
                          _debug + 1 if _debug else False)
        if _debug:
            print(PREFIX * _debug, "conj =>", _result)
        return _result

    def inv(self, _debug=False):
        """Multiplicative inverse (1/self)"""
        l_squared = float(self.mod_squared(_debug + 1 if _debug else False))
        if l_squared == 0:
            print("inv: Error - divide by zero")
            return self
        _result = Complex(
                float(self.r / l_squared),
                float(-self.i / l_squared),
                _debug + 1 if _debug else False)
        if _debug:
            print(PREFIX * _debug, "inv(self:", self, ")")
            print(PREFIX * _debug, "inv: l_squared:", l_squared)
            print(PREFIX * _debug, "inv => (", _result)
        return _result

    def div(self, divisor, _debug=False):
        """Divide self by divisor"""
        if _debug:
            print(PREFIX * _debug,
                  "div(self:", self,
                  ", divisor:", divisor, ")")
        _result = self.mul(
                divisor.inv(_debug + 1 if _debug else False),
                _debug + 1 if _debug else False)
        if _debug:
            print(PREFIX * _debug, "div =>", _result)
        return _result

    def exp(self, _debug=False):
        """Complex exponential!"""
        _magnitude = float(math.exp(self.r))
        if _debug:
            print(PREFIX * _debug, "exp(self:", self, ")")
        _result = Complex(_magnitude * math.cos(self.i),
                          _magnitude * math.sin(self.i),
                          _debug + 1 if _debug else False)
        if _debug:
            print(PREFIX * _debug, "exp =>", _result)
        return _result

    def log(self, _debug=False):
        """Complex logarithm"""
        _r = math.log(self.mod(_debug + 1 if _debug else False))
        _arg = math.atan2(self.i, self.r)
        _result = Complex(float(_r), float(_arg),
                          _debug + 1 if _debug else False)
        if _debug:
            print(PREFIX * _debug,
                  "log(self: ", self, ")")
            print(PREFIX * _debug, "log: ",
                  "_r:", _r, ", _arg: ", _arg)
            print(PREFIX * _debug, "log => ", _result)
        return _result

    # These methods return Real results

    def mod_squared(self, _debug=False):
        """Utility function r^2 + i^2"""
        if _debug:
            print(PREFIX * _debug, "mod_squared(self:", self, ")")
        _result = float(self.dot(self, _debug + 1 if _debug else False))
        if _debug:
            print(PREFIX * _debug, "mod_squared =>", _result)
        return _result

    def mod(self, _debug=False):
        """Utility function - sqrt(mod_squared)"""
        if _debug:
            print(PREFIX * _debug, "mod(self:", self, ")")
        _result = math.sqrt(self.mod_squared(
            _debug + 1 if _debug else False))
        if _debug:
            print(PREFIX * _debug, "mod =>", _result)
        return _result

    def real(self, _debug=False):
        """Real part"""
        if _debug:
            print(PREFIX * _debug, "real(self:", self, ")")
            print(PREFIX * _debug, "real =>", "self.r:", self.r)
        return self.r

    def imag(self, _debug=False):
        """Imaginary part"""
        if _debug:
            print(PREFIX * _debug, "imag(self:", self, ")")
            print(PREFIX * _debug, "imag =>", "imag.i:", self.i)
        return self.i

    def dot(self, z, _debug=False):
        """Dot product of self with z."""
        if _debug:
            print(PREFIX * _debug, "dot(self:", self, ", z:", z, ")")
        _result = self.mul(z.conj(_debug + 1 if _debug else False),
                           _debug + 1 if _debug else False).real(
                                   _debug + 1 if _debug else False)
        if _debug:
            print(PREFIX * _debug, "dot =>", _result)
        return _result

    # Utility

    def __str__(self):
        return "(" + str(self.r) + " + " + str(self.i) + "i)"

def main():
    """Main"""
    debug = True
    print("debug: ", debug)
    x = Complex(1, 1, debug)
    print("x:", x)
    y = Complex(2, 3)
    print("y:", y)
    z = x.add(y, debug)
    print("z [x+y]:", z)
    z = x.sub(y, debug)
    print("z [x-y]:", z)
    z = x.mul(y, debug)
    print("z [x*y]:", z)
    w = Complex(0, 1, debug)
    print("w:", w)
    z = w.mul(w, debug)
    print("z [w*w]:", z)
    print("mod_squared(z):", z.mod_squared(debug))
    z = x.inv(debug)
    print("z [1/x]:", z)

    z = x.mul(x.inv(debug), debug)
    print("z [x/x]:", z)
    z = y.div(x, debug)
    print("z [y/x]:", z)
    print("mod(x):", x.mod(debug))
    print("real(y):", y.real(debug))
    print("imag(y):", y.imag(debug))
    z = Complex(y.real(debug), y.imag(debug), debug)
    print("z [y reconstructed]:", z)
    w = Complex(0, math.pi, debug)
    print("w [pi]:", w)
    z = w.exp(debug)
    print("z [e**i(pi)]:", z)
    w = Complex(-1, 0, debug)
    print("w [-1]:", w)
    z = w.log(debug)
    print("z [log(-1)]:", z)

if __name__ == '__main__':
    main()
