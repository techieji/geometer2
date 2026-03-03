import pytest
import uuid
from geometer.core.entities import Point, Shape, PointShape, Line, Bezier, Text, Arc

def test_point_creation():
    p = Point(10, 20)
    assert p.x == 10
    assert p.y == 20
    assert not p.computed
    assert p.dependencies == []

def test_computed_point_creation():
    s1 = Line(Point(0,0), Point(1,1))
    s2 = Line(Point(0,1), Point(1,0))
    cp = Point(5, 5, computed=True, dependencies=[s1, s2])
    assert cp.x == 5
    assert cp.y == 5
    assert cp.computed
    assert set(cp.dependencies) == {s1, s2}

def test_point_equality():
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(2, 1)
    pc1 = Point(1, 2, computed=True)
    pc2 = Point(1, 2, computed=True)

    assert p1 == p2
    assert p1 != p3
    assert p1 != pc1 # computed status affects equality
    assert pc1 == pc2

    # Test with dependencies, which should not affect equality (only x, y, computed)
    s1 = Line(Point(0,0), Point(1,1))
    s2 = Line(Point(0,0), Point(1,1)) # s1 and s2 are different Line objects (different IDs)
    pd1 = Point(1, 2, computed=True, dependencies=[s1])
    pd2 = Point(1, 2, computed=True, dependencies=[s2])
    assert pd1 == pd2 # dependencies list itself is not part of Point's equality check

def test_point_hashing():
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(2, 1)
    pc1 = Point(1, 2, computed=True)

    s = {p1, p2, p3, pc1}
    assert len(s) == 3 # p1 and p2 should be considered equal and result in one item

    assert hash(p1) == hash(p2)
    assert hash(p1) != hash(p3)
    assert hash(p1) != hash(pc1)

def test_point_addition():
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    p_sum = p1 + p2
    assert p_sum == Point(4, 6)
    assert not p_sum.computed # Definite + Definite = Definite
    assert p_sum.dependencies == []

    pc1 = Point(1, 2, computed=True)
    p_sum_computed = p1 + pc1
    assert p_sum_computed == Point(2, 4, computed=True)
    assert p_sum_computed.computed # Definite + Computed = Computed

def test_point_addition_with_dependencies():
    s1 = Line(Point(0,0), Point(1,1))
    s2 = Line(Point(0,1), Point(1,0))
    s3 = Arc(Point(5,5), Point(6,5), Point(5,6))

    p_definite = Point(1, 1)
    pc_no_deps = Point(2, 2, computed=True)
    pc_with_s1 = Point(3, 3, computed=True, dependencies=[s1])
    pc_with_s1_s2 = Point(4, 4, computed=True, dependencies=[s1, s2])
    pc_with_s2_s3 = Point(5, 5, computed=True, dependencies=[s2, s3])

    # Case 1: Definite + Computed (with dependencies)
    res1 = p_definite + pc_with_s1
    assert res1.computed
    assert set(res1.dependencies) == {s1}

    # Case 2: Computed (no deps) + Computed (with deps)
    res2 = pc_no_deps + pc_with_s1
    assert res2.computed
    assert set(res2.dependencies) == {s1}

    # Case 3: Computed (with deps) + Computed (with other deps)
    res3 = pc_with_s1 + pc_with_s2_s3
    assert res3.computed
    assert set(res3.dependencies) == {s1, s2, s3}

    # Case 4: Computed (with overlapping deps)
    res4 = pc_with_s1_s2 + pc_with_s2_s3
    assert res4.computed
    assert set(res4.dependencies) == {s1, s2, s3}

    # Case 5: Definite + Definite -> no deps
    res5 = p_definite + Point(1,1)
    assert not res5.computed
    assert res5.dependencies == []


