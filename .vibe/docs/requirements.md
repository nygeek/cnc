# HP-35 GUI Calculator Requirements

## Project Overview
Create a faithful pixel-perfect GUI replica of the 1972 HP-35 calculator using SDL, with mouse-driven interaction and extended functionality for quaternions and octonions.

## Stakeholders
- **End Users**: Scientists, engineers, calculator enthusiasts wanting an authentic HP-35 experience
- **Technical Team**: Development team implementing SDL graphics
- **Project Owner**: Marc Donner (NYGeek LLC)

## Success Criteria
- Visual fidelity matches original HP-35 appearance (colors, proportions, button shapes)
- All original HP-35 calculator operations work correctly via mouse input
- Extended quaternion/octonion operations are accessible via additional buttons
- Application builds and runs on both macOS and Linux
- LED display recreates the authentic 1970s red LED appearance

## Constraints
- Must use SDL portable graphics library
- Must integrate with existing CNC calculator logic (cnc.py, hp35stack.py)
- Must maintain RPN calculation semantics
- Build system must provide clear SDL dependency installation instructions

---

## REQ-1: Physical Dimensions and Proportions

**User Story:** As a calculator enthusiast, I want the GUI to match the original HP-35's proportions so that it feels like using the real calculator.

**Acceptance Criteria:**
- The GUI calculator SHALL maintain the aspect ratio of 5.8" × 3.2" (width:height ≈ 1.8:1)
- The display SHALL occupy approximately the top 20% of the calculator height
- The button area SHALL occupy approximately the bottom 75% of the calculator height
- WHEN the window is resizable, the system SHALL maintain the original aspect ratio

## REQ-2: Color Scheme and Visual Styling

**User Story:** As a user, I want the calculator to look like the original HP-35 so that I get an authentic vintage experience.

**Acceptance Criteria:**
- The calculator case SHALL be rendered in black
- Digit keys (0-9, decimal, π) SHALL be rendered in tan/beige color
- Function keys (ENTER, CHS, EEX, CLx, CLR, +, -, ×, ÷) SHALL be rendered in blue
- Scientific function keys SHALL be rendered in black with white lettering
- The display background SHALL be black with red LED-style digits

## REQ-3: LED Display Rendering

**User Story:** As a user, I want an authentic LED display appearance so that it recreates the 1970s calculator experience.

