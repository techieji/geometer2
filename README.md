# Geometer

Project goal: create a lightweight, powerful, and extendible modal graphics editor
that can generate mathematical vector graphics for LaTeX.

## Architecture

### Figure State

Geometer stores the figure state as a list of shapes. The list of
permissible shapes are:
 - line
 - point
 - bezier curve
 - text
 - arc

Each shape has attributes including:
 - color (default: black)
 - line thickness
 - endcaps

An object is represented as a set of points; a point can either be *definite* or *computed*. Definite points
are manually given by the user. Computed points are a function of one or many shapes, and can represent
intersections and midpoints.

### Language

Geometer can be controlled using a sophisticated Scheme dialect. The list of features unique to Geometer Lisp
are:
 - `'(<x>,<y>)`: a syntax addition to represent a location/point on the screen. This will be represented with a
   builtin type.
 - `(mouse-position)`: return the mouse's position on the screen as a point. If the mouse is locked onto a point,
   this function should return a computed point. Otherwise, this function should return a definite point.
 - `(point <p>)`: return a point shape at the specified point. Note that shapes are represented as a builtin type.
 - `(line <p1> <p2>)`: return a line between the two points
 - `(bezier <p1> <c1> <c2> <p2>)`: return a bezier curve with endpoints `p1` and `p2` and control points `c1` and `c2`.
 - `(text <p> <string>)`: return a text shape the string `string` at point `p`
 - `(arc <center> <p1> <p2>)`: return an arc centered at `center` sweeping from `p1` to `p2`
 - `(add-shape! <shape>)`: adds a shape to the list of shapes.
 - `(delete! <shape>)`: removes the shape from the list of shapes.
 - `(set-attr! <shape> <attrname> <attrvalue>)`: sets the specified attribute name to its respective value on the shape
 - `(intersect <s1> <s2>)`: returns a list of computed points where the two shapes intersect
 - `(distance <p1> <p2>)`: returns a number representing the distance between the two points
 - `(set-mode! <function>)`: sets the mode to `function`; see below for documentation on mode.
 - `(bind <string> <function>)`: when `string` is entered on the keyboard, `function` will be run.
 - `(save! <filename)`: saves the current figure as a PostScript file to `filename`.

All other features common to Scheme should also be implemented. Addition and subtraction should work with
two points, and scalar multiplication should also work on a point.

### Interface

Geometer has a visual WYSIWYG interface. A mode is represented by a function from Geometer Lisp: when the
user is in the `bezier` mode, the interface will prompt the user for each argument depending on its type:
 - if the function expects a point, the interface should use `(mouse-position)` to get the position.
 - if the function expects text, the interface should prompt the user to enter text in the lower left corner of the
   screen.
 - if the function expects a shape, the interface should prompt the user to click on a shape.
**Even if the function does not have all its arguments, an intermediate shape should be rendered as a function
of the current mouse position**. This shape should be grayed out.
There are three special modes:
 - normal mode should enable zooming with pinch-in and pinch-out and panning with control + drag. All keybindings
   should also be enabled. Entering normal mode also deletes all intermediate shapes.
 - command mode allows the user to write a command in the language to be executed. All entered text will be displayed
   in the bottom left corner in the text entry area; any output of the language will also be displayed there. Only
   one input or one output will be displayed in the corner to avoid cluttering up the screen.
 - edit mode should show all definite points and should allow them to be manipulated

Text will be displayed in the bottom left corner like vim. When in a mode, a representative word will be shown,
unless prompting for an argument. When in normal mode, no word will be shown. When in command mode, either
the command being currently entered or the output of the previously executed command will be shown.

The color theme for this project should be minimalist and representative of LaTeX: black lines on a white background.
Shapes may be other colors if their attributes are set to be so.

Keybindings:
 - `<ESC>`: normal mode (works in any mode)
 - `l`: line (only in normal)
 - `b`: bezier (only in normal)
 - `(`: starts command mode (only in normal). Note that the parenthesis is added to the beginning of the command
   to be executed.
 - `d`: delete mode
 - `e`: edit mode

### Saving

Geometer saves its output as a PostScript figure. Any required data to open it up in Geometer again (e.g.
computed points and shapes that use computed points) should be stored as comments in PostScript. This file
should be able to be included as a graphics file in LaTeX; any text including LaTeX commands should **not**
be preprocessed.

## Implementation Details

All types should be marked when clear, and documentation should be minimal and concise. Code should rely on builtins
where they exist. Classes should be created when necessary, and code should be easy to extend. PRIORITIZE
CONCISION and BREVITY by writing general functions that can be applied to multiple specific usecases. Obscure
code can be used.

A pytest test suite should be used for every component that can be tested.
