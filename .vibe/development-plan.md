# Development Plan: cnc (main branch)

*Generated on 2026-02-09 by Vibe Feature MCP*
*Workflow: [epcc](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/epcc)*

## Goal
Add support for quaternions (4D hypercomplex numbers) and octonions (8D hypercomplex numbers) to the Complex Number Calculator, extending the existing complex number operations to these higher-dimensional number systems.

## Explore
<!-- beads-phase-id: cnc-1.1 -->
### Tasks

*Tasks managed via `bd` CLI*

## Plan
<!-- beads-phase-id: cnc-1.2 -->
### Phase Entrance Criteria:
- [ ] Existing codebase architecture is understood (complex number handling, stack operations, button dispatch)
- [ ] Quaternion and octonion mathematics are researched and documented
- [ ] Alternatives for implementation approach have been evaluated
- [ ] Integration points with existing code are identified
- [ ] Scope is clearly defined (which operations to support)

### Tasks

*Tasks managed via `bd` CLI*

## Code
<!-- beads-phase-id: cnc-1.3 -->
### Phase Entrance Criteria:
- [ ] Implementation plan is documented and approved
- [ ] Data structures for quaternions and octonions are designed
- [ ] API/interface design is complete
- [ ] Required operations and their behavior are specified
- [ ] Testing approach is defined

### Tasks

*Tasks managed via `bd` CLI*

## Commit
<!-- beads-phase-id: cnc-1.4 -->
### Phase Entrance Criteria:
- [ ] All code is implemented and working
- [ ] Code follows existing project style and conventions
- [ ] Basic testing has been performed
- [ ] Documentation is updated (README, help text)
- [ ] No breaking changes to existing complex number functionality

### Tasks

*Tasks managed via `bd` CLI*

## Key Decisions
*Important decisions will be documented here as they are made*

### Decision: Stack Architecture ✅ DECIDED (REVISED)
**Initial Choice:** Option B - Mode-Based Stack
**Final Choice:** Option A - Unified Stack (user requested change during implementation)

Calculator uses unified stack where complex numbers, quaternions, and octonions can coexist on the same stack. Operations work polymorphically based on operand types. No mode switching needed.

**Implementation:** Quaternion and Octonion classes implement full operator overloading. Stack operations work with any type. Removed mode system after initial implementation.

### Decision: Implementation Priority ✅ DECIDED
**Chosen:** Option B - Both Together

Implement quaternions and octonions simultaneously since the implementation patterns are similar. Create both `quaternion.py` and `octonion.py` in the same development cycle.

## Implementation Strategy

### Phase 1: Core Number Classes (P0 - No dependencies)
**Files:** `quaternion.py`, `octonion.py`

**Quaternion Class:**
```python
class Quaternion:
    def __init__(self, w, x, y, z, backend='float')  # backend: 'float' or 'decimal'
    def __add__, __sub__, __mul__, __truediv__
    def __neg__, __abs__, __str__, __repr__
    def conjugate()  # w - xi - yj - zk
    def norm()  # sqrt(w² + x² + y² + z²)
    def inverse()  # conjugate / norm²
    def normalize()  # self / norm
    @property real, i, j, k  # component accessors
```

**Octonion Class:** Similar structure, 8 components (e0-e7), Cayley-Dickson multiplication table

### Phase 2: Unified Stack Implementation (P1 - Depends on Phase 1)
**Files:** `cnc.py`, `cnc10.py`

No mode system needed. Operations work polymorphically:
- Stack accepts any type (complex, Quaternion, Octonion)
- Operator overloading handles mixed-type operations
- Tokenizer recognizes all input formats automatically

### Phase 3: Input Parsing (P1 - Depends on Phase 2)
**Files:** `cnc.py`, `cnc10.py` (tokenizer)

Update `TOKEN_PATTERNS` priority order:
1. OCTONION: `\({NUM}(,{NUM}){7}\)` → 8 components
2. QUATERNION: `\({NUM}(,{NUM}){3}\)` → 4 components
3. COMPLEX: `\({NUM},{NUM}\)` → 2 components
4. NUMBER: `{NUM}` → 1 component

In `handle_string`, parse based on current mode and pattern match.

### Phase 4: Operations & Display (P2 - Depends on Phase 1-2)
**Files:** `cnc.py`, `cnc10.py`, `hp35stack.py`

