# HP-35 GUI Calculator Architecture

## 1. Introduction and Goals

### 1.1 Requirements Overview
Create a faithful pixel-perfect GUI replica of the 1972 HP-35 calculator using SDL2, with mouse-driven interaction and extended functionality for quaternions and octonions. The GUI must integrate with the existing CNC calculator engine while maintaining visual fidelity to the original HP-35.

See [requirements.md](requirements.md) for complete functional requirements (REQ-1 through REQ-15).

### 1.2 Quality Goals

| Priority | Quality Goal | Motivation |
|----------|--------------|------------|
| 1 | **Visual Fidelity** | Authentic HP-35 appearance is core to user experience |
| 2 | **Functional Correctness** | All calculator operations must work accurately |
| 3 | **Responsiveness** | UI must respond within 100ms to user actions |
| 4 | **Portability** | Must work on macOS and Linux without modification |
| 5 | **Maintainability** | Clean separation between UI and calculator logic |

### 1.3 Stakeholders

| Role | Expectations |
|------|--------------|
| End Users | Authentic HP-35 experience, accurate calculations |
| Project Owner | Integration with existing CNC codebase |
| Developers | Clear architecture, reusable components |

## 2. Constraints

- **Technology**: Must use Python 3.5+ and SDL2 via PySDL2
- **Platform**: macOS and Linux only (not Windows initially)
- **Integration**: Must use existing `ComplexNumberCalculator` and `HP35Stack` classes
- **Input**: Mouse-only (no keyboard support initially)
- **Appearance**: Must match original HP-35 physical design

## 3. System Context

```
┌─────────────────────────────────────────────────┐
│                                                 │
│              Operating System                   │
│         (macOS / Linux)                        │
│                                                 │
│  ┌──────────────┐      ┌──────────────┐       │
│  │              │      │              │       │
│  │  SDL2        │      │  SDL2_gfx    │       │
│  │  Library     │      │  Library     │       │
│  │              │      │              │       │
│  └──────┬───────┘      └──────┬───────┘       │
│         │                     │               │
└─────────┼─────────────────────┼───────────────┘
          │                     │
          └────────┬────────────┘
                   │
          ┌────────▼────────┐
          │                 │
          │   PySDL2        │
          │   Bindings      │
          │                 │
          └────────┬────────┘
                   │
          ┌────────▼────────────────────┐
          │                             │
          │   HP35GUI                   │
          │   (Main GUI Application)    │
          │                             │
          │  ┌─────────────────────┐   │
          │  │ SDL Window & Events │   │
          │  └──────────┬──────────┘   │
          │             │               │
          │  ┌──────────▼──────────┐   │
          │  │  Button Grid        │   │
          │  │  LED Display        │   │
          │  │  Event Handler      │   │
          │  └──────────┬──────────┘   │
          │             │               │
          └─────────────┼───────────────┘
                        │
          ┌─────────────▼────────────────┐
          │                              │
          │  ComplexNumberCalculator     │
          │  (Existing Calculator Logic) │
          │                              │
          │   ┌──────────────────┐      │
          │   │   HP35Stack      │      │
          │   └──────────────────┘      │
          │                              │
          └──────────────────────────────┘
```

### External Interfaces

- **SDL2**: Window management, rendering, event loop
- **SDL2_gfx**: Shape drawing primitives (rectangles, filled polygons)
- **SDL2_ttf**: TrueType font rendering for button labels
- **PySDL2**: Python bindings providing ctypes-based access to SDL
- **Existing CNC**: `cnc.py` (ComplexNumberCalculator), `hp35stack.py` (HP35Stack)

## 4. Solution Strategy

### 4.1 Technology Decisions

| Decision | Rationale |
|----------|-----------|
| **PySDL2** | Pure Python wrapper, no C compilation needed, ctypes-based |
| **SDL2** | Cross-platform, mature, excellent 2D graphics support |
| **Direct rendering** | Draw primitives directly rather than using sprites for flexibility |
| **Single-file GUI** | Keep GUI code in one module for simplicity |
| **Polling event loop** | SDL standard pattern for event handling |

