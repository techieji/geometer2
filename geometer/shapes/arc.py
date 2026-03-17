from typing import Any
from .shape import Shape


class Arc(Shape):
    """An arc defined by center, start, and end points."""
    
    def __init__(self, center: Any, start: Any, end: Any, **kwargs):
        super().__init__(**kwargs)
        self._center = center
        self._start = start
        self._end = end
    
    @property
    def center(self) -> Any:
        return self._center
    
    @center.setter
    def center(self, value: Any) -> None:
        self._center = value
    
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
        return f"Arc({self._center!r}, {self._start!r}, {self._end!r})"