New buttons:
- `j`, `k`: push quaternion basis elements
- `e0`-`e7`: push octonion basis elements
- `conj`: conjugate (works for all types)

Operations by mode:
- **Complex**: all existing operations work
- **Quaternion**: +, -, *, /, abs, inv, exp, log, sqrt, conj
- **Octonion**: +, -, *, /, abs, inv, conj (no transcendentals)

Stack display already polymorphic via `__str__` method.

### Phase 5: Documentation & Testing (P3 - Depends on Phase 1-4)
Update README.md, help text, create test files.

## Implementation Summary

**Completed Features:**
1. ✅ Quaternion class (quaternion.py) - Full arithmetic, conjugate, norm, inverse
2. ✅ Octonion class (octonion.py) - Full arithmetic, handles non-associativity
3. ✅ Unified stack architecture - All types coexist freely
4. ✅ Extended tokenizer - Recognizes (w,x,y,z) and (e0,...,e7) formats
5. ✅ New buttons - j, k, e0-e7, conj
6. ✅ Both float and Decimal backends supported
7. ✅ Comprehensive test suite - All tests passing
8. ✅ Updated documentation - README reflects unified stack

**Files Created:**
- quaternion.py (4D hypercomplex numbers)
- octonion.py (8D hypercomplex numbers)
- test_quaternion_octonion.py (unit tests)

**Files Modified:**
- cnc.py (added imports, buttons, methods)
- cnc10.py (added imports, buttons, methods)
- cli_cnc.py (minor prompt update)
- README.md (comprehensive documentation)

**Key Architectural Decisions:**
- Unified stack instead of mode-based (user preference)
- Polymorphic operations via operator overloading
- Basis elements accessible via simple buttons (j, k, e0-e7)

## Notes
*Additional context and observations*

### Architecture Understanding

**Current Implementation:**
- Polymorphic calculator: binary (IEEE 754 via cmath) and decimal (via decimal.py + cmath10)
- HP35Stack class: configurable depth (default 8), handles push/pop/rolldown/exch/sto/rcl
- ComplexNumberCalculator class: button dispatch table, tokenizer, operation handlers
- Operations classified as: nullary (constants), unary (1 operand), binary (2 operands)
- Complex numbers entered as `(real,imag)` notation
- Tokenizer patterns: COMPLEX, NUMBER, OPERATOR, ALPHA

**Integration Points for Quaternions/Octonions:**
1. **Stack class**: Currently stores Python complex or cmath10.complex - needs to support quaternion/octonion types
2. **Tokenizer**: Need new patterns for quaternion `(w,x,y,z)` and octonion `(e0,e1,e2,e3,e4,e5,e6,e7)` input
3. **Button dispatch**: Most operations can reuse existing unary/binary handlers if quaternion/octonion classes implement proper operator overloading
4. **Display**: `__str__` method in stack needs to handle new types
5. **Type switching**: Need mechanism to switch between complex/quaternion/octonion modes

**Key Considerations:**
- Quaternion multiplication is non-commutative (xy ≠ yx)
- Octonion multiplication is non-associative ((xy)z ≠ x(yz))
- Not all complex operations make sense for quaternions/octonions (e.g., arg/phase)
- Need to decide: separate modes or unified stack?

### Quaternion Mathematics

**Definition:** q = w + xi + yj + zk where i² = j² = k² = ijk = -1

**Properties:**
- 4-dimensional hypercomplex numbers
- Non-commutative: ij = k, ji = -k; jk = i, kj = -i; ki = j, ik = -j
- Useful for 3D rotations, physics, computer graphics

**Operations to Support:**
1. **Basic arithmetic:** ✓ addition, subtraction, multiplication, division (via conjugate)
2. **Conjugate:** q* = w - xi - yj - zk
3. **Norm/Absolute value:** |q| = sqrt(w² + x² + y² + z²)
4. **Inverse:** q⁻¹ = q* / |q|²
5. **Exp/Log:** Quaternion exponential and logarithm (extend from complex)
6. **Powers:** q^n using exp/log
7. **Normalization:** q/|q| for unit quaternions
8. **Extract components:** real part, i-component, j-component, k-component

**Operations NOT to Support:**
- arg/phase (ambiguous for quaternions)
- Trigonometric functions (no natural extension)
- Comparison operators (no natural ordering)

**Input format:** `(w,x,y,z)` where w=scalar, x=i-coeff, y=j-coeff, z=k-coeff

