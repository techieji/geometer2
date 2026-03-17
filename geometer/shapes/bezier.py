from typing import Any
from .shape import Shape


class BezierCurve(Shape):
    """A cubic Bezier curve."""
    
    def __init__(self, start: Any, control1: Any, control2: Any, end: Any, **kwargs):
        pass
    
    @property
    def start(self) -> Any:
        pass
    
    @start.setter
    def start(self, value: Any) -> None:
        pass
    
    @property
    def control1(self) -> Any:
        pass
    
    @control1.setter
    def control1(self, value: Any) -> None:
        pass
    
    @property
    def control2(self) -> Any:
        pass
    
    @control2.setter
    def control2(self, value: Any) -> None:
        pass
    
    @property
    def end(self) -> Any:
        pass
    
    @end.setter
    def end(self, value: Any) -> None:
        pass
