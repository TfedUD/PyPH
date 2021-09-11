import PHX.geometry


def test_non_plane_poly_area():
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 1, 0)
    normal = PHX.geometry.Vector(0, 0, 1)

    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2]
    p1.nVec = normal

    assert p1.area == 0


def test_triangle_poly_area():
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 1, 0)
    v3 = PHX.geometry.Vertex(1, 1, 0)
    normal = PHX.geometry.Vector(0, 0, 1)

    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3]
    p1.nVec = normal

    assert p1.area == 0.5


def test_square_poly_area():
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 1, 0)
    v3 = PHX.geometry.Vertex(1, 1, 0)
    v4 = PHX.geometry.Vertex(1, 0, 0)
    normal = PHX.geometry.Vector(0, 0, 1)

    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]
    p1.nVec = normal

    assert p1.area == 1


def test_rectangle_poly_area():
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 2, 0)
    v3 = PHX.geometry.Vertex(1, 2, 0)
    v4 = PHX.geometry.Vertex(1, 0, 0)
    normal = PHX.geometry.Vector(0, 0, 1)

    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]
    p1.nVec = normal

    assert p1.area == 2


def test_irregular_poly_area():
    """
    2 +----+
      |    |
    1 |    +-----+
      |          |
    0 +----------+
      0    1     2
    """

    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 2, 0)
    v3 = PHX.geometry.Vertex(2, 1, 0)
    v4 = PHX.geometry.Vertex(1, 1, 0)
    v5 = PHX.geometry.Vertex(1, 2, 0)
    v6 = PHX.geometry.Vertex(2, 0, 0)
    normal = PHX.geometry.Vector(0, 0, 1)

    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4, v5, v6]
    p1.nVec = normal

    assert p1.area == 3