### Octonion Mathematics

**Definition:** o = e₀ + e₁i₁ + e₂i₂ + ... + e₇i₇ (8-dimensional)

**Properties:**
- 8-dimensional hypercomplex numbers (Cayley numbers)
- Non-commutative AND non-associative: (ab)c ≠ a(bc) in general
- Last normed division algebra (Hurwitz's theorem)
- Used in exceptional structures, string theory, but less common in applications

**Operations to Support:**
1. **Basic arithmetic:** ✓ addition, subtraction, multiplication (with care!), division
2. **Conjugate:** o* = e₀ - e₁i₁ - e₂i₂ - ... - e₇i₇
3. **Norm/Absolute value:** |o| = sqrt(e₀² + e₁² + ... + e₇²)
4. **Inverse:** o⁻¹ = o* / |o|²
5. **Extract components:** 8 component accessors

**Operations to AVOID:**
- Exp/Log (complicated due to non-associativity)
- Powers beyond n=2 (ambiguous without associativity)
- Most transcendental functions

**Warning:** Non-associativity means expressions like `x y z *` are ambiguous. Will need to be careful with binary operations on stack.

**Input format:** `(e0,e1,e2,e3,e4,e5,e6,e7)` - 8 components

### Detailed Integration Plan

**1. Create New Number Classes:**
- `quaternion.py`: Quaternion class with operator overloading (+, -, *, /, abs, conjugate, etc.)
- `octonion.py`: Octonion class with operator overloading (more limited)
- Both should work with both binary (float) and decimal modes

**2. Extend Tokenizer:**
- Current: `\({NUM}\s*,\s*{NUM}\)` for complex (2 components)
- Add: `\({NUM}\s*,\s*{NUM}\s*,\s*{NUM}\s*,\s*{NUM}\)` for quaternion (4 components)
- Add: `\({NUM}(,{NUM}){7}\)` for octonion (8 components)
- Pattern priority: try octonion → quaternion → complex → number

**3. Update HP35Stack:**
- Already polymorphic (takes math_mod parameter)
- Should work with quaternion/octonion if they have proper `__str__`
- No changes needed!

**4. Add New Buttons:**
- `quat` or `Q`: convert top 4 stack elements to quaternion
- `oct` or `O`: convert top 8 stack elements to octonion
- `conj`: conjugate (works for complex, quaternion, octonion)
- `i`, `j`, `k`: push quaternion basis elements
- `components`: extract components back to stack

**5. Modify Existing Buttons:**
- Most unary/binary operations work if quaternion/octonion implement them
- Disable: arg, asin, acos, atan, asinh, acosh, atanh for quaternions/octonions
- Keep: abs, exp, log, sqrt, inv, chs, +, -, *, /, xtoy

**6. Mode System (DECISION NEEDED):**
- **Option A:** Unified stack - mix complex/quaternion/octonion freely
- **Option B:** Mode flag - switch calculator between C/Q/O modes
- **Recommendation:** Option A (unified) - more flexible, matches "hypercomplex calculator" vision

### Scope Definition

**IN SCOPE (Phase 1):**
1. Quaternion class with full arithmetic (+, -, *, /, conjugate, norm, inverse)
2. Octonion class with basic arithmetic (+, -, *, /, conjugate, norm, inverse)
3. Direct input: `(w,x,y,z)` for quaternions, `(e0,...,e7)` for octonions
4. Basis element buttons: `j`, `k` (quaternion), `e0`-`e7` (octonion basis)
5. Operations that work: abs, inv, chs, +, -, *, /, sqrt, exp, log (quaternions only)
6. Both binary and decimal modes support
7. Updated help text and README documentation

**OUT OF SCOPE (for now):**
1. Trigonometric functions for quaternions/octonions
2. Spherical linear interpolation (SLERP) for quaternions
3. Octonion exp/log (too complex due to non-associativity)
4. Graphical visualization of rotations
5. Conversion between Euler angles and quaternions
6. Split-complex numbers, dual numbers, other algebras

**OPEN QUESTIONS (need user input):**
1. Should we use unified stack or mode switching?
2. Button naming: verbose (`quat`, `conj`) or terse (`q`, `c`)?
3. Priority: quaternions first, or implement both together?

---
*This plan is maintained by the LLM and uses beads CLI for task management. Tool responses provide guidance on which bd commands to use for task management.*