### 4.2 Top-level Decomposition

The system is decomposed into three main layers:

1. **Presentation Layer**: SDL-based GUI (buttons, display, mouse handling)
2. **Application Layer**: Calculator logic (existing CNC code)
3. **Platform Layer**: SDL2 libraries and OS

### 4.3 Achieving Quality Goals

| Quality Goal | Approach |
|--------------|----------|
| Visual Fidelity | Use exact HP-35 measurements, colors from research; seven-segment LED rendering |
| Functional Correctness | Delegate all calculations to proven `ComplexNumberCalculator` class |
| Responsiveness | Single-threaded event loop, immediate display updates after operations |
| Portability | Use platform-independent SDL features only |
| Maintainability | Clear class structure, separation of rendering vs logic |

## 5. Building Block View

### 5.1 Level 1: System Overview

```
┌───────────────────────────────────────────────┐
│          HP35GUICalculator (main)             │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │        GUI Components                   │ │
│  │                                         │ │
│  │  • HP35Window                          │ │
│  │  • ButtonGrid                          │ │
│  │  • LEDDisplay                          │ │
│  │  • EventHandler                        │ │
│  │                                         │ │
│  └────────────┬────────────────────────────┘ │
│               │                               │
│  ┌────────────▼────────────────────────────┐ │
│  │    Calculator Engine (existing)        │ │
│  │                                         │ │
│  │  • ComplexNumberCalculator             │ │
│  │  • HP35Stack                           │ │
│  │                                         │ │
│  └─────────────────────────────────────────┘ │
│                                               │
└───────────────────────────────────────────────┘
```

### 5.2 Level 2: Component Details

#### HP35Window
- **Responsibility**: SDL window lifecycle, main event loop, coordinate rendering
- **Interfaces**:
  - `__init__(width, height)`: Create window
  - `run()`: Main event loop
  - `render()`: Orchestrate rendering of all components
  - `cleanup()`: SDL resource cleanup

#### ButtonGrid
- **Responsibility**: Button layout, rendering, hit detection
- **Data**: List of Button objects with positions, labels, colors, callbacks
- **Interfaces**:
  - `render(surface)`: Draw all buttons
  - `handle_click(x, y)`: Detect which button was clicked
  - `get_button_at(x, y)`: Return button or None
  - `animate_press(button)`: Visual feedback on click

#### Button (data class)
- **Data**:
  - `x, y, width, height`: Position and size
  - `label`: Button text
  - `color`: RGB tuple
  - `callback`: Function to invoke
  - `font_color`: Text color
  - `pressed`: Boolean state

#### LEDDisplay
- **Responsibility**: Seven-segment LED rendering, display state
- **Data**: Current display string, digit positions
- **Interfaces**:
  - `render(surface)`: Draw LED display
  - `update(value)`: Update displayed value
  - `render_seven_segment(surface, x, y, char)`: Draw single character
  - `render_stack(surface, stack)`: Show entire stack

#### EventHandler
- **Responsibility**: Mouse event processing, state management
- **Interfaces**:
  - `handle_event(event)`: Process SDL event
  - `handle_mouse_down(x, y)`: Mouse button press
  - `handle_mouse_up(x, y)`: Mouse button release
  - `handle_mouse_motion(x, y)`: Mouse hover

### 5.3 Calculator Engine Integration

The GUI delegates all calculation logic to existing classes:

```python
# In HP35Window.__init__:
self.calculator = ComplexNumberCalculator(stack_depth=8)

# In button callback:
def on_button_click(self, button_name):
    self.calculator.handle_string(button_name)
    self.led_display.update(self.calculator.stack)
```

## 6. Runtime View

### 6.1 Application Startup

