import pytest
from geometer.shapes import Shape, PointShape, Line, BezierCurve, Text, Arc
from geometer.types import DefinitePoint


class TestShapeBaseClass:
    """Tests for Shape base class."""
    
    def test_default_color(self):
        """Test default color is black."""
        shape = Shape()
        assert shape.color == "black"
    
    def test_default_line_thickness(self):
        """Test default line thickness is 1.0."""
        shape = Shape()
        assert shape.line_thickness == 1.0
    
    def test_default_endcaps(self):
        """Test default endcaps is round."""
        shape = Shape()
        assert shape.endcaps == "round"
    
    def test_custom_color(self):
        """Test setting custom color."""
        shape = Shape(color="red")
        assert shape.color == "red"
    
    def test_custom_line_thickness(self):
        """Test setting custom line thickness."""
        shape = Shape(line_thickness=3.0)
        assert shape.line_thickness == 3.0
    
    def test_custom_endcaps(self):
        """Test setting custom endcaps."""
        shape = Shape(endcaps="butt")
        assert shape.endcaps == "butt"
    
    def test_repr(self):
        """Test string representation."""
        shape = Shape()
        assert "Shape" in repr(shape)
    
    def test_color_setter(self):
        """Test color property setter."""
        shape = Shape()
        shape.color = "blue"
        assert shape.color == "blue"
    
    def test_line_thickness_setter(self):
        """Test line_thickness property setter."""
        shape = Shape()
        shape.line_thickness = 2.5
        assert shape.line_thickness == 2.5
    
    def test_endcaps_setter(self):
        """Test endcaps property setter."""
        shape = Shape()
        shape.endcaps = "square"
        assert shape.endcaps == "square"


class TestPointShape:
    """Tests for PointShape class."""
    
    def test_creation(self):
        """Test creating a point shape."""
        p = DefinitePoint(1.0, 2.0)
        ps = PointShape(p)
        assert ps.point == p
    
    def test_point_property(self):
        """Test point property getter and setter."""
        p1 = DefinitePoint(1.0, 2.0)
        p2 = DefinitePoint(3.0, 4.0)
        ps = PointShape(p1)
        assert ps.point == p1
        ps.point = p2
        assert ps.point == p2
    
    def test_inherits_from_shape(self):
        """Test that PointShape inherits from Shape."""
        p = DefinitePoint(1.0, 2.0)
        ps = PointShape(p)
        assert isinstance(ps, Shape)


class TestLine:
    """Tests for Line class."""
    
    def test_creation(self):
        """Test creating a line."""
        start = DefinitePoint(0.0, 0.0)
        end = DefinitePoint(1.0, 1.0)
        line = Line(start, end)
        assert line.start == start
        assert line.end == end
    
    def test_start_property(self):
        """Test start point property."""
        start = DefinitePoint(1.0, 2.0)
        end = DefinitePoint(3.0, 4.0)
        line = Line(start, end)
        assert line.start == start
    
    def test_end_property(self):
        """Test end point property."""
        start = DefinitePoint(1.0, 2.0)
        end = DefinitePoint(3.0, 4.0)
        line = Line(start, end)
        assert line.end == end
    
    def test_inherits_from_shape(self):
        """Test that Line inherits from Shape."""
        line = Line(DefinitePoint(0, 0), DefinitePoint(1, 1))
        assert isinstance(line, Shape)


class TestBezierCurve:
    """Tests for BezierCurve class."""
    
    def test_creation(self):
        """Test creating a bezier curve."""
        start = DefinitePoint(0.0, 0.0)
        c1 = DefinitePoint(1.0, 0.0)
        c2 = DefinitePoint(0.0, 1.0)
        end = DefinitePoint(1.0, 1.0)
        bezier = BezierCurve(start, c1, c2, end)
        assert bezier.start == start
        assert bezier.control1 == c1
        assert bezier.control2 == c2
        assert bezier.end == end
    
    def test_control_points(self):
        """Test control point properties."""
        start = DefinitePoint(0.0, 0.0)
        c1 = DefinitePoint(1.0, 0.0)
        c2 = DefinitePoint(0.0, 1.0)
        end = DefinitePoint(1.0, 1.0)
        bezier = BezierCurve(start, c1, c2, end)
        assert bezier.control1 == c1
        assert bezier.control2 == c2
    
    def test_start_end_points(self):
        """Test start and end point properties."""
        start = DefinitePoint(0.0, 0.0)
        c1 = DefinitePoint(1.0, 0.0)
        c2 = DefinitePoint(0.0, 1.0)
        end = DefinitePoint(1.0, 1.0)
        bezier = BezierCurve(start, c1, c2, end)
        assert bezier.start == start
        assert bezier.end == end
    
    def test_inherits_from_shape(self):
        """Test that BezierCurve inherits from Shape."""
        bezier = BezierCurve(
            DefinitePoint(0, 0),
            DefinitePoint(1, 0),
            DefinitePoint(0, 1),
            DefinitePoint(1, 1)
        )
        assert isinstance(bezier, Shape)


class TestText:
    """Tests for Text class."""
    
    def test_creation(self):
        """Test creating text."""
        pos = DefinitePoint(5.0, 5.0)
        text = Text(pos, "Hello")
        assert text.position == pos
        assert text.content == "Hello"
    
    def test_position_property(self):
        """Test position property."""
        pos1 = DefinitePoint(1.0, 2.0)
        pos2 = DefinitePoint(3.0, 4.0)
        text = Text(pos1, "Test")
        assert text.position == pos1
        text.position = pos2
        assert text.position == pos2
    
    def test_content_property(self):
        """Test content property."""
        text = Text(DefinitePoint(0, 0), "Initial")
        assert text.content == "Initial"
        text.content = "Updated"
        assert text.content == "Updated"
    
    def test_inherits_from_shape(self):
        """Test that Text inherits from Shape."""
        text = Text(DefinitePoint(0, 0), "test")
        assert isinstance(text, Shape)


class TestArc:
    """Tests for Arc class."""
    
    def test_creation(self):
        """Test creating an arc."""
        center = DefinitePoint(0.0, 0.0)
        start = DefinitePoint(1.0, 0.0)
        end = DefinitePoint(0.0, 1.0)
        arc = Arc(center, start, end)
        assert arc.center == center
        assert arc.start == start
        assert arc.end == end
    
    def test_center_property(self):
        """Test center property."""
        center = DefinitePoint(0.0, 0.0)
        start = DefinitePoint(1.0, 0.0)
        end = DefinitePoint(0.0, 1.0)
        arc = Arc(center, start, end)
        assert arc.center == center
    
    def test_start_property(self):
        """Test start point property."""
        center = DefinitePoint(0.0, 0.0)
        start = DefinitePoint(1.0, 0.0)
        end = DefinitePoint(0.0, 1.0)
        arc = Arc(center, start, end)
        assert arc.start == start
    
    def test_end_property(self):
        """Test end point property."""
        center = DefinitePoint(0.0, 0.0)
        start = DefinitePoint(1.0, 0.0)
        end = DefinitePoint(0.0, 1.0)
        arc = Arc(center, start, end)
        assert arc.end == end
    
    def test_inherits_from_shape(self):
        """Test that Arc inherits from Shape."""
        arc = Arc(DefinitePoint(0, 0), DefinitePoint(1, 0), DefinitePoint(0, 1))
        assert isinstance(arc, Shape)
