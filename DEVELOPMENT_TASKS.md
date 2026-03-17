# Geometer Development Tasks

This file contains a granular sequence of tasks for implementing the Geometer specification.

---

## Phase 1: Core Data Structures & Type System

### 1.1 Point System
- [ ] Create `geometer/types/point.py` with `Point` base class
- [ ] Implement `DefinitePoint` subclass with x, y coordinates
- [ ] Implement `ComputedPoint` subclass with reference to calculation function
- [ ] Add `__eq__`, `__repr__` methods to Point classes

### 1.2 Shape Classes
- [ ] Create `geometer/shapes/shape.py` with `Shape` base class
- [ ] Add attributes: color (default: black), line_thickness, endcaps
- [ ] Create `geometer/shapes/point_shape.py` with `PointShape` class
- [ ] Create `geometer/shapes/line.py` with `Line` class
- [ ] Create `geometer/shapes/bezier.py` with `BezierCurve` class
- [ ] Create `geometer/shapes/text.py` with `Text` class
- [ ] Create `geometer/shapes/arc.py` with `Arc` class
- [ ] Add `__repr__` methods to all shape classes

### 1.3 Figure State
- [ ] Create `geometer/figure.py` with `Figure` class
- [ ] Implement `add_shape(shape)` method
- [ ] Implement `remove_shape(shape)` method
- [ ] Implement `get_shapes()` method returning list
- [ ] Implement `clear()` method

### 1.4 Shape Factory (Optional Enhancement)
- [ ] Create `geometer/shapes/factory.py` with shape creation helpers
- [ ] Add validation for shape parameters

---

## Phase 2: Geometer Lisp Interpreter

### 2.1 Lexer
- [ ] Create `geometer/lisp/lexer.py`
- [ ] Implement tokenization of Scheme syntax
- [ ] Handle point syntax `'(<x>,<y>)'`
- [ ] Handle strings, numbers, symbols, parentheses

### 2.2 Parser
- [ ] Create `geometer/lisp/parser.py`
- [ ] Implement S-expression parsing
- [ ] Build AST nodes for: atoms, lists, quoted expressions
- [ ] Handle point literal parsing

### 2.3 Evaluator - Core
- [ ] Create `geometer/lisp/environment.py` for variable bindings
- [ ] Create `geometer/lisp/evaluator.py`
- [ ] Implement `eval` function for atoms and lists
- [ ] Implement special forms: quote, if, define, lambda, let
- [ ] Implement function application

### 2.4 Built-in Functions - Shapes
- [ ] Implement `(point <p>)` - create point shape
- [ ] Implement `(line <p1> <p2>)` - create line
- [ ] Implement `(bezier <p1> <c1> <c2> <p2>)` - create bezier
- [ ] Implement `(text <p> <string>)` - create text
- [ ] Implement `(arc <center> <p1> <p2>)` - create arc

### 2.5 Built-in Functions - Figure Operations
- [ ] Implement `(add-shape! <shape>)`
- [ ] Implement `(delete! <shape>)`
- [ ] Implement `(set-attr! <shape> <attrname> <attrvalue>)`

### 2.6 Built-in Functions - Math & Geometry
- [ ] Implement `(intersect <s1> <s2>)` - return list of computed points
- [ ] Implement `(distance <p1> <p2>)` - return float
- [ ] Implement point addition (two points)
- [ ] Implement point subtraction (two points)
- [ ] Implement scalar multiplication (number * point)

### 2.7 Built-in Functions - System
- [ ] Implement `(mouse-position)` - placeholder for UI integration
- [ ] Implement `(set-mode! <function>)` - mode switching
- [ ] Implement `(bind <string> <function>)` - keybinding
- [ ] Implement `(save! <filename>)` - PostScript export

### 2.8 Interpreter Integration
- [ ] Create `geometer/lisp/__init__.py` for package exports
- [ ] Create `geometer/lisp/interpreter.py` as main entry point
- [ ] Add REPL for testing

---

## Phase 3: Rendering Engine

### 3.1 Canvas/Renderer Setup
- [ ] Create `geometer/renderer/__init__.py`
- [ ] Create `geometer/renderer/renderer.py`
- [ ] Set up window using pygame or similar library
- [ ] Implement basic draw loop

### 3.2 Shape Drawing
- [ ] Implement draw method for `Line`
- [ ] Implement draw method for `BezierCurve`
- [ ] Implement draw method for `Text`
- [ ] Implement draw method for `Arc`
- [ ] Implement draw method for `PointShape`
- [ ] Handle color attribute in all shapes
- [ ] Handle line_thickness attribute in all shapes
- [ ] Handle endcaps attribute in all shapes

