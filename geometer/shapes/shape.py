from typing import Optional


class Shape:
    """Base class for all shapes."""
    
    def __init__(
        self,
        color: str = "black",
        line_thickness: float = 1.0,
        endcaps: str = "round"
    ):
        self._color = color
        self._line_thickness = line_thickness
        self._endcaps = endcaps
    
    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, value: str) -> None:
        self._color = value
    
    @property
    def line_thickness(self) -> float:
        return self._line_thickness
    
    @line_thickness.setter
    def line_thickness(self, value: float) -> None:
        self._line_thickness = value
    
    @property
    def endcaps(self) -> str:
        return self._endcaps
    
    @endcaps.setter
    def endcaps(self, value: str) -> None:
        self._endcaps = value
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
