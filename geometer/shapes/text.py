from typing import Any
from .shape import Shape


class Text(Shape):
    """Text displayed at a point."""
    
    def __init__(self, position: Any, content: str, **kwargs):
        pass
    
    @property
    def position(self) -> Any:
        pass
    
    @position.setter
    def position(self, value: Any) -> None:
        pass
    
    @property
    def content(self) -> str:
        pass
    
    @content.setter
    def content(self, value: str) -> None:
        pass
