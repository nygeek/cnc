#!/usr/bin/python3

""" Implementation of Octonion class for the CNC calculator

    Octonions are 8-dimensional hypercomplex numbers (Cayley numbers).

    Octonions extend quaternions but lose associativity:
    (ab)c ≠ a(bc) in general

    Multiplication uses the Cayley-Dickson construction from quaternions.

Started 2026-02-09

SPDX-License-Identifier: MIT
Copyright (C) 2026 NYGeek LLC

"""

import math
from decimal import Decimal


class Octonion:
    """ Class to implement octonions for the CNC calculator """

    def __init__(self, e0, e1=0, e2=0, e3=0, e4=0, e5=0, e6=0, e7=0, backend='float'):
        """
        Initialize an octonion with 8 components

        Args:
            e0-e7: the 8 components
            backend: 'float' for Python float, 'decimal' for Decimal
        """
        self.backend = backend

        if backend == 'decimal':
            self.e0 = Decimal(str(e0)) if not isinstance(e0, Decimal) else e0
            self.e1 = Decimal(str(e1)) if not isinstance(e1, Decimal) else e1
            self.e2 = Decimal(str(e2)) if not isinstance(e2, Decimal) else e2
            self.e3 = Decimal(str(e3)) if not isinstance(e3, Decimal) else e3
            self.e4 = Decimal(str(e4)) if not isinstance(e4, Decimal) else e4
            self.e5 = Decimal(str(e5)) if not isinstance(e5, Decimal) else e5
            self.e6 = Decimal(str(e6)) if not isinstance(e6, Decimal) else e6
            self.e7 = Decimal(str(e7)) if not isinstance(e7, Decimal) else e7
        else:
            self.e0 = float(e0)
            self.e1 = float(e1)
            self.e2 = float(e2)
            self.e3 = float(e3)
            self.e4 = float(e4)
            self.e5 = float(e5)
            self.e6 = float(e6)
            self.e7 = float(e7)

    @property
    def real(self):
        """Return the real (scalar) part"""
        return self.e0

    def get_component(self, i):
        """Get component by index (0-7)"""
        return [self.e0, self.e1, self.e2, self.e3,
                self.e4, self.e5, self.e6, self.e7][i]

    def __add__(self, other):
        """Addition: component-wise"""
        if isinstance(other, Octonion):
            return Octonion(
                self.e0 + other.e0,
                self.e1 + other.e1,
                self.e2 + other.e2,
                self.e3 + other.e3,
                self.e4 + other.e4,
                self.e5 + other.e5,
                self.e6 + other.e6,
                self.e7 + other.e7,
                backend=self.backend
            )
        else:
            # Treat as scalar addition to real part
            return Octonion(
                self.e0 + other,
                self.e1, self.e2, self.e3, self.e4, self.e5, self.e6, self.e7,
                backend=self.backend
            )

    def __radd__(self, other):
        """Right addition"""
        return self.__add__(other)

    def __sub__(self, other):
        """Subtraction: component-wise"""
        if isinstance(other, Octonion):
            return Octonion(
                self.e0 - other.e0,
                self.e1 - other.e1,
                self.e2 - other.e2,
                self.e3 - other.e3,
                self.e4 - other.e4,
                self.e5 - other.e5,
                self.e6 - other.e6,
                self.e7 - other.e7,
                backend=self.backend
            )
        else:
            # Treat as scalar subtraction from real part
            return Octonion(
                self.e0 - other,
                self.e1, self.e2, self.e3, self.e4, self.e5, self.e6, self.e7,
                backend=self.backend
            )

    def __rsub__(self, other):
        """Right subtraction"""
        return Octonion(
            other - self.e0,
            -self.e1, -self.e2, -self.e3, -self.e4, -self.e5, -self.e6, -self.e7,
            backend=self.backend
        )

    def __mul__(self, other):
        """
        Octonion multiplication using Cayley-Dickson construction

        Note: Octonion multiplication is non-associative!
        (a*b)*c may not equal a*(b*c)
        """
        if isinstance(other, Octonion):
            # Use Cayley-Dickson formula
            # Split each octonion into two quaternions
            # o = (a, b) where a and b are quaternions (4D each)
            # (a,b) * (c,d) = (ac - d*b, da + bc*)

            # First octonion as two quaternions
            a0, a1, a2, a3 = self.e0, self.e1, self.e2, self.e3
            b0, b1, b2, b3 = self.e4, self.e5, self.e6, self.e7

            # Second octonion as two quaternions
            c0, c1, c2, c3 = other.e0, other.e1, other.e2, other.e3
            d0, d1, d2, d3 = other.e4, other.e5, other.e6, other.e7

            # ac (quaternion multiplication)
            ac0 = a0*c0 - a1*c1 - a2*c2 - a3*c3
            ac1 = a0*c1 + a1*c0 + a2*c3 - a3*c2
            ac2 = a0*c2 - a1*c3 + a2*c0 + a3*c1
            ac3 = a0*c3 + a1*c2 - a2*c1 + a3*c0

            # d*b (quaternion conjugate of d times b)
            db0 = d0*b0 + d1*b1 + d2*b2 + d3*b3
            db1 = d0*b1 - d1*b0 + d2*b3 - d3*b2
            db2 = d0*b2 - d1*b3 - d2*b0 + d3*b1
            db3 = d0*b3 + d1*b2 - d2*b1 - d3*b0

            # ac - d*b
            r0 = ac0 - db0
            r1 = ac1 - db1
            r2 = ac2 - db2
            r3 = ac3 - db3

            # da (d times a)
            da0 = d0*a0 - d1*a1 - d2*a2 - d3*a3
            da1 = d0*a1 + d1*a0 + d2*a3 - d3*a2
            da2 = d0*a2 - d1*a3 + d2*a0 + d3*a1
            da3 = d0*a3 + d1*a2 - d2*a1 + d3*a0

            # bc* (b times conjugate of c)
            bc0 = b0*c0 + b1*c1 + b2*c2 + b3*c3
            bc1 = b0*c1 - b1*c0 - b2*c3 + b3*c2
            bc2 = b0*c2 + b1*c3 - b2*c0 - b3*c1
            bc3 = b0*c3 - b1*c2 + b2*c1 - b3*c0

            # da + bc*
            r4 = da0 + bc0
            r5 = da1 + bc1
            r6 = da2 + bc2
            r7 = da3 + bc3

            return Octonion(r0, r1, r2, r3, r4, r5, r6, r7, backend=self.backend)
        else:
            # Scalar multiplication
            return Octonion(
                self.e0 * other,
                self.e1 * other,
                self.e2 * other,
                self.e3 * other,
                self.e4 * other,
                self.e5 * other,
                self.e6 * other,
                self.e7 * other,
                backend=self.backend
            )

    def __rmul__(self, other):
        """Right multiplication by scalar"""
        return self.__mul__(other)

    def __neg__(self):
        """Negation"""
        return Octonion(
            -self.e0, -self.e1, -self.e2, -self.e3,
            -self.e4, -self.e5, -self.e6, -self.e7,
            backend=self.backend
        )

    def conjugate(self):
        """Return the conjugate: e0 - e1 - e2 - ... - e7"""
        return Octonion(
            self.e0, -self.e1, -self.e2, -self.e3,
            -self.e4, -self.e5, -self.e6, -self.e7,
            backend=self.backend
        )

    def norm_squared(self):
        """Return the squared norm: sum of squares of all components"""
        return (self.e0 * self.e0 + self.e1 * self.e1 +
                self.e2 * self.e2 + self.e3 * self.e3 +
                self.e4 * self.e4 + self.e5 * self.e5 +
                self.e6 * self.e6 + self.e7 * self.e7)

    def norm(self):
        """Return the norm (magnitude)"""
        if self.backend == 'decimal':
            return self.norm_squared().sqrt()
        else:
            return math.sqrt(self.norm_squared())

    def __abs__(self):
        """Absolute value (norm)"""
        return self.norm()

    def inverse(self):
        """Return the multiplicative inverse: o* / |o|²"""
        norm_sq = self.norm_squared()
        if norm_sq == 0:
            raise ZeroDivisionError("Cannot invert zero octonion")
        conj = self.conjugate()
        return Octonion(
            conj.e0 / norm_sq,
            conj.e1 / norm_sq,
            conj.e2 / norm_sq,
            conj.e3 / norm_sq,
            conj.e4 / norm_sq,
            conj.e5 / norm_sq,
            conj.e6 / norm_sq,
            conj.e7 / norm_sq,
            backend=self.backend
        )

    def __truediv__(self, other):
        """Division: o / p = o * p⁻¹"""
        if isinstance(other, Octonion):
            return self * other.inverse()
        else:
            # Scalar division
            return Octonion(
                self.e0 / other,
                self.e1 / other,
                self.e2 / other,
                self.e3 / other,
                self.e4 / other,
                self.e5 / other,
                self.e6 / other,
                self.e7 / other,
                backend=self.backend
            )

    def __rtruediv__(self, other):
        """Right division: scalar / o"""
        return Octonion(other, 0, 0, 0, 0, 0, 0, 0, backend=self.backend) * self.inverse()

    def normalize(self):
        """Return the unit octonion: o / |o|"""
        n = self.norm()
        if n == 0:
            raise ZeroDivisionError("Cannot normalize zero octonion")
        return self / n

    def __str__(self):
        """String representation"""
        def format_component(val, symbol):
            if self.backend == 'decimal':
                if val == 0:
                    return None
                sign = '+' if val > 0 else ''
                return f"{sign}{val}{symbol}"
            else:
                if val == 0:
                    return None
                sign = '+' if val > 0 else ''
                return f"{sign}{val:.10g}{symbol}"

        parts = []

        # Real part
        if self.backend == 'decimal':
            parts.append(str(self.e0))
        else:
            parts.append(f"{self.e0:.10g}")

        # Imaginary parts
        for i, val in enumerate([self.e1, self.e2, self.e3, self.e4,
                                  self.e5, self.e6, self.e7], 1):
            comp = format_component(val, f'e{i}')
            if comp:
                parts.append(comp)

        result = ''.join(parts)
        # Clean up leading +
        if result.startswith('+'):
            result = result[1:]
        return result

    def __repr__(self):
        """Representation for debugging"""
        return (f"Octonion({self.e0}, {self.e1}, {self.e2}, {self.e3}, "
                f"{self.e4}, {self.e5}, {self.e6}, {self.e7})")

    def __eq__(self, other):
        """Equality comparison"""
        if not isinstance(other, Octonion):
            return False
        return (self.e0 == other.e0 and self.e1 == other.e1 and
                self.e2 == other.e2 and self.e3 == other.e3 and
                self.e4 == other.e4 and self.e5 == other.e5 and
                self.e6 == other.e6 and self.e7 == other.e7)


