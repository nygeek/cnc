# CNC

Complex Number Calculator in honor of the late George Stibitz and
the 1972 HP35 scientific calculator.

## About

The HP35 calculator was introduced by Hewlett Packard in the fall
of 1972.  It was the first scientific calculator in a pocket sized
form factor.  While it was expensive, $395 in 1972, its price was
only about five times that of a contemporary high-end slide rule.

The HP35 calculator had four primary registers arranged in a stack.
The four registers were called X, Y, Z, and T.  In addition there
was a memory register called M.  Our implementation of the HP35
stack has eight elements rather than four.  The bottom four are
shown as X, Y, Z, and T, but the rest are simply shown by their
index.

The bottom register, called X, was always displayed on the HP35.
The CNC shell displays the entire stack and the M register every
time the enter key is pressed.

Pressing enter would push the number in X up to Y, Y up to Z, and
Z up to T.  When this was done the value in T was lost.

Roll down, shown on the keyboard with the letter R and a down arrow,
would move T to Z, Z to Y, Y to X, and X around to T.  We call this
'down'.

STO would take the value in X and save it in M.  RCL would replace
the value in X with the value from M.

A unary function, say sqrt,  would replace the value of X with the
result of the function.

A binary function would operate on X and Y.  The result would be
left in X and the values above in the stack would be pulled down:
Z to Y, T to Z.  The value in T would remain, so after any binary
operation the T and Z registers would hold the same value.

The EEX (Enter Exponent) button on the original HP35 operated
completely outside the stack logic of the calculator.  If you were
in the midst of entering a number digit-by-digit you could press
the EEX button and could type digits into the exponent.  You could
set the sign of the exponent if you chose.  Our EEX implementation,
however, uses the integer part of the real number in X and creates
a number 10^(int(X.real)) in X and then multiplies Y by that number.

So, entering a number in scientific notation, say 6.022E23 would
be something like this:

   6.022 23 eex

### George Stibitz

[George Stibitz](https://en.wikipedia.org/wiki/George_Stibitz)
built a complex number calculator at Bell Labs (CNC) in 1939.  He
used a modified teletype to send commands over telegraph lines to
the CNC in New York for a demonstration at Dartmouth College in
1940.  This was the first telecomputing application.

### CNC characteristics

Out-of-the box the CNC calculator creates an eight-element stack
instead of the original HP35's four.  The four extra elements
are imaginatively numbered 4, 5, 6, and 7.  The idiosyncratic
behavior of the original HP35 T register (duplicating to the
register below it on any operation consuming an element of the
stack) is now that of element 7.

An enterprising user may edit the source code of cnc and change the
size of the stack to any particular value they like.  Best of luck.

This, the original CNC calculator, uses the math and cmath modules,
which rely in turn on the underlying floating point hardware of your
machine.  Modern machines almost always do their arithemtic using the
[IEEE 754](https://en.wikipedia.org/wiki/IEEE_754) standard.

Because we enter and display our numbers in decimal but do our
calculations in binary, there are often small differences resulting
from the conversion process.  To manage that we have added the
"clamp" machinery.  When pushing a number onto the stack we check
the real and imaginary parts against the closest integer.  If the
difference between a component and a nearby integer is smaller than
the clamp value, which defaults to 1E-10, then we round that component
to the closest integer.  You may examine the clamp value with the
getclamp button and set it using the setclamp button.  Note that we
do *not* clamp numbers to zero, just non-zero integers.

### CNC10 characteristics

This variant of cnc uses the long decimal arithmetic provided in
the [decimal.py](https://docs.python.org/3/library/decimal.html) module.

The decimal.py module handles arbitrary length numbers and does all
of its operations in decimal.  However, decimal.py only offers a very
limted number of mathematical functions.  In order to support the
scientific calculator scope I have created a Math10.py module that
augments decimal.py with most of the machinery offered in the base
math.py module that comes with the base Python.  And in order to
support the complex manipulations that were the original objective
of creating this calculator I created a CMath10.py module that
implements most of the cmath.py functionality, but in arbitrary
length decimal form.

As of 2026-01-13 this is incomplete.  Worse yet, there are some
tricky issues associated with the underlying mathematics that will
need deeper study to make sure that I'm doing it right.

### Debug tracing

The debug machinery is implemented using the Python trace hooks,
thus triggering a callout to a trace function on each method entry
and exit.

### Known bugs

The original HP35 did all of its work in decimal.  The largest
number it could represent was 9.999999999E99, or 10 to the 100.
This calculator does whatever the underlying Python engine supports,
presumably the IEEE 754 standard that most CPUs provide these days.

As a consequence the base ten logarithm of the overflow value was
100, a behavior that enabled a number of entertaining tricks with
the calculator back in the day.

### CNC functions

1. "?"
    * display this documentation
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
1. eex
    * push 10^x * y onto the stack (Enter Exponent)
1. enter
    * display the stack
1. exch
    * exchange x and y
1. exp
    * replace x with e^x
1. down
    * t to z, z to y, y to x, x to z
1. getclamp
    * push the clamp threshold onto the stack
1. help
    * display documentation
1. i
    * push i on to the stack
1. imag
    * push the imaginary part of x onto the stack
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
1. real
    * push the real part of x onto the stack
1. rcl
    * replace x with the value in M
1. setclamp
    * set the clamp threshold to the value in x
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

### Installing

Get the CMath10 and Math10 modules:
```
> cd ~/projects/c
> git clone https://github.com/nygeek/cmath10.git
```

*Of course, you may put the module anywhere you like.  I show it in ~/projects/c for ease in explaining.*

Get the DebugTrace module:
```
> cd ~/projects/t
> git clone https://github.com/nygeek/tracedebug.git
```

Get this module:
1. ```> cd ~/projects/c```
1. ```> git clone https://github.com/nygeek/cnc.git```
1. ```> cd ./cnc```
1. ```> python -m venv .venv```
1. ```> direnv allow```  
*If you are not using [direnv](https://direnv.net/) you can skip this step and instead run
```> source .venv/bin/activate``` each time you cd into the directory.*  
1. ```> pip install -e ~/projects/c/cmath10```
1. ```> pip install -e ~/projects/t/tracedebug```

## Metadata

Memo to: File

From: **Marc Donner**

Contact: **marc@nygeek.net**

Subject: **Complex Calculator**

Start Date: **2024-08-17**

Status: **WORKING**
