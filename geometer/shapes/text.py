from typing import Any
from .shape import Shape


class Text(Shape):
    """Text displayed at a point."""
    
    def __init__(self, position: Any, content: str, **kwargs):
        super().__init__(**kwargs)
        self._position = position
        self._content = content
    
    @property
    def position(self) -> Any:
        return self._position
    
    @position.setter
    def position(self, value: Any) -> None:
        self._position = value
    
    @property
    def content(self) -> str:
        return self._content
    
    @content.setter
    def content(self, value: str) -> None:
        self._content = value
    
    def __repr__(self) -> str:
        return f"Text({self._position!r}, {self._content!r})"
