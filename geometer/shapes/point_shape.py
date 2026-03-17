from typing import Any
from .shape import Shape


class PointShape(Shape):
    """A visual point marker."""
    
    def __init__(self, point: Any, **kwargs):
        super().__init__(**kwargs)
        self._point = point
    
    @property
    def point(self) -> Any:
        return self._point
    
    @point.setter
    def point(self, value: Any) -> None:
        self._point = value
    
    def __repr__(self) -> str:
        return f"PointShape({self._point!r})"
