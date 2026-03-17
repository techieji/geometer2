from typing import Any
from .shape import Shape


class BezierCurve(Shape):
    """A cubic Bezier curve."""
    
    def __init__(self, start: Any, control1: Any, control2: Any, end: Any, **kwargs):
        super().__init__(**kwargs)
        self._start = start
        self._control1 = control1
        self._control2 = control2
        self._end = end
    
    @property
    def start(self) -> Any:
        return self._start
    
    @start.setter
    def start(self, value: Any) -> None:
        self._start = value
    
    @property
    def control1(self) -> Any:
        return self._control1
    
    @control1.setter
    def control1(self, value: Any) -> None:
        self._control1 = value
    
    @property
    def control2(self) -> Any:
        return self._control2
    
    @control2.setter
    def control2(self, value: Any) -> None:
        self._control2 = value
    
    @property
    def end(self) -> Any:
        return self._end
    
    @end.setter
    def end(self, value: Any) -> None:
        self._end = value
    
    def __repr__(self) -> str:
        return f"BezierCurve({self._start!r}, {self._control1!r}, {self._control2!r}, {self._end!r})"
