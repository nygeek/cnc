# CNC
Complex Number Calculator in honor of the late George Stibitz

## 2024-08-28 and 2024-09-01

All of the HP35 functionality except 'E EX' (enter exponent for
scientific notation) are working. The original HP35 did all of its
work in decimal.  The largest number it could represent was
9.999999999E99, or 10 to the 100.  This calculator does whatever
the underlying Python engine supports, presumably the IEEE 754
standard that most CPUs provide these days.

The HP35 calculator had four primary registers arranged in a stack.
The four registers were called X, Y, Z, and T.  In addition there
was a memory register called M.

The bottom register, called X, was always displayed.

Pressing enter would push the number in X up to Y, Y up to Z, and
Z up to T.  When this was done the value in T was lost.

Roll down, shown on the keyboard with the letter R and a down arrow,
would move t to z, z to y, y to x, and x around to t.

STO would take the value in save it in M.  RCL would replace the
value in X with the value stored in M.

A unary function would replace the value of X with the result of
the function.

A binary function would operate on X and Y.  The result would be
left in X and the values above in the stack would be pulled down:
Z to Y, T to Z.  The value in T would remain, so after any binary
function the T and Z registers would hold the same value.

### Known bugs

1.  The number recognizer doesn't understand a '-' prefix.  (This
is actually like the HP35 ... to enter a negative number you had
to enter the positive number and then press CHS.)

### CNC functions

1. "-"
    * subtract x from y
1. "/"
    * divide y by x
1. "*"
    * multiply y by x
1. "+"
    * add x and y
1. arccos
    * replace x with arccos(x)
1. arcsin
    * replace x with arcsin(x)
1. arctan
    * replace x with arctan(x)
1. arg
    * replace x with arg(x)
1. chs
    * reverse the sign of x
1. clr
    * clear the stack
1. clx
    * clear the x register
1. cos
    * replace x with cos(x)
1. debug
    * toggle the debug flag
1. e
    * push e onto the stack
1. enter
    * display the stack
1. exch
    * exchange x and y
1. exp
    * replace x with e^x
1. down
    * t to z, z to y, y to x, x to z
1. help
    * display documentation
1. i
    * push i on to the stack
1. inv
    * replace x with put 1/x
1. ln
    * replace x with ln(x)
1. mod
    * replace x with mod(x)
1. pi
    * push pi onto the stack
1. push
    * push everything up the stack
1. quit
    * exit the calculator
1. rcl
    * replace x with the value in M
1. sin
    * replace x with sin(x)
1. sqrt
    * replace x with sqrt(x)
1. sto
    * store x into M
1. tan
    * replace x with tan(x)
1. xtoy
    * put x^y in x, removing both x and y

## 2024-08-18

I have the cnc.py class functioning nicely.  It has a set of little tests in the main() function at the bottom.  It has a _debug flag that is used also as an indentation control for the debug output.  Each time a method calls another method it uses one more than the debug flag that it received and it prefixes all of its debug output with "  " * the debug flag so that the debug output is easier to read.

### Method list as of today:

#### Complex results
1. add(self, addend):
   * return self + addend
1. sub(self, diminuend):
   * return self - diminuend
1. mul(self, multiplicand):
   * return self * multiplicand
1. conj(self):
   * return complex conjugate of self (a+bi) => (a-bi)
1. inv(self):
   * return 1/self
1. div(self, divisor):
   * return self / divisor
1. exp(self):
   * return e^self
1. log(self)
   * return log(self)
#### Real results
1. mod_squared(self):
   * return self.dot(self)
1. mod(self):
   * return length(self) == **[self.dot(self)]**
1. real(self):
   * return realpart of self
1. imag(self):
   * return imagpart of self
1. dot(self, z):
   * return self.mul(z.conj()).real()
   
## 2024-08-17

Why call this calculator **stibitz**?

[George Stibitz](https://en.wikipedia.org/wiki/George_Stibitz/) built a complex number calculator at Bell Labs (CNC) in 1939.  He used a modified teletype to send commands over telegraph lines to the CNC in New York.

Here are some design notes:

First of all, the complex calculator will operate purely on complex numbers (a + bi).

The first set of operators will be:

*x* in **C**: *(a + bi)*

*y* in **C**: *(d + ei)*

*a, b, d, e* in **R**

* complex(a, b) ⇒ x == (a + bi)
* sum(x, y) ⇒ (x+y) == (a + d, (b + e)i)
* diff(x, y) ⇒ (x - y) == (a - d, (b - e)i)
* mul(x, y) ⇒ (x * y) == (ad - be, (ae + bd)i)
* inv(x) ⇒ (1 / x) == a / (a^2 + b^2) - bi / (a^2 + b^2)
* div(x, y) ⇒ x * inv(y)
* conj(x) ⇒ (a, -bi)
* mod(x) ⇒ sqrt(mul(x, conj(x))) [in R]
* real(x) ⇒ (a, 0)
* img(x) ⇒ (0, b)

Question: should real(x) and img(x) return elements of R instead of C?

Python design pattern: each operator will return element of C so
that we can chain the results.

So: complex(real(x), img(x)) == x

---
## Metadata

Memo to: File

From: **Marc Donner**

Contact: **marc@nygeek.net**

Subject: **Complex Calculator**

Start Date: **2024-08-17**

Status: **WORKING**
