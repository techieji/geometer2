from typing import Any
from .shape import Shape


class Line(Shape):
    """A straight line between two points."""
    
    def __init__(self, start: Any, end: Any, **kwargs):
        pass
    
    @property
    def start(self) -> Any:
        pass
    
    @start.setter
    def start(self, value: Any) -> None:
        pass
    
    @property
    def end(self) -> Any:
        pass
    
    @end.setter
    def end(self, value: Any) -> None:
        pass
