import pytest
from geometer.types import Point, DefinitePoint, ComputedPoint


class TestDefinitePoint:
    """Tests for DefinitePoint class."""
    
    def test_creation_with_coordinates(self):
        """Test creating a definite point with x, y coordinates."""
        p = DefinitePoint(3.0, 4.0)
        assert p.x == 3.0
        assert p.y == 4.0
    
    def test_x_property(self):
        """Test x coordinate property."""
        p = DefinitePoint(5.5, 2.2)
        assert p.x == 5.5
    
    def test_y_property(self):
        """Test y coordinate property."""
        p = DefinitePoint(5.5, 2.2)
        assert p.y == 2.2
    
    def test_equality_with_same_coordinates(self):
        """Test that two points with same coordinates are equal."""
        p1 = DefinitePoint(1.0, 2.0)
        p2 = DefinitePoint(1.0, 2.0)
        assert p1 == p2
    
    def test_inequality_with_different_coordinates(self):
        """Test that two points with different coordinates are not equal."""
        p1 = DefinitePoint(1.0, 2.0)
        p2 = DefinitePoint(1.0, 3.0)
        assert p1 != p2
    
    def test_repr(self):
        """Test string representation."""
        p = DefinitePoint(1.0, 2.0)
        assert "DefinitePoint" in repr(p)
        assert "1.0" in repr(p)
        assert "2.0" in repr(p)
    
    def test_resolve_returns_self(self):
        """Test that resolve returns the point itself."""
        p = DefinitePoint(1.0, 2.0)
        result = p.resolve(None)
        assert result == p


class TestComputedPoint:
    """Tests for ComputedPoint class."""
    
    def test_creation_with_function(self):
        """Test creating a computed point with a function."""
        func = lambda: [1.0, 2.0]
        cp = ComputedPoint(func)
        assert cp._func == func
    
    def test_resolve_calls_function(self):
        """Test that resolve calls the stored function."""
        func = lambda: [3.0, 4.0]
        cp = ComputedPoint(func)
        result = cp.resolve(None)
        assert isinstance(result, DefinitePoint)
        assert result.x == 3.0
        assert result.y == 4.0
    
    def test_resolve_returns_definite_point(self):
        """Test that resolve returns a DefinitePoint."""
        cp = ComputedPoint(lambda: [5.0, 6.0])
        result = cp.resolve(None)
        assert isinstance(result, DefinitePoint)
        assert result.x == 5.0
        assert result.y == 6.0
    
    def test_equality_based_on_function(self):
        """Test equality of computed points."""
        func1 = lambda: [1.0, 2.0]
        func2 = lambda: [1.0, 2.0]
        cp1 = ComputedPoint(func1)
        cp2 = ComputedPoint(func1)
        # Same function reference should be equal
        assert cp1 == cp2


class TestPointBaseClass:
    """Tests for Point base class."""
    
    def test_is_base_class(self):
        """Test that Point is the base class."""
        assert hasattr(Point, 'resolve')
    
    def test_definite_point_isinstance(self):
        """Test that DefinitePoint is instance of Point."""
        p = DefinitePoint(1.0, 2.0)
        assert isinstance(p, Point)
    
    def test_computed_point_isinstance(self):
        """Test that ComputedPoint is instance of Point."""
        cp = ComputedPoint(lambda: [1.0, 2.0])
        assert isinstance(cp, Point)
