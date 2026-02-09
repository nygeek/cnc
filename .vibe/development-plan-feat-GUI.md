# Development Plan: cnc (feat/GUI branch)

*Generated on 2026-02-09 by Vibe Feature MCP*
*Workflow: [waterfall](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/waterfall)*

## Goal
Create a faithful pixel-perfect GUI replica of the HP-35 calculator using SDL graphics library, with mouse-driven interaction, authentic LED display, and extended buttons for quaternion/octonion operations

## Requirements
<!-- beads-phase-id: cnc-3.1 -->
### Tasks

*Tasks managed via `bd` CLI*

## Design
<!-- beads-phase-id: cnc-3.2 -->

### Phase Entrance Criteria:
- [x] HP-35 physical specifications researched and documented (dimensions, colors, button layout, LED display characteristics)
- [x] All functional requirements defined in requirements.md
- [x] SDL library capabilities and modules needed are identified
- [x] Extended functionality (quaternion/octonion buttons) requirements are clear
- [x] User interaction patterns (mouse-driven) are specified
- [x] Scope is clearly defined (what's in/out)

### Tasks

*Tasks managed via `bd` CLI*

## Implementation
<!-- beads-phase-id: cnc-3.3 -->

### Phase Entrance Criteria:
- [x] Complete architecture documented in architecture.md
- [x] Detailed design documented in design.md
- [x] SDL integration approach defined
- [x] UI component structure and rendering pipeline designed
- [x] Button layout and coordinate mapping specified
- [x] LED display rendering approach designed
- [x] Event handling (mouse clicks) architecture defined
- [x] Integration with existing calculator logic planned

### Tasks

*Tasks managed via `bd` CLI*

## Qa
<!-- beads-phase-id: cnc-3.4 -->

### Phase Entrance Criteria:
- [ ] All GUI components implemented
- [ ] SDL integration complete
- [ ] Mouse event handling working
- [ ] Display rendering functional
- [ ] Calculator logic integrated with GUI
- [ ] Build system updated with SDL dependencies
- [ ] Code compiles without errors

### Tasks

*Tasks managed via `bd` CLI*

## Testing
<!-- beads-phase-id: cnc-3.5 -->

### Phase Entrance Criteria:
- [ ] Code review completed
- [ ] Static analysis (pylint) passed
- [ ] All identified bugs and issues fixed
- [ ] Visual fidelity verified against HP-35 reference materials
- [ ] Code quality standards met

### Tasks

*Tasks managed via `bd` CLI*

## Finalize
<!-- beads-phase-id: cnc-3.6 -->

### Phase Entrance Criteria:
- [ ] All test cases executed and passed
- [ ] Functional testing complete (all calculator operations work via GUI)
- [ ] Visual fidelity testing complete (matches HP-35 appearance)
- [ ] User acceptance testing complete
- [ ] Performance is acceptable
- [ ] No critical bugs remain

### Tasks

*Tasks managed via `bd` CLI*

## Key Decisions

### Requirements Phase Decisions
- **Graphics Library**: SDL2 chosen for cross-platform portability (macOS/Linux)
- **Python Bindings**: PySDL2 for pure Python SDL2 wrapper using ctypes
- **SDL Modules Needed**:
  - SDL2 (core): window management, rendering, event handling
  - SDL2_gfx: shape rendering primitives (rectangles, circles, lines)
  - SDL2_ttf: TrueType font rendering for button labels
- **Display Technology**: Seven-segment LED rendering to match original HP-35 aesthetics
- **Color Scheme**: Black case, tan digit keys, blue function keys, black scientific keys (per original HP-35)
- **Physical Dimensions**: Maintain 1.8:1 aspect ratio (5.8" × 3.2" original proportions)
- **Extended Functionality**: Add 12 extra buttons for quaternion/octonion operations (j, k, e0-e7, conj)
- **Input Method**: Mouse-only initially (keyboard input deferred to future release)
- **Integration Approach**: Integrate with existing ComplexNumberCalculator and HP35Stack classes
- **Setup Target**: Makefile will provide OS-specific SDL installation instructions

### Design Phase Decisions
- **Window Size**: 600×1080 pixels (maintains HP-35 aspect ratio)
- **Button Count**: 47 total buttons (35 original HP-35 + 12 extended)
- **Button Layout**: 11 rows with precise pixel coordinates documented
- **LED Display**: Custom seven-segment rendering with exact segment polygon definitions
- **Color Palette**: Exact RGB values specified for all colors (tan, blue, black keys, purple quaternion, orange octonion)
- **Event Handling**: State machine with IDLE → HOVERING → PRESSING states
- **Rendering Pipeline**: 60 FPS target with SDL double buffering
- **Display Format**: 15-character LED display (mantissa + exponent)
- **Calculator Integration**: Direct instantiation of ComplexNumberCalculator with callback architecture

## Notes

### Design Document Completed (2026-02-09)
Created comprehensive detailed design document at `/Users/jordanh/Src/cnc/.vibe/docs/design.md` with:
- Complete button layout with exact pixel coordinates for all 47 buttons
- Seven-segment LED rendering algorithm with segment definitions and character mapping
- Display layout with 15-digit LED format and stack register positions
- Event handling state machine with mouse interaction flow
- Exact RGB color specifications for all button types and display elements
- Complete data structures (Button, ButtonGrid, LEDDisplay classes)
- Integration architecture with existing calculator engine
- Implementation-ready specifications with no ambiguity

### Implementation Completed (2026-02-09)
Successfully implemented complete HP-35 GUI calculator at `/Users/jordanh/Src/cnc/cnc_gui.py`:
- **911 lines** of clean, well-documented Python code
- **All 47 buttons** with exact layout: 35 original HP-35 + 12 extended (quaternion/octonion)
- **Seven-segment LED display** with custom polygon-based rendering
- **Event handling** with complete state machine (IDLE → HOVERING → PRESSING)
- **Calculator integration** with ComplexNumberCalculator via direct instantiation
- **Color-coded buttons**: TAN (digits), BLUE (functions), BLACK_KEY (scientific), PURPLE (quaternion), ORANGE (octonion)
- **Mouse interactions**: Hover effects, press effects, proper hit detection
- **Error handling**: Division by zero, overflow, graceful exceptions
- **Makefile updated** with setup target providing OS-conditional SDL installation instructions
- **GUI target added** to Makefile for easy launching (`make gui`)
- **Syntax verified**: Python compilation successful, ready to run after SDL installation

---
*This plan is maintained by the LLM and uses beads CLI for task management. Tool responses provide guidance on which bd commands to use for task management.*
