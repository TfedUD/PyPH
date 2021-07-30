from PHX.geometry import Polygon, Vertex, Vector, PolygonNormalError
import pytest

def test_Polygon_identifier(reset_geometry_count):
    p1 = Polygon()
    p2 = Polygon()

    assert p1.identifier != p2.identifier

def test_Polygon_count(reset_geometry_count):
    assert Polygon._count == 9_999_999
    p1 = Polygon()
    assert p1.id == 10_000_000

    p2 = Polygon()
    assert p1.id == 10_000_000
    assert p2.id == 10_000_001

def test_Polygon_nVec(reset_geometry_count):
    p1 = Polygon()
    v1 = Vector(0,0,1)

    p1.nVec = v1

    v2 = 'not a Vector'
    with pytest.raises(PolygonNormalError):
        p1.nVec = v2

def test_Polygon_Vertices(reset_geometry_count):
    p1 = Polygon()
    v1 = Vertex(0,0,0)
    v2 = Vertex(0,1,0)
    v3 = Vertex(1,1,0)
    v4 = Vertex(0,1,0)

    p1.vertices.append(v1)
    p1.vertices.append(v2)
    p1.vertices.append(v3)
    p1.vertices.append(v4)

    assert p1.idVert == [ v1.id, v2.id, v3.id, v4.id ]

def test_Polygon_add_child(reset_geometry_count):
    p1 = Polygon()
    p2 = Polygon()
    p3 = Polygon()
    p4 = Polygon()

    # Try adding a single child
    p1.add_children( p2 )
    assert p2.id in p1.children
    assert len(p1.children) == 1

    # Try adding multiple children
    p1.add_children( [p3, p4] )
    assert p2.id in p1.children
    assert p3.id in p1.children
    assert p4.id in p1.children
    assert len(p1.children) == 3

    # Add same Child, should ignore since its already in
    p1.add_children( p2 )
    assert p2.id in p1.children
    assert len(p1.children) == 3