def test_point_subtraction():
    p1 = Point(5, 5)
    p2 = Point(2, 1)
    p_diff = p1 - p2
    assert p_diff == Point(3, 4)
    assert not p_diff.computed

    pc1 = Point(5, 5, computed=True)
    p_diff_computed = pc1 - p2
    assert p_diff_computed == Point(3, 4, computed=True)
    assert p_diff_computed.computed

def test_point_subtraction_with_dependencies():
    s1 = Line(Point(0,0), Point(1,1))
    pc_with_s1 = Point(3, 3, computed=True, dependencies=[s1])
    p_definite = Point(1, 1)

    res = pc_with_s1 - p_definite
    assert res.computed
    assert set(res.dependencies) == {s1}


def test_point_scalar_multiplication():
    p = Point(2, 3)
    p_scaled = p * 2
    assert p_scaled == Point(4, 6)
    assert not p_scaled.computed
    assert p_scaled.dependencies == []

    p_scaled_rmul = 3 * p
    assert p_scaled_rmul == Point(6, 9)
    assert not p_scaled_rmul.computed
    assert p_scaled_rmul.dependencies == []

    pc_s1 = Line(Point(0,0), Point(1,1))
    pc = Point(2, 3, computed=True, dependencies=[pc_s1])
    pc_scaled = pc * 2
    assert pc_scaled == Point(4, 6, computed=True)
    assert pc_scaled.computed
    assert set(pc_scaled.dependencies) == {pc_s1}


def test_point_distance():
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    assert p1.distance(p2) == 5.0
    assert p2.distance(p1) == 5.0

    p3 = Point(1, 1)
    p4 = Point(1, 1)
    assert p3.distance(p4) == 0.0

def test_shape_creation():
    s = Shape()
    assert isinstance(s.id, uuid.UUID)
    assert s.color == (0, 0, 0)
    assert s.line_thickness == 1
    assert s.endcaps is None

def test_shape_custom_attributes():
    s = Shape(color=(255, 0, 0), line_thickness=3, endcaps='round')
    assert s.color == (255, 0, 0)
    assert s.line_thickness == 3
    assert s.endcaps == 'round'

def test_shape_equality():
    s1 = Shape()
    s2 = Shape()
    s3 = s1 # Reference to the same object

    assert s1 == s1 # Same object
    assert s1 == s3 # Same ID
    assert s1 != s2 # Different IDs

def test_shape_hashing():
    s1 = Shape()
    s2 = Shape()
    s_set = {s1, s2}
    assert len(s_set) == 2 # Distinct shapes should have distinct hashes

    s3 = s1
    s_set_with_duplicate = {s1, s3}
    assert len(s_set_with_duplicate) == 1 # Same shape ID should result in one item

def test_point_shape_creation():
    p = Point(10, 20)
    ps = PointShape(p)
    assert ps.point == p
    assert ps.color == (0, 0, 0) # inherited default

    ps_custom = PointShape(p, color=(0, 255, 0))
    assert ps_custom.color == (0, 255, 0)

def test_line_creation():
    p1 = Point(0, 0)
    p2 = Point(10, 10)
    line = Line(p1, p2)
    assert line.p1 == p1
    assert line.p2 == p2
    assert line.color == (0, 0, 0)

def test_bezier_creation():
    p1, c1, c2, p2 = Point(0, 0), Point(10, 100), Point(90, 100), Point(100, 0)
    bezier = Bezier(p1, c1, c2, p2)
    assert bezier.p1 == p1
    assert bezier.c1 == c1
    assert bezier.c2 == c2
    assert bezier.p2 == p2

def test_text_creation():
    p = Point(50, 50)
    text_shape = Text(p, "Hello World")
    assert text_shape.point == p
    assert text_shape.text_content == "Hello World"
    assert text_shape.color == (0, 0, 0)

def test_arc_creation():
    center = Point(0, 0)
    p1 = Point(10, 0)
    p2 = Point(0, 10)
    arc = Arc(center, p1, p2)
    assert arc.center == center
    assert arc.p1 == p1
    assert arc.p2 == p2
    assert arc.color == (0, 0, 0)
