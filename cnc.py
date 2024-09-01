""" CNC - Complex Number Calculator

Started 2024-08-17 by Marc Donner
Part of the Stibitz project
Copyright (C) 2024 Marc Donner

This class and the test code in the main() function at the bottom
are written as part of my Complex Number Calculator project.

$Id$

"""

# public libraries
import math

# cnc infrastructure
from debug import Debug

class Complex:
    """The core of our Complex Number Calculator."""
    def __init__(self, realpart, imagpart, debug):
        if debug.get():
            print(f"{debug.indent()}Complex({realpart}, {imagpart})")
        self.r = realpart
        self.i = imagpart
        if debug.get():
            print(f"{debug.indent()}Complex => {self}")

    # These methods return Complex results

    def chs(self, debug):
        """ change the sign of self """
        if debug.get():
            print(f"{debug.indent()}chs({self})")
        _old = debug.inc()
        _result = Complex(-self.r, -self.i, debug)
        debug.reset(_old)
        return _result


    def add(self, addend, debug):
        """Add addend to self."""
        if debug.get():
            print(f"{debug.indent()}add({self}, {addend})")
        _old = debug.inc()
        _result = Complex(
                self.r + addend.r,
                self.i + addend.i,
                debug)
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}add => {_result}")
        return _result


    def arccos(self, debug):
        """ compute the inverse cosine """
        if debug.get():
            print(f"{debug.indent()}arccos({self}")
        _old = debug.inc()
        # arccos(z) = (1/i) ln( z + sqrt(1 - z^2) )
        _t1 = self.mul(self, debug) # z^2
        _t2 = Complex(1, 0, debug).sub(_t1, debug).sqrt(debug) # sqrt(1-z^2)
        _t2 = _t2.add(self, debug) # z + sqrt(1-z^2)
        result =  _t2.ln(debug).mul(Complex(0, -1, debug), debug)
        debug.reset(_old)
        return result


    def arcsin(self, debug):
        """ compute the inverse sine """
        if debug.get():
            print(f"{debug.indent()}arcsin({self}")
        _old = debug.inc()
        # arcsin(z) = (1/i) ln( iz + sqrt(1 - z^2) )
        _t1 = self.mul(self, debug) # z^2
        _t2 = Complex(1, 0, debug).sub(_t1, debug).sqrt(debug) # sqrt(1-z^2)
        _t2 = _t2.add(self.mul(Complex(0, 1, debug), debug), debug) # iz + sqrt(1-z^2)
        # 1/i is -i
        result = _t2.ln(debug).mul(Complex(0, -1, debug), debug)
        debug.reset(_old)
        return result


    def arctan(self, debug):
        """ compute the inverse tangent """
        if debug.get():
            print(f"{debug.indent()}arctan({self}")
        _old = debug.inc()
        # arctan(z) = (1/2i) ln( (i-z) / (i+z) ) [plus k pi, but we'll
        # restrict ourselves to range from (0-i) to (0+i)]
        _num = Complex(0, 1, debug).sub(self, debug) # numerator
        _den = Complex(0, 1, debug).add(self, debug) # denominator
        result = _num.div(_den, debug).ln(debug).mul(Complex(0, -.5, debug), debug)
        debug.reset(_old)
        return result


    def cos(self, debug):
        """ cosine function """
        # this depends on the identity:
        # cos z = ( e^iz + e^-iz ) / 2
        if debug.get():
            print(f"{debug.indent()}cos({self}")
        _old = debug.inc()
        _iz = self.mul(Complex(0, 1, debug), debug)
        _result = _iz.exp(debug).add(_iz.chs(debug).exp(debug), debug)
        _result = _result.div(Complex(2, 0, debug), debug)
        debug.reset(_old)
        return _result


    def sin(self, debug):
        """ sine function """
        # this depends on the identity:
        # sin(a + bi) = sin(a)cosh(b) + i cos(a)sinh(b)
        if debug.get():
            print(f"{debug.indent()}sin({self}")
        _old = debug.inc()
        _result = Complex(
                math.sin(self.r)*math.cosh(self.i),
                math.cos(self.r)*math.sinh(self.i),
                debug.inc())
        debug.reset(_old)
        return _result


    def tan(self, debug):
        """ tangent function """
        # this depends on the identity:
        # tan(a + bi) = sin(a + bi) / cos(a + bi)
        if debug.get():
            print(f"{debug.indent()}tan({self}")
        _old = debug.inc()
        _sin = self.sin(debug)
        _cos = self.cos(debug)
        _result = _sin.div(_cos, debug)
        debug.reset(_old)
        return _result


    def sub(self, diminuend, debug):
        """Subtract diminuend from self."""
        if debug.get():
            print(f"{debug.indent()}sub({self}, {diminuend})")
        _old = debug.inc()
        _result = Complex(
                self.r - diminuend.r,
                self.i - diminuend.i,
                debug)
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}sub => {_result}")
        return _result


    def mul(self, multiplicand, debug):
        """Multiply self with multiplicand"""
        if debug.get():
            print(f"{debug.indent()}mul({self}, {multiplicand})")
        _old = debug.inc()
        _result = Complex(
                float(self.r * multiplicand.r - self.i * multiplicand.i),
                float(self.r * multiplicand.i + self.i * multiplicand.r),
                debug)
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}mul => {_result}")
        return _result


    def conj(self, debug):
        """Conjugate of self"""
        if debug.get():
            print(f"{debug.indent()}conj({self})")
        _old = debug.inc()
        _result = Complex(self.r, -self.i, debug)
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}conj => {_result}")
        return _result


    def inv(self, debug):
        """Multiplicative inverse (1/self)"""
        if debug.get():
            print(f"{debug.indent()}inv({self})")
        _old = debug.inc()
        l_squared = float(self.mod_squared(debug))
        if l_squared == 0:
            print("inv: Error - divide by zero")
            return self
        _result = Complex(
                float(self.r / l_squared),
                float(-self.i / l_squared),
                debug)
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}inv: l_squared: {l_squared}")
            print(f"{debug.indent()}inv => {_result}")
        return _result


    def div(self, divisor, debug):
        """Divide self by divisor"""
        if debug.get():
            print(f"{debug.indent()}div({self}, {divisor})")
        _old = debug.inc()
        _result = self.mul(divisor.inv(debug),debug)
        debug.reset(_old)
        if debug.get():
            print(debug.indent(), "div =>", _result)
        return _result


    def exp(self, debug):
        """Complex exponential!"""
        if debug.get():
            print(f"{debug.indent()}exp({self})")
        _old = debug.inc()
        _magnitude = float(math.exp(self.r))
        _result = Complex(_magnitude * math.cos(self.i),
                          _magnitude * math.sin(self.i),
                          debug)
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}exp => {_result}")
        return _result


    def ln(self, debug):
        """Complex logarithm"""
        if debug.get():
            print(f"{debug.indent()}ln({self})")
        _old = debug.inc()
        _r = math.log(self.mod(debug))
        _arg = math.atan2(self.i, self.r)
        _result = Complex(float(_r), float(_arg), debug)
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}ln ==> {_result}")
        return _result


    def sqrt(self, debug):
        """Complex square root"""
        if debug.get():
            print(f"{debug.indent()}sqrt({self})")
        _old = debug.inc()
        _r = self.mod(debug)
        _x = self.real(debug)
        _result = Complex(
                math.sqrt((_r + _x)/2),
                math.sqrt((_r - _x)/2),
                debug)
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}sqrt ==> ({_result})")
        return _result


    # These methods return Real results

    def mod_squared(self, debug):
        """Utility function r^2 + i^2"""
        if debug.get():
            print(f"{debug.indent()}mod_squared({self})")
        _old = debug.inc()
        _result = float(self.dot(self, debug))
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}mod_squared => {_result}")
        return _result


    def mod(self, debug):
        """Utility function - sqrt(mod_squared)"""
        if debug.get():
            print(f"{debug.indent()}mod({self})")
        _old = debug.inc()
        _result = math.sqrt(self.mod_squared(debug))
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}mod => {_result}")
        return _result


    def arg(self, debug):
        """ handle arg """
        if debug.get():
            print(f"{debug.indent()}arg({self})")
        _old = debug.inc()
        _result = math.atan2(self.i, self.r)
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}arg ==> {_result}")
        return _result


    def real(self, debug):
        """Real part"""
        if debug.get():
            print(f"{debug.indent()}real({self})")
            print(f"{debug.indent()}real => {self.r}")
        return self.r


    def imag(self, debug):
        """Imaginary part"""
        if debug.get():
            print(f"{debug.indent()}imag({self})")
            print(f"{debug.indent()}imag => {self.i}")
        return self.i


    def dot(self, z, debug):
        """Dot product of self with z."""
        if debug.get():
            print(f"{debug.indent()}dot({self}, {z})")
        _old = debug.inc()
        _result = self.mul(z.conj(debug), debug).real(debug)
        debug.reset(_old)
        if debug.get():
            print(f"{debug.indent()}dot => {_result}")
        return _result


    # Utility

    def __str__(self):
        return "(" + str(self.r) + " + " + str(self.i) + "i)"

def main():
    """Main"""
    debug = Debug(True)
    print(f"debug.get(): {debug.get()}")
    x = Complex(1, 1, debug)
    print("x:", x)
    y = Complex(2, 3, debug)
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
    z = w.ln(debug)
    print("z [ln(-1)]:", z)

if __name__ == '__main__':
    main()
