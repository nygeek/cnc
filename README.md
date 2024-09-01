# stibitz
Complex Number Calculator in honor of the late George Stibitz

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
