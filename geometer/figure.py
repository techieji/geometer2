from typing import List, Optional, Any
from .shapes.shape import Shape


class Figure:
    """Container for all shapes in a drawing."""
    
    def __init__(self):
        self._shapes: List[Shape] = []
    
    def add_shape(self, shape: Shape) -> None:
        self._shapes.append(shape)
    
    def remove_shape(self, shape: Shape) -> None:
        self._shapes.remove(shape)
    
    def get_shapes(self) -> List[Shape]:
        return self._shapes.copy()
    
    def clear(self) -> None:
        self._shapes.clear()
