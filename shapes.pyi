from enum import Enum
from typing import Callable

class Point:
    x: float
    y: float
    def __add__(self, other: Point) -> Point: ...
    def __sub__(self, other: Point) -> Point: ...
    def __mul__(self, other: float) -> Point: ...
    def __truediv__(self, other: float) -> Point: ...

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
    start_angle: float
    end_angle: float
    direction: RotationDirection
