import PHX.geometry
import PHX.component
import PHX.bldg_segment
import PHX.infiltration


def test_q50_with_no_envelope():
    host_segment = PHX.bldg_segment.BldgSegment()
    i = PHX.infiltration.Infiltration(host_segment)
    i.annual_avg_airflow = 500

    assert i.q50 == 0


def test_q50_with_simple_envelope():
    host_segment = PHX.bldg_segment.BldgSegment()
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 1, 0)
    v3 = PHX.geometry.Vertex(1, 1, 0)
    v4 = PHX.geometry.Vertex(1, 0, 0)
    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]

    c1 = PHX.component.Component()
    c1.add_polygons(p1)
    c1.type = 1  # Opaque
    c1.idEC = -1  # Outdoors

    host_segment.add_components(c1)

    i = PHX.infiltration.Infiltration(host_segment)
    i.annual_avg_airflow = 500

    assert c1.exposed_area == 1
    assert host_segment.total_envelope_area == 1
    assert i.q50 == 500


def test_q50_with_complex_envelope():
    host_segment = PHX.bldg_segment.BldgSegment()
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 1, 0)
    v3 = PHX.geometry.Vertex(1, 1, 0)
    v4 = PHX.geometry.Vertex(1, 0, 0)
    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]

    v5 = PHX.geometry.Vertex(0, 0, 0)
    v6 = PHX.geometry.Vertex(0, 2, 0)
    v7 = PHX.geometry.Vertex(1, 2, 0)
    v8 = PHX.geometry.Vertex(1, 0, 0)
    p2 = PHX.geometry.Polygon()
    p2.vertices = [v5, v6, v7, v8]

    c1 = PHX.component.Component()
    c1.add_polygons([p1, p2])
    c1.type = 1  # Opaque
    c1.idEC = -1  # Outdoors

    v9 = PHX.geometry.Vertex(0, 0, 0)
    v10 = PHX.geometry.Vertex(0, 2, 0)
    v11 = PHX.geometry.Vertex(1, 2, 0)
    v12 = PHX.geometry.Vertex(1, 0, 0)
    p3 = PHX.geometry.Polygon()
    p3.vertices = [v9, v10, v11, v12]

    c2 = PHX.component.Component()
    c2.add_polygons(p3)
    c2.type = 1  # Opaque
    c2.idEC = -1  # Outdoors

    host_segment.add_components([c1, c2])

    i = PHX.infiltration.Infiltration(host_segment)
    i.annual_avg_airflow = 500

    assert c1.exposed_area == 3
    assert c2.exposed_area == 2
    assert host_segment.total_envelope_area == 5
    assert i.q50 == 100


def test_q50_with_windows():
    host_segment = PHX.bldg_segment.BldgSegment()
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 1, 0)
    v3 = PHX.geometry.Vertex(1, 1, 0)
    v4 = PHX.geometry.Vertex(1, 0, 0)
    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]

    v5 = PHX.geometry.Vertex(0, 0, 0)
    v6 = PHX.geometry.Vertex(0, 2, 0)
    v7 = PHX.geometry.Vertex(1, 2, 0)
    v8 = PHX.geometry.Vertex(1, 0, 0)
    p2 = PHX.geometry.Polygon()
    p2.vertices = [v5, v6, v7, v8]

    c1 = PHX.component.Component()
    c1.add_polygons([p1, p2])
    c1.type = 1  # Opaque
    c1.idEC = -1  # Outdoors

    v9 = PHX.geometry.Vertex(0, 0, 0)
    v10 = PHX.geometry.Vertex(0, 2, 0)
    v11 = PHX.geometry.Vertex(1, 2, 0)
    v12 = PHX.geometry.Vertex(1, 0, 0)
    p3 = PHX.geometry.Polygon()
    p3.vertices = [v9, v10, v11, v12]

    c2 = PHX.component.Component()
    c2.add_polygons(p3)
    c2.type = 1  # Opaque
    c2.idEC = -1  # Outdoors

    wv1 = PHX.geometry.Vertex(0.5, 0.5, 0)
    wv2 = PHX.geometry.Vertex(0.5, 1.0, 0)
    wv3 = PHX.geometry.Vertex(0.5, 1.0, 0)
    wv4 = PHX.geometry.Vertex(1.0, 0.5, 0)
    wp = PHX.geometry.Polygon()
    wp.vertices = [wv1, wv2, wv3, wv4]
    wc = PHX.component.Component()
    wc.add_polygons(wp)
    wc.type = 2  # Transparent
    wc.idEC = -1  # Outdoors

    c2.add_window_as_child(wc, p3.identifier)

    host_segment.add_components([c1, c2])

    i = PHX.infiltration.Infiltration(host_segment)
    i.annual_avg_airflow = 500

    assert c1.exposed_area == 3
    assert c2.exposed_area == 2
    assert host_segment.total_envelope_area == 5
    assert i.q50 == 100
