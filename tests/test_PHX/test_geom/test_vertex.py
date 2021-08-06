from PHX.geometry import Vertex


def test_Vertex_identifier(reset_geometry_count):
    v1 = Vertex()
    v2 = Vertex()

    assert v1.identifier != v2.identifier


def test_Vertex_attributes(reset_geometry_count):
    v1 = Vertex()

    assert v1.x == 0
    assert v1.y == 0
    assert v1.z == 0
    assert not v1.user_data

    v1.x = 12
    v1.y = 13
    v1.z = 14

    assert v1.x == 12
    assert v1.y == 13
    assert v1.z == 14

    v2 = Vertex(15, 16, 17)
    assert v2.x == 15
    assert v2.y == 16
    assert v2.z == 17
    assert not v2.user_data


def test_Vertex_count(reset_geometry_count):
    assert Vertex._count == 0

    v1 = Vertex()
    assert Vertex._count == 1
    assert v1.id == 1

    v2 = Vertex()
    assert Vertex._count == 2
    assert v1.id == 1
    assert v2.id == 2

    v3 = Vertex(1, 2, 3)
    assert Vertex._count == 3
    assert v1.id == 1
    assert v2.id == 2
    assert v3.id == 3
