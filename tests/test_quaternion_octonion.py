#!/usr/bin/python3

""" Unit tests for Quaternion and Octonion classes

Started 2026-02-09

SPDX-License-Identifier: MIT
Copyright (C) 2026 NYGeek LLC

"""

import sys
from quaternion import Quaternion
from octonion import Octonion


def test_quaternion_basic():
    """Test basic quaternion operations"""
    print("Testing Quaternion basics...")

    q1 = Quaternion(1, 2, 3, 4)
    q2 = Quaternion(2, 1, 0, 1)

    # Test addition
    result = q1 + q2
    assert result.w == 3 and result.x == 3 and result.y == 3 and result.z == 5
    print("  ✓ Addition works")

    # Test subtraction
    result = q1 - q2
    assert result.w == -1 and result.x == 1 and result.y == 3 and result.z == 3
    print("  ✓ Subtraction works")

    # Test multiplication non-commutativity
    r1 = q1 * q2
    r2 = q2 * q1
    assert r1 != r2
    print("  ✓ Multiplication is non-commutative")

    # Test conjugate
    conj = q1.conjugate()
    assert conj.w == 1 and conj.x == -2 and conj.y == -3 and conj.z == -4
    print("  ✓ Conjugate works")

    # Test norm
    norm_sq = q1.norm_squared()
    assert norm_sq == 1 + 4 + 9 + 16  # 30
    print("  ✓ Norm squared works")

    # Test inverse
    inv = q2.inverse()
    identity = q2 * inv
    # Allow for floating point error
    assert abs(identity.w - 1) < 1e-10
    assert abs(identity.x) < 1e-10
    assert abs(identity.y) < 1e-10
    assert abs(identity.z) < 1e-10
    print("  ✓ Inverse works")

    print("All quaternion basic tests passed!\n")


def test_quaternion_basis():
    """Test quaternion basis elements"""
    print("Testing Quaternion basis elements...")

    i = Quaternion(0, 1, 0, 0)
    j = Quaternion(0, 0, 1, 0)
    k = Quaternion(0, 0, 0, 1)

    # Test i² = j² = k² = -1
    assert (i * i).w == -1 and (i * i).x == 0
    assert (j * j).w == -1 and (j * j).y == 0
    assert (k * k).w == -1 and (k * k).z == 0
    print("  ✓ i² = j² = k² = -1")

    # Test ij = k, ji = -k
    ij = i * j
    ji = j * i
    assert ij.z == 1 and ij.w == 0
    assert ji.z == -1 and ji.w == 0
    print("  ✓ ij = k, ji = -k")

    # Test jk = i, kj = -i
    jk = j * k
    kj = k * j
    assert jk.x == 1 and jk.w == 0
    assert kj.x == -1 and kj.w == 0
    print("  ✓ jk = i, kj = -i")

    # Test ki = j, ik = -j
    ki = k * i
    ik = i * k
    assert ki.y == 1 and ki.w == 0
    assert ik.y == -1 and ik.w == 0
    print("  ✓ ki = j, ik = -j")

    # Test ijk = -1
    ijk = (i * j) * k
    assert ijk.w == -1 and ijk.x == 0 and ijk.y == 0 and ijk.z == 0
    print("  ✓ ijk = -1")

    print("All quaternion basis tests passed!\n")


def test_octonion_basic():
    """Test basic octonion operations"""
    print("Testing Octonion basics...")

    o1 = Octonion(1, 1, 1, 1, 1, 1, 1, 1)
    o2 = Octonion(2, 1, 0, 0, 1, 0, 0, 0)

    # Test addition
    result = o1 + o2
    assert result.e0 == 3 and result.e1 == 2
    print("  ✓ Addition works")

    # Test subtraction
    result = o1 - o2
    assert result.e0 == -1 and result.e1 == 0
    print("  ✓ Subtraction works")

    # Test conjugate
    conj = o1.conjugate()
    assert conj.e0 == 1
    for i in range(1, 8):
        assert conj.get_component(i) == -1
    print("  ✓ Conjugate works")

    # Test norm
    norm_sq = o1.norm_squared()
    assert norm_sq == 8  # 1² × 8
    print("  ✓ Norm squared works")

    # Test inverse
    inv = o2.inverse()
    identity = o2 * inv
    # Allow for floating point error
    assert abs(identity.e0 - 1) < 1e-10
    print("  ✓ Inverse works")

    print("All octonion basic tests passed!\n")


def test_octonion_non_associativity():
    """Test octonion non-associativity"""
    print("Testing Octonion non-associativity...")

    e1 = Octonion(0, 1, 0, 0, 0, 0, 0, 0)
    e2 = Octonion(0, 0, 1, 0, 0, 0, 0, 0)
    e4 = Octonion(0, 0, 0, 0, 1, 0, 0, 0)

    # Test (e1 * e2) * e4 ≠ e1 * (e2 * e4)
    left = (e1 * e2) * e4
    right = e1 * (e2 * e4)

    # They should differ (demonstrating non-associativity)
    assert left != right
    print(f"  ✓ (e1*e2)*e4 = {left} ≠ e1*(e2*e4) = {right}")
    print("  ✓ Multiplication is non-associative")

    print("All octonion non-associativity tests passed!\n")


def test_decimal_backend():
    """Test decimal backend for quaternions and octonions"""
    print("Testing Decimal backend...")

    q = Quaternion(1, 2, 3, 4, backend='decimal')
    assert q.backend == 'decimal'
    print("  ✓ Quaternion decimal backend works")

    o = Octonion(1, 1, 1, 1, 1, 1, 1, 1, backend='decimal')
    assert o.backend == 'decimal'
    print("  ✓ Octonion decimal backend works")

    print("All decimal backend tests passed!\n")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Running Quaternion and Octonion Unit Tests")
    print("=" * 60 + "\n")

    try:
        test_quaternion_basic()
        test_quaternion_basis()
        test_octonion_basic()
        test_octonion_non_associativity()
        test_decimal_backend()

        print("=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
