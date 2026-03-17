from typing import Callable, Optional, List, Any


class Point:
    """Base class for all point types."""
    
    def __init__(self):
        pass
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.resolve(None) == other.resolve(None)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
    
    def resolve(self, figure: Any) -> 'DefinitePoint':
        """Resolve to a definite point from the figure."""
        raise NotImplementedError


class DefinitePoint(Point):
    """A point with concrete x, y coordinates."""
    
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
    
    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        if isinstance(other, DefinitePoint):
            return self._x == other._x and self._y == other._y
        return self.resolve(None) == other.resolve(None)
    
    def __repr__(self) -> str:
        return f"DefinitePoint({self._x}, {self._y})"
    
    def resolve(self, figure: Any) -> 'DefinitePoint':
        """Resolve returns self since this is already definite."""
        return self


class ComputedPoint(Point):
    """A point computed from a function or reference to other shapes."""
    
    def __init__(self, func: Callable[[], List[float]]):
        self._func = func
    
    @property
    def func(self) -> Callable[[], List[float]]:
        return self._func
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        if isinstance(other, ComputedPoint):
            return self._func == other._func
        return self.resolve(None) == other.resolve(None)
    
    def __repr__(self) -> str:
        return f"ComputedPoint({self._func})"
    
    def resolve(self, figure: Any) -> 'DefinitePoint':
        """Call the stored function and return a DefinitePoint."""
        result = self._func()
        return DefinitePoint(result[0], result[1])