def main():
    """Simple unit tests"""
    print("Testing Octonion class")

    # Test basic construction
    o1 = Octonion(1, 1, 1, 1, 1, 1, 1, 1)
    print(f"o1 = {o1}")

    o2 = Octonion(2, 1, 0, 0, 1, 0, 0, 0)
    print(f"o2 = {o2}")

    # Test addition
    print(f"o1 + o2 = {o1 + o2}")

    # Test multiplication
    print(f"o1 * o2 = {o1 * o2}")

    # Test non-associativity
    o3 = Octonion(0, 1, 0, 0, 0, 0, 0, 0)  # e1
    o4 = Octonion(0, 0, 1, 0, 0, 0, 0, 0)  # e2
    o5 = Octonion(0, 0, 0, 0, 1, 0, 0, 0)  # e4

    print(f"\nTesting non-associativity:")
    print(f"e1 = {o3}")
    print(f"e2 = {o4}")
    print(f"e4 = {o5}")
    print(f"(e1 * e2) * e4 = {(o3 * o4) * o5}")
    print(f"e1 * (e2 * e4) = {o3 * (o4 * o5)}")

    # Test conjugate and norm
    print(f"\no1* = {o1.conjugate()}")
    print(f"|o1| = {o1.norm()}")

    # Test inverse
    print(f"\no2⁻¹ = {o2.inverse()}")
    print(f"o2 * o2⁻¹ = {o2 * o2.inverse()}")


if __name__ == '__main__':
    main()
