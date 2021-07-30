import PHX.component
import PHX.geometry
import PHX.variant

def test_Geom_add_components():
    assert True
    g1 = PHX.variant.Geom()
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