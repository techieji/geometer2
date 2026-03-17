from typing import Any
from .shape import Shape


class Arc(Shape):
    """An arc defined by center, start, and end points."""
    
    def __init__(self, center: Any, start: Any, end: Any, **kwargs):
        pass
    
    @property
    def center(self) -> Any:
        pass
    
    @center.setter
    def center(self, value: Any) -> None:
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
