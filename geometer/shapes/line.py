from typing import Any
from .shape import Shape


class Line(Shape):
    """A straight line between two points."""
    
    def __init__(self, start: Any, end: Any, **kwargs):
        super().__init__(**kwargs)
        self._start = start
        self._end = end
    
    @property
    def start(self) -> Any:
        return self._start
    
    @start.setter
    def start(self, value: Any) -> None:
        self._start = value
    
    @property
    def end(self) -> Any:
        return self._end
    
    @end.setter
    def end(self, value: Any) -> None:
        self._end = value
    
    def __repr__(self) -> str:
        return f"Line({self._start!r}, {self._end!r})"
