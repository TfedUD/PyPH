import PHX.component
import PHX.geometry
import PHX.bldg_segment


def test_Geom_add_components():
    g1 = PHX.bldg_segment.Geom()
    c1 = PHX.component.Component()
    c2 = PHX.component.Component()
    p1 = PHX.geometry.Polygon()
    p2 = PHX.geometry.Polygon()

    c1.add_polygons(p1)
    c2.add_polygons(p2)

    # Add a Component to the collection
    g1.add_component_polygons(c1)

    assert p1 in g1.polygons
    assert len(g1.polygons) == 1

    # Add another Component
    g1.add_component_polygons(c2)

    assert p1 in g1.polygons
    assert p2 in g1.polygons
    assert len(g1.polygons) == 2

    # Add the same Component again
    # should ignore it
    g1.add_component_polygons(c2)

    assert p1 in g1.polygons
    assert p2 in g1.polygons
    assert len(g1.polygons) == 2


def test_Geom_get_vertices():
    """Test that all vertices are gotten correctly from the Geom collection"""

    g1 = PHX.bldg_segment.Geom()
    c1 = PHX.component.Component()
    p1 = PHX.geometry.Polygon()
    v11 = PHX.geometry.Vertex(0, 0, 0)
    v12 = PHX.geometry.Vertex(0, 1, 0)
    v13 = PHX.geometry.Vertex(1, 1, 0)
    v14 = PHX.geometry.Vertex(1, 0, 0)

    p2 = PHX.geometry.Polygon()
    v21 = PHX.geometry.Vertex(0, 0, 0)
    v22 = PHX.geometry.Vertex(0, 1, 0)
    v23 = PHX.geometry.Vertex(1, 1, 0)
    v24 = PHX.geometry.Vertex(1, 0, 0)

    p1.vertices = [v11, v12, v13, v14]
    p2.vertices = [v21, v22, v23, v24]

    c1.add_polygons([p1, p2])
    g1.add_component_polygons(c1)

    assert list(g1.vertices) == [v11, v12, v13, v14, v21, v22, v23, v24]