```
┌────────┐      ┌────────────┐     ┌──────────────┐
│  main  │─────>│ Initialize │────>│  Create      │
│        │      │    SDL     │     │  Window      │
└────────┘      └────────────┘     └──────┬───────┘
                                           │
                    ┌──────────────────────┘
                    │
                    ▼
            ┌───────────────┐
            │  Create GUI   │
            │  Components   │
            │               │
            │  • Buttons    │
            │  • Display    │
            │  • Calculator │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │  Enter Event  │
            │     Loop      │
            └───────────────┘
```

### 6.2 User Click Interaction

```
User clicks mouse
        │
        ▼
┌───────────────┐
│ SDL generates │
│ MOUSEBUTTONUP │
│     event     │
└───────┬───────┘
        │
        ▼
┌───────────────────┐
│  EventHandler     │
│  handle_event()   │
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│  ButtonGrid       │
│  get_button_at()  │
└───────┬───────────┘
        │
        ▼
  Button found?
   /         \
  Yes         No
  │            │
  ▼            ▼
┌──────────┐  (ignore)
│ Execute  │
│ callback │
└─────┬────┘
      │
      ▼
┌──────────────────┐
│  Calculator      │
│  handle_string() │
└─────┬────────────┘
      │
      ▼
┌──────────────────┐
│  Stack updated   │
└─────┬────────────┘
      │
      ▼
┌──────────────────┐
│  LEDDisplay      │
│  update()        │
└─────┬────────────┘
      │
      ▼
┌──────────────────┐
│  render()        │
│  on next frame   │
└──────────────────┘
```

### 6.3 Display Update Cycle

```
Event Loop (60 FPS)
        │
        ▼
┌───────────────┐
│ Handle Events │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Clear Surface │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Render Buttons│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Render Display│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ SDL_Present() │
└───────┬───────┘
        │
        ▼
    (repeat)
```

## 7. Deployment View

```
┌─────────────────────────────────────┐
│     User's Computer                 │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Python 3.5+ Runtime         │  │
│  │                              │  │
│  │  ┌────────────────────────┐ │  │
│  │  │  PySDL2 Package       │ │  │
│  │  │  • cnc_gui.py         │ │  │
│  │  │  • cnc.py             │ │  │
│  │  │  • hp35stack.py       │ │  │
│  │  │  • (other modules)    │ │  │
│  │  └────────────────────────┘ │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  System Libraries            │  │
│  │  • libSDL2.so / .dylib      │  │
│  │  • libSDL2_gfx.so / .dylib  │  │
│  │  • libSDL2_ttf.so / .dylib  │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Installation**:
- SDL2 libraries installed via package manager (Homebrew/apt)
- PySDL2 installed via pip
- CNC calculator installed in development mode (`pip install -e .`)

## 8. Cross-cutting Concepts

### 8.1 Seven-Segment LED Rendering

Each digit is rendered as a seven-segment display:

```
   ╔═══╗      Segments:
   ║ A ║        A
╔══╣   ╠══╗    F B
║ F║   ║ B║     G
╠══╩═══╩══╣    E C
║ E║ G ║ C║     D
╠══╣   ╠══╣
║  ╚═══╝  ║
   ║ D ║
   ╚═══╝