**Acceptance Criteria:**
- The display SHALL render numbers in red color (#FF0000 or similar LED red)
- The display SHALL use seven-segment LED-style digit rendering
- The display SHALL show 15 digit positions (10-digit mantissa + sign + decimal + 2-digit exponent + sign)
- WHEN a digit is active, the system SHALL show illuminated red segments
- WHEN a digit is inactive, the system SHALL show dim or dark segments
- The display SHALL render with a slight glow effect to simulate LED behavior

## REQ-4: Button Layout - Original HP-35 Keys

**User Story:** As a user, I want the button layout to match the original HP-35 so that I can use muscle memory from the original calculator.

**Acceptance Criteria:**
- The calculator SHALL have 35 buttons matching the original HP-35 layout
- The bottom row SHALL contain: digit keys 7, 8, 9, and ÷
- The layout SHALL follow the original HP-35 keyboard arrangement in 5 rows
- Button labels SHALL match the original HP-35 nomenclature
- The ENTER key SHALL be wider than other keys
- Buttons SHALL be grouped by function with visual separation

## REQ-5: Extended Buttons for Quaternion/Octonion Operations

**User Story:** As a user doing hypercomplex mathematics, I want access to quaternion and octonion operations so that I can use the extended calculator functionality.

**Acceptance Criteria:**
- The calculator SHALL include buttons for: j, k (quaternion basis elements)
- The calculator SHALL include buttons for: e0, e1, e2, e3, e4, e5, e6, e7 (octonion basis elements)
- The calculator SHALL include a button for conjugate operation (conj)
- Extended buttons SHALL be visually distinct from original HP-35 buttons
- Extended buttons SHALL be positioned logically (grouped near related functions)
- The calculator SHALL be slightly larger than the original HP-35 to accommodate extra buttons

## REQ-6: Mouse Input Handling

**User Story:** As a user, I want to click buttons with my mouse so that I can perform calculations interactively.

**Acceptance Criteria:**
- WHEN the user clicks on a button, the system SHALL trigger the corresponding calculator operation
- WHEN the user hovers over a button, the system SHALL provide visual feedback (highlight, color change)
- WHEN the user clicks a button, the system SHALL provide visual feedback (button press animation)
- WHEN the user releases the mouse button, the system SHALL execute the button's function
- The system SHALL detect mouse clicks within button boundaries with pixel precision

## REQ-7: Calculator Functional Integration

**User Story:** As a user, I want all calculator operations to work correctly so that I can perform calculations.

**Acceptance Criteria:**
- The GUI SHALL integrate with the existing ComplexNumberCalculator class
- The GUI SHALL integrate with the existing HP35Stack class
- WHEN a button is clicked, the system SHALL call the appropriate calculator method
- The display SHALL update immediately after each operation
- The system SHALL support all operations from the CLI version: arithmetic (+, -, *, /), trigonometric (sin, cos, tan, asin, acos, atan), logarithmic (ln, log, exp), hyperbolic (sinh, cosh, tanh, asinh, acosh, atanh), stack operations (enter, down, exch, clr, clx), memory operations (sto, rcl), constants (pi, e, i), and power operations (sqrt, inv, xtoy)

## REQ-8: Number Entry via Mouse

**User Story:** As a user, I want to enter numbers by clicking digit buttons so that I can input operands for calculations.

**Acceptance Criteria:**
- WHEN the user clicks digit buttons (0-9), the system SHALL build up the current number in the display
- WHEN the user clicks the decimal point button, the system SHALL add a decimal point to the current number
- WHEN the user clicks EEX, the system SHALL allow entering an exponent
- WHEN the user clicks ENTER, the system SHALL push the current number onto the stack
- The system SHALL support entering complex numbers, quaternions, and octonions via parenthesis notation
- IF the user enters invalid input, the system SHALL provide error feedback

## REQ-9: SDL Library Integration

**User Story:** As a developer, I want to use SDL for graphics so that the application is portable across platforms.

**Acceptance Criteria:**
- The application SHALL use SDL2 for window management and rendering
- The application SHALL use SDL2_ttf for text rendering (if needed for labels)
- The application SHALL use SDL2 drawing primitives for shapes and graphics
- The application SHALL handle SDL events for mouse input
- The application SHALL properly initialize and cleanup SDL resources

## REQ-10: Build System - Setup Target

**User Story:** As a user installing the calculator, I want clear instructions for installing SDL dependencies so that I can build the application.

**Acceptance Criteria:**
- The Makefile SHALL include a "setup" target
- WHEN the user runs "make setup" on macOS, the system SHALL display instructions for installing SDL via Homebrew
- WHEN the user runs "make setup" on Linux, the system SHALL display instructions for installing SDL via apt/yum/dnf
- The setup target SHALL detect the operating system and show appropriate instructions
- The instructions SHALL list all required SDL packages: SDL2, SDL2_ttf (if needed)

## REQ-11: Cross-Platform Compatibility

**User Story:** As a user on different platforms, I want the calculator to work on both macOS and Linux so that I can use it regardless of my OS.

**Acceptance Criteria:**
- The application SHALL compile and run on macOS (Darwin)
- The application SHALL compile and run on Linux distributions
- The application SHALL use conditional compilation for platform-specific code (if needed)
- The Makefile SHALL support building on both macOS and Linux
- The application SHALL use platform-independent SDL features

## REQ-12: Window Management

**User Story:** As a user, I want a properly sized window so that the calculator is usable and looks correct.

**Acceptance Criteria:**
- The application SHALL create an SDL window on startup
- The window SHALL have an appropriate default size (e.g., 600x800 pixels maintaining 1.8:1 aspect ratio)
- The window SHALL have a title "CNC - HP-35 Calculator" or similar
- The window SHALL remain open until the user closes it or clicks a quit button
- The window SHALL handle standard OS window controls (minimize, close)

## REQ-13: Display Update and Refresh

**User Story:** As a user, I want the display to update smoothly so that I can see calculation results immediately.

**Acceptance Criteria:**
- The display SHALL update within 100ms of any button click
- The system SHALL use a reasonable frame rate (30-60 FPS) for smooth animations
- The display SHALL show the entire stack (X, Y, Z, T registers at minimum)
- The display SHALL show the M register (memory)
- The display SHALL clear old values when new calculations are performed

## REQ-14: Error Handling and User Feedback

**User Story:** As a user, I want to see error messages so that I understand when something goes wrong.

**Acceptance Criteria:**
- IF the user performs an invalid operation (e.g., division by zero), the system SHALL display an error message
- IF the calculator encounters an overflow, the system SHALL display an appropriate error
- Error messages SHALL be displayed in the LED display area
- Errors SHALL be dismissable (e.g., by clicking CLx or CLR)

## REQ-15: Application Lifecycle

**User Story:** As a user, I want to be able to start and stop the calculator cleanly so that it behaves like a normal application.

**Acceptance Criteria:**
- The application SHALL start with an empty stack
- The application SHALL initialize SDL properly on startup
- WHEN the user closes the window, the application SHALL clean up SDL resources and exit cleanly
- The application SHALL handle quit events from the OS gracefully
- The application SHALL not leave orphaned processes or resources on exit

---

## Out of Scope (for initial release)
- Keyboard input (mouse only initially)
- Touchscreen support
- Saving/loading calculator state
- Skins or themes (only original HP-35 appearance)
- Sound effects (click sounds)
- Resizable buttons/window (fixed size initially)
- Windows platform support (macOS and Linux only)

## References
- [HP-35 Wikipedia](https://en.wikipedia.org/wiki/HP-35)
- [HP Museum HP-35 Page](https://www.hpmuseum.org/hp35.htm)
- [Vintage Calculators - HP-35](http://www.vintagecalculators.com/html/the_hp-35_calculator.html)
- [Smithsonian HP-35](https://americanhistory.si.edu/collections/object/nmah_334321)
- [HP-35 Engineering Milestone](https://ethw.org/Milestones:Development_of_the_HP-35,_the_First_Handheld_Scientific_Calculator,_1972)
