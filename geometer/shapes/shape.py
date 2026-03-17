from typing import Optional, Tuple


class Shape:
    """Base class for all shapes."""
    
    def __init__(
        self,
        color: str = "black",
        line_thickness: float = 1.0,
        endcaps: str = "round"
    ):
        pass
    
    @property
    def color(self) -> str:
        pass
    
    @color.setter
    def color(self, value: str) -> None:
        pass
    
    @property
    def line_thickness(self) -> float:
        pass
    
    @line_thickness.setter
    def line_thickness(self, value: float) -> None:
        pass
    
    @property
    def endcaps(self) -> str:
        pass
    
    @endcaps.setter
    def endcaps(self, value: str) -> None:
        pass
    
    def __repr__(self) -> str:
        pass
