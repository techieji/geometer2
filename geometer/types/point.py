from typing import Callable, Optional, List, Any


class Point:
    """Base class for all point types."""
    
    def __init__(self):
        pass
    
    def __eq__(self, other: object) -> bool:
        pass
    
    def __repr__(self) -> str:
        pass
    
    def resolve(self, figure: Any) -> 'DefinitePoint':
        """Resolve to a definite point from the figure."""
        pass


class DefinitePoint(Point):
    """A point with concrete x, y coordinates."""
    
    def __init__(self, x: float, y: float):
        pass
    
    @property
    def x(self) -> float:
        pass
    
    @property
    def y(self) -> float:
        pass


class ComputedPoint(Point):
    """A point computed from a function or reference to other shapes."""
    
    def __init__(self, func: Callable[[], List[float]]):
        pass
    
    def resolve(self, figure: Any) -> 'DefinitePoint':
        pass
