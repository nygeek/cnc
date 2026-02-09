#!/usr/bin/python3

""" Implementation of Quaternion class for the CNC calculator

    Quaternions are 4-dimensional hypercomplex numbers of the form:
    q = w + xi + yj + zk

    where i² = j² = k² = ijk = -1

    Quaternion multiplication is non-commutative:
    ij = k, ji = -k
    jk = i, kj = -i
    ki = j, ik = -j

Started 2026-02-09

SPDX-License-Identifier: MIT
Copyright (C) 2026 NYGeek LLC

"""

import math
from decimal import Decimal


class Quaternion:
    """ Class to implement quaternions for the CNC calculator """

    def __init__(self, w, x=0, y=0, z=0, backend='float'):
        """
        Initialize a quaternion: q = w + xi + yj + zk

        Args:
            w: scalar (real) component
            x: i component
            y: j component
            z: k component
            backend: 'float' for Python float, 'decimal' for Decimal
        """
        self.backend = backend

        if backend == 'decimal':
            self.w = Decimal(str(w)) if not isinstance(w, Decimal) else w
            self.x = Decimal(str(x)) if not isinstance(x, Decimal) else x
            self.y = Decimal(str(y)) if not isinstance(y, Decimal) else y
            self.z = Decimal(str(z)) if not isinstance(z, Decimal) else z
        else:
            self.w = float(w)
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

    @property
    def real(self):
        """Return the real (scalar) part"""
        return self.w

    @property
    def i(self):
        """Return the i component"""
        return self.x

    @property
    def j(self):
        """Return the j component"""
        return self.y

    @property
    def k(self):
        """Return the k component"""
        return self.z

    def __add__(self, other):
        """Addition: component-wise"""
        if isinstance(other, Quaternion):
            return Quaternion(
                self.w + other.w,
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
                backend=self.backend
            )
        else:
            # Treat as scalar addition to real part
            return Quaternion(
                self.w + other,
                self.x,
                self.y,
                self.z,
                backend=self.backend
            )

    def __radd__(self, other):
        """Right addition"""
        return self.__add__(other)

    def __sub__(self, other):
        """Subtraction: component-wise"""
        if isinstance(other, Quaternion):
            return Quaternion(
                self.w - other.w,
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
                backend=self.backend
            )
        else:
            # Treat as scalar subtraction from real part
            return Quaternion(
                self.w - other,
                self.x,
                self.y,
                self.z,
                backend=self.backend
            )

    def __rsub__(self, other):
        """Right subtraction"""
        return Quaternion(
            other - self.w,
            -self.x,
            -self.y,
            -self.z,
            backend=self.backend
        )

    def __mul__(self, other):
        """
        Quaternion multiplication (non-commutative!)

        Using the rules:
        i² = j² = k² = ijk = -1
        ij = k, ji = -k
        jk = i, kj = -i
        ki = j, ik = -j
        """
        if isinstance(other, Quaternion):
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z, backend=self.backend)
        else:
            # Scalar multiplication
            return Quaternion(
                self.w * other,
                self.x * other,
                self.y * other,
                self.z * other,
                backend=self.backend
            )

    def __rmul__(self, other):
        """Right multiplication by scalar"""
        return self.__mul__(other)

    def __neg__(self):
        """Negation"""
        return Quaternion(-self.w, -self.x, -self.y, -self.z, backend=self.backend)

    def conjugate(self):
        """Return the conjugate: w - xi - yj - zk"""
        return Quaternion(self.w, -self.x, -self.y, -self.z, backend=self.backend)

    def norm_squared(self):
        """Return the squared norm: w² + x² + y² + z²"""
        return self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z

    def norm(self):
        """Return the norm (magnitude): sqrt(w² + x² + y² + z²)"""
        if self.backend == 'decimal':
            return self.norm_squared().sqrt()
        else:
            return math.sqrt(self.norm_squared())

    def __abs__(self):
        """Absolute value (norm)"""
        return self.norm()

    def inverse(self):
        """Return the multiplicative inverse: q* / |q|²"""
        norm_sq = self.norm_squared()
        if norm_sq == 0:
            raise ZeroDivisionError("Cannot invert zero quaternion")
        conj = self.conjugate()
        return Quaternion(
            conj.w / norm_sq,
            conj.x / norm_sq,
            conj.y / norm_sq,
            conj.z / norm_sq,
            backend=self.backend
        )

    def __truediv__(self, other):
        """Division: q / p = q * p⁻¹"""
        if isinstance(other, Quaternion):
            return self * other.inverse()
        else:
            # Scalar division
            return Quaternion(
                self.w / other,
                self.x / other,
                self.y / other,
                self.z / other,
                backend=self.backend
            )

    def __rtruediv__(self, other):
        """Right division: scalar / q"""
        return Quaternion(other, 0, 0, 0, backend=self.backend) * self.inverse()

    def normalize(self):
        """Return the unit quaternion: q / |q|"""
        n = self.norm()
        if n == 0:
            raise ZeroDivisionError("Cannot normalize zero quaternion")
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
            parts.append(str(self.w))
        else:
            parts.append(f"{self.w:.10g}")

        # Imaginary parts
        for val, sym in [(self.x, 'i'), (self.y, 'j'), (self.z, 'k')]:
            comp = format_component(val, sym)
            if comp:
                parts.append(comp)

        result = ''.join(parts)
        # Clean up leading +
        if result.startswith('+'):
            result = result[1:]
        return result

    def __repr__(self):
        """Representation for debugging"""
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        """Equality comparison"""
        if not isinstance(other, Quaternion):
            return False
        return (self.w == other.w and self.x == other.x and
                self.y == other.y and self.z == other.z)


def main():
    """Simple unit tests"""
    print("Testing Quaternion class")

    # Test basic construction
    q1 = Quaternion(1, 2, 3, 4)
    print(f"q1 = {q1}")

    q2 = Quaternion(2, 1, 0, 1)
    print(f"q2 = {q2}")

    # Test addition
    print(f"q1 + q2 = {q1 + q2}")

    # Test multiplication (non-commutative)
    print(f"q1 * q2 = {q1 * q2}")
    print(f"q2 * q1 = {q2 * q1}")

    # Test conjugate and norm
    print(f"q1* = {q1.conjugate()}")
    print(f"|q1| = {q1.norm()}")

    # Test inverse
    print(f"q1⁻¹ = {q1.inverse()}")
    print(f"q1 * q1⁻¹ = {q1 * q1.inverse()}")

    # Test basis elements
    i = Quaternion(0, 1, 0, 0)
    j = Quaternion(0, 0, 1, 0)
    k = Quaternion(0, 0, 0, 1)

    print(f"\nBasis elements:")
    print(f"i² = {i * i}")
    print(f"j² = {j * j}")
    print(f"k² = {k * k}")
    print(f"ij = {i * j}")
    print(f"ji = {j * i}")
    print(f"jk = {j * k}")
    print(f"kj = {k * j}")
    print(f"ki = {k * i}")
    print(f"ik = {i * k}")
    print(f"ijk = {i * j * k}")


if __name__ == '__main__':
    main()
