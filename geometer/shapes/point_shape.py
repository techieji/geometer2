from typing import Any
from .shape import Shape


class PointShape(Shape):
    """A visual point marker."""
    
    def __init__(self, point: Any, **kwargs):
        pass
    
    @property
    def point(self) -> Any:
        pass
    
    @point.setter
    def point(self, value: Any) -> None:
        pass
