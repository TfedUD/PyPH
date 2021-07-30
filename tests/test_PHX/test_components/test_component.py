import PHX.component
import PHX.geometry
import pytest

def test_Component_identifier(reset_component_count):
    """Ensure unique identifier"""

    c1 = PHX.component.Component()
    c2 = PHX.component.Component()

    assert c2.identifier != c1.identifier

def test_Component_id(reset_component_count):
    """Ensure that the id increment is working"""
    
    assert PHX.component.Component._count == 0

    c1 = PHX.component.Component()
    assert PHX.component.Component._count == 1
    assert c1.id == 1

    c2 = PHX.component.Component()
    assert PHX.component.Component._count == 2
    assert c1.id == 1
    assert c2.id == 2

def test_Polygon_ID_list(reset_component_count):
    c1 = PHX.component.Component()
    p1 = PHX.geometry.Polygon()
    p2 = PHX.geometry.Polygon()
    p3 = PHX.geometry.Polygon()
    p4 = PHX.geometry.Polygon()

    # add some Polygons
    c1.add_polygons( [ p1, p2 ] )
    assert c1.polygon_id_list == [ p1.id, p2.id ]

    # add some more
    c1.add_polygons( [ p3, p4] )
    assert c1.polygon_id_list == [ p1.id, p2.id, p3.id, p4.id ]

    # Add same one again, should ignore
    c1.add_polygons( p3 )
    assert c1.polygon_id_list == [ p1.id, p2.id, p3.id, p4.id ]

def test_add_polygon_to_component():
    c1 = PHX.component.Component()
    p1 = PHX.geometry.Polygon()

    # add a single polygon
    assert len(c1.polygons)  == 0
    c1.add_polygons( p1 )
    assert len(c1.polygons) == 1

    # add multiple polygons
    p2 = PHX.geometry.Polygon()
    p3 = PHX.geometry.Polygon()
    assert len(c1.polygons)  == 1
    c1.add_polygons( [p2, p3] )
    assert len(c1.polygons) == 3

    # add the same polgon twice, should ignore it
    p4 = PHX.geometry.Polygon()
    assert len(c1.polygons) == 3
    c1.add_polygons( p4 )
    assert len(c1.polygons) == 4    
    c1.add_polygons( p4 )
    assert len(c1.polygons) == 4

    # Add not a poly
    p5 = 'Not a Polygon'
    with pytest.raises(PHX.geometry.PolygonTypeError):
        c1.add_polygons( p5 )

def test_add_window_as_child():
    # Set up the Hot Component
    c1 = PHX.component.Component()
    p1 = PHX.geometry.Polygon()
    p2 = PHX.geometry.Polygon()
    c1.add_polygons( [p1, p2] )

    # Set up the Window Component
    c_win = PHX.component.Component()
    p_win = PHX.geometry.Polygon()
    c_win.add_polygons( p_win )

    # Add the window as a child of the host poly
    c1.add_window_as_child( c_win, p1.identifier )
    assert p_win.id in p1.children
    assert p_win.id not in p2.children

    # Add a window as a child of a poly not in the compo
    p3 = PHX.geometry.Polygon()
    with pytest.raises(PHX.component.WindowHostNotFoundError):
        c1.add_window_as_child( c_win, p3.identifier )

    # Add not a window
    not_window = "I am not a Window, do not have a .polygons attribute"
    with pytest.raises(AttributeError):
        c1.add_window_as_child( not_window, p1.identifier )
    
    # Add not a window, but closer (has .polygons attribute)
    class NotWindow:
        def __init__(self):
            self.polygons = [ 'not', 'a', 'window']
    not_window = NotWindow()
    with pytest.raises(PHX.geometry.PolygonTypeError):
        c1.add_window_as_child( not_window, p1.identifier )