from __future__ import annotations
import uuid
from typing import List, Optional, Tuple, Any

class Point:
    """Represents a point in 2D space, which can be definite or computed."""
    def __init__(self, x: float, y: float, computed: bool = False, dependencies: Optional[List['Shape']] = None):
        self.x = x
        self.y = y
        self.computed = computed
        # dependencies are other Shapes that this computed point relies on
        self.dependencies: List[Shape] = dependencies if dependencies is not None else []

    def __add__(self, other: Point) -> Point:
        if not isinstance(other, Point):
            return NotImplemented
        computed = self.computed or other.computed
        # Use a set to merge dependencies and remove duplicates
        merged_dependencies = list(set(self.dependencies + other.dependencies))
        return Point(self.x + other.x, self.y + other.y, computed=computed, dependencies=merged_dependencies)

    def __sub__(self, other: Point) -> Point:
        if not isinstance(other, Point):
            return NotImplemented
        computed = self.computed or other.computed
        merged_dependencies = list(set(self.dependencies + other.dependencies))
        return Point(self.x - other.x, self.y - other.y, computed=computed, dependencies=merged_dependencies)

    def __mul__(self, scalar: float) -> Point:
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        # If the original point is computed, the scaled point is also computed
        return Point(self.x * scalar, self.y * scalar, computed=self.computed, dependencies=self.dependencies)

    def __rmul__(self, scalar: float) -> Point:
        return self.__mul__(scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        # Comparing computed status is crucial for identity
        return self.x == other.x and self.y == other.y and self.computed == other.computed

    def __hash__(self) -> int:
        # Hash must be consistent with __eq__
        return hash((self.x, self.y, self.computed))

    def __repr__(self) -> str:
        status = "computed" if self.computed else "definite"
        return f"Point({self.x}, {self.y}, {status})"

    def distance(self, other: Point) -> float:
        """Calculates the Euclidean distance to another point."""
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5


class Shape:
    """Base class for all geometric shapes."""
    def __init__(self, color: Tuple[int, int, int] = (0, 0, 0), line_thickness: int = 1, endcaps: Optional[str] = None):
        self._id = uuid.uuid4()
        self.color = color
        self.line_thickness = line_thickness
        self.endcaps = endcaps

    @property
    def id(self) -> uuid.UUID:
        return self._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id.hex[:8]}, color={self.color})"


class PointShape(Shape):
    """A shape representing a single point."""
    def __init__(self, point: Point, **kwargs):
        super().__init__(**kwargs)
        self.point = point

    def __repr__(self) -> str:
        return f"PointShape(id={self.id.hex[:8]}, point={self.point})"


class Line(Shape):
    """A line segment between two points."""
    def __init__(self, p1: Point, p2: Point, **kwargs):
        super().__init__(**kwargs)
        self.p1 = p1
        self.p2 = p2

    def __repr__(self) -> str:
        return f"Line(id={self.id.hex[:8]}, p1={self.p1}, p2={self.p2})"


class Bezier(Shape):
    """A Bezier curve defined by two endpoints and two control points."""
    def __init__(self, p1: Point, c1: Point, c2: Point, p2: Point, **kwargs):
        super().__init__(**kwargs)
        self.p1 = p1
        self.c1 = c1
        self.c2 = c2
        self.p2 = p2

    def __repr__(self) -> str:
        return f"Bezier(id={self.id.hex[:8]}, p1={self.p1}, c1={self.c1}, c2={self.c2}, p2={self.p2})"


class Text(Shape):
    """A text string placed at a specific point."""
    def __init__(self, point: Point, text_content: str, **kwargs):
        super().__init__(**kwargs)
        self.point = point
        self.text_content = text_content

    def __repr__(self) -> str:
        return f"Text(id={self.id.hex[:8]}, point={self.point}, text='{self.text_content}')"


class Arc(Shape):
    """An arc defined by a center point and two sweep points."""
    def __init__(self, center: Point, p1: Point, p2: Point, **kwargs):
        super().__init__(**kwargs)
        self.center = center
        self.p1 = p1
        self.p2 = p2

    def __repr__(self) -> str:
        return f"Arc(id={self.id.hex[:8]}, center={self.center}, p1={self.p1}, p2={self.p2})"
