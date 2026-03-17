from typing import List, Optional, Any
from .shapes.shape import Shape


class Figure:
    """Container for all shapes in a drawing."""
    
    def __init__(self):
        pass
    
    def add_shape(self, shape: Shape) -> None:
        pass
    
    def remove_shape(self, shape: Shape) -> None:
        pass
    
    def get_shapes(self) -> List[Shape]:
        pass
    
    def clear(self) -> None:
        pass