### 3.3 Computed Point Resolution
- [ ] Create `geometer/geometry/intersections.py`
- [ ] Implement line-line intersection
- [ ] Implement line-arc intersection
- [ ] Implement arc-arc intersection
- [ ] Create `geometer/geometry/midpoint.py` for midpoint calculation
- [ ] Implement computed point evaluation (resolve to definite points)

### 3.4 Intermediate Shape Rendering
- [ ] Add `is_intermediate` flag to Shape base class
- [ ] Implement gray color for intermediate shapes
- [ ] Update renderer to handle intermediate shapes
- [ ] Connect mouse position to intermediate shape preview

---

## Phase 4: Mode System & UI

### 4.1 Mode Architecture
- [ ] Create `geometer/modes/__init__.py`
- [ ] Create `geometer/modes/mode.py` with Mode base class
- [ ] Create `geometer/modes/normal_mode.py`
- [ ] Create `geometer/modes/command_mode.py`
- [ ] Create `geometer/modes/edit_mode.py`

### 4.2 Function-Specific Modes
- [ ] Create `geometer/modes/line_mode.py`
- [ ] Create `geometer/modes/bezier_mode.py`
- [ ] Create `geometer/modes/delete_mode.py`

### 4.3 Mode Manager
- [ ] Create `geometer/modes/manager.py`
- [ ] Implement mode switching logic
- [ ] Handle ESC key for returning to normal mode

### 4.4 Argument Prompting System
- [ ] Create `geometer/modes/prompter.py`
- [ ] Detect expected argument type from function signature
- [ ] Route mouse input for point arguments
- [ ] Route keyboard input for text arguments
- [ ] Route shape click for shape arguments

### 4.5 UI Elements
- [ ] Create `geometer/ui/status_bar.py`
- [ ] Display mode name in bottom left
- [ ] Display command input in command mode
- [ ] Display function output in command mode
- [ ] Implement vim-like text display behavior

---

## Phase 5: Keybindings & Interaction

### 5.1 Core Keybindings
- [ ] Bind `<ESC>` to normal mode (clear intermediates)
- [ ] Bind `l` to line mode (normal mode only)
- [ ] Bind `b` to bezier mode (normal mode only)
- [ ] Bind `(` to command mode (normal mode only, prepend parenthesis)
- [ ] Bind `d` to delete mode (normal mode only)
- [ ] Bind `e` to edit mode (normal mode only)

### 5.2 Normal Mode - Mouse
- [ ] Implement pinch-in zoom
- [ ] Implement pinch-out zoom
- [ ] Implement ctrl+drag panning

### 5.3 Edit Mode Implementation
- [ ] Display all definite points visually
- [ ] Allow dragging definite points
- [ ] Update all shapes referencing moved points

### 5.4 Delete Mode Implementation
- [ ] Allow clicking shapes to delete
- [ ] Remove shape from figure on click

---

## Phase 6: Save/Load System

### 6.1 PostScript Export
- [ ] Create `geometer/export/postscript.py`
- [ ] Convert Line to PS commands
- [ ] Convert BezierCurve to PS commands
- [ ] Convert Text to PS commands
- [ ] Convert Arc to PS commands
- [ ] Convert PointShape to PS commands
- [ ] Handle color in PS output
- [ ] Handle line thickness in PS output

### 6.2 Metadata Recovery
- [ ] Add computed points as PS comments
- [ ] Add shape relationships as PS comments
- [ ] Create `geometer/export/loader.py` to parse PS comments
- [ ] Implement figure state reconstruction from PS

---

## Phase 7: Testing

### 7.1 Core Tests
- [ ] Create `tests/test_point.py` - test DefinitePoint and ComputedPoint
- [ ] Create `tests/test_shapes.py` - test all shape classes

### 7.2 Interpreter Tests
- [ ] Create `tests/test_lexer.py` - test tokenization
- [ ] Create `tests/test_parser.py` - test parsing
- [ ] Create `tests/test_evaluator.py` - test evaluation
- [ ] Create `tests/test_builtins.py` - test built-in functions

### 7.3 Geometry Tests
- [ ] Create `tests/test_intersections.py` - test intersection algorithms
- [ ] Create `tests/test_geometry.py` - test midpoint and other calculations

### 7.4 Integration Tests
- [ ] Create `tests/test_figure.py` - test figure state management
- [ ] Create `tests/test_modes.py` - test mode switching

### 7.5 Export Tests
- [ ] Create `tests/test_postscript.py` - test PS generation

---

## Project Structure