```

- Each segment maps to a polygon or thick line
- Active segments: bright red (#FF0000)
- Inactive segments: very dim red (#200000) for ghost effect

### 8.2 Color Palette

```python
COLORS = {
    'CASE_BLACK': (20, 20, 20),
    'DISPLAY_BG': (10, 10, 10),
    'LED_ON': (255, 0, 0),
    'LED_OFF': (32, 0, 0),
    'TAN': (210, 180, 140),
    'BLUE': (50, 100, 200),
    'BLACK_KEY': (30, 30, 30),
    'WHITE_TEXT': (255, 255, 255),
    'BLACK_TEXT': (0, 0, 0),
}
```

### 8.3 Button Layout Grid

- Window size: 600×1080 pixels (maintains ~1.8:1 aspect ratio)
- Display area: top 200 pixels
- Button area: remaining 880 pixels
- 7-8 rows of buttons (5 original rows + 2-3 extended rows)
- Button spacing: 10 pixels between buttons
- Button size: ~70×70 pixels (varies by row)

### 8.4 Error Handling

- SDL initialization failures: Print error and exit gracefully
- Calculator errors: Display "ERROR" in LED display
- Mouse outside button: No action
- Invalid operations: Delegate to calculator error handling

### 8.5 Coordinate Systems

- SDL uses top-left origin (0,0)
- Y increases downward
- All coordinates in pixels
- Button positions calculated relative to window size

## 9. Architecture Decisions

### ADR-1: Use PySDL2 instead of Pygame

**Context**: Need Python GUI library for graphics
**Decision**: Use PySDL2
**Rationale**:
- Pure Python (no C compilation)
- Direct SDL2 access (more control than Pygame)
- Actively maintained
- Better cross-platform support

**Consequences**:
- (+) More flexible than Pygame
- (+) Better documentation for SDL2 features
- (-) Less "batteries included" than Pygame
- (-) Need to manage SDL resources manually

### ADR-2: Single GUI File Architecture

**Context**: Need to organize GUI code
**Decision**: Implement GUI in single `cnc_gui.py` file
**Rationale**:
- GUI is relatively small (~500-800 lines)
- All components tightly coupled
- Easier to understand as single unit
- No need for complex module structure

**Consequences**:
- (+) Simple to navigate
- (+) No import complexity
- (-) May need refactoring if > 1000 lines
- (-) All classes in one namespace

### ADR-3: Direct Calculator Integration

**Context**: How to integrate with existing calculator
**Decision**: Instantiate `ComplexNumberCalculator` directly in GUI
**Rationale**:
- Simplest approach
- No need for adapters or facades
- Calculator already has string-based API

**Consequences**:
- (+) Minimal code
- (+) Leverages existing tested logic
- (-) GUI tied to specific calculator class
- (-) Limited flexibility for alternate calculators

### ADR-4: Custom Seven-Segment Rendering

**Context**: How to render LED display
**Decision**: Draw seven-segment digits using SDL primitives
**Rationale**:
- Full control over appearance
- Can achieve authentic LED look
- No external font files needed
- Can add glow effects

**Consequences**:
- (+) Authentic appearance
- (+) Customizable
- (-) More complex than text rendering
- (-) Must implement digit mapping

### ADR-5: Mouse-Only Input Initially

**Context**: Support mouse and/or keyboard
**Decision**: Mouse-only for MVP
**Rationale**:
- Matches tactile calculator experience
- Simpler to implement
- Keyboard support can be added later

**Consequences**:
- (+) Faster MVP delivery
- (+) Authentic experience
- (-) Less convenient for power users
- (-) Keyboard mapping needed later

## 10. Quality and Performance

### Performance Requirements
- Frame rate: 60 FPS target
- Click response: < 100ms from click to display update
- Startup time: < 2 seconds

### Memory Requirements
- Estimated memory: < 50 MB (SDL + Python + calculator)
- No dynamic allocation in render loop

### Scalability
- Fixed window size (no dynamic scaling initially)
- Stack depth: 8 registers (configurable)

## 11. Risks and Technical Debt

| Risk | Mitigation |
|------|------------|
| SDL dependency complex | Provide clear setup instructions in Makefile |
| Seven-segment rendering complex | Start with simple implementation, refine iteratively |
| Button layout tedious | Calculate positions programmatically |
| Color matching difficult | Use color picker on HP-35 images |

| Technical Debt | Priority |
|----------------|----------|
| No keyboard support | Low (can add later) |
| Fixed window size | Low (resizing complex) |
| No configuration file | Low (hardcode acceptable) |
| Limited error messages | Medium (improve UX) |

## 12. Glossary

- **HP-35**: First handheld scientific calculator by HP (1972)
- **RPN**: Reverse Polish Notation, stack-based input method
- **Seven-segment**: LED/LCD display with 7 segments per digit
- **PySDL2**: Python bindings for SDL2
- **SDL2**: Simple DirectMedia Layer 2, cross-platform graphics library
- **Quaternion**: 4D hypercomplex number
- **Octonion**: 8D hypercomplex number
