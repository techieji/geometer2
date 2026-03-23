from typing import NamedTuple, Callable, Any, Iterable
from enum import Enum

### Goes in shapes.py #####

class Point(NamedTuple):
    x: float
    y: float

class ConstrainedPoint:
    constraint: Callable[[], Point]

class Shape:
    color: str
    thickness: float
    endcaps: str

    def midpoint(self) -> ConstrainedPoint: ...

class Line(Shape):
    start: Point
    end: Point

class Bezier(Shape):
    # Cubic bezier curve
    start: Point
    control1: Point
    control2: Point
    end: Point

class Dot(Shape):
    place: Point

class Text(Shape):
    place: Point
    text: str

class RotationDirection(Enum):
    CLOCKWISE = -1
    COUNTERCLOCKWISE = 1

class Arc(Shape):
    center: Point
    radius: float
    start_angle: float    # radians
    end_angle: float
    direction: RotationDirection

### Goes in language.py #####

class TokenType(Enum):
    NUMBER = 0
    STRING = 1
    ATOM = 2
    BOOLEAN = 3
    CHARACTER = 4        # represents parentheses, quotes, unquote, quasiquotes, etc.

class Token:
    kind: TokenType
    value: Any

class ParseTree:
    is_literal: bool
    value: Token | list[ParseTree]
    # value is of type Token if is_literal is true; otherwise, it is a list of ParseTrees.

type Environment = ChainMap

def make_global_environment() -> Environment: ...

def lex(program: str) -> Iterable[Token]: ...
def parse(tokens: Iterable[Token]) -> ParseTree: ...
def execute(parse_tree: ParseTree, environment: Environment) -> Token: ...      # Returns a literal
