import PHX.spaces
import pytest
import PHX.geometry

# -- Ladybug Geometry
# -------------------------------------------------------------------------------
@pytest.fixture()
def polygon_1():
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 10, 0)
    v3 = PHX.geometry.Vertex(10, 10, 0)
    v4 = PHX.geometry.Vertex(10, 0, 0)
    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]
    return p1


@pytest.fixture()
def polygon_2():
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, -10, 0)
    v3 = PHX.geometry.Vertex(-10, -10, 0)
    v4 = PHX.geometry.Vertex(-10, 0, 0)
    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]
    return p1


@pytest.fixture()
def polygon_3():
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, -10, 0)
    v3 = PHX.geometry.Vertex(-10, -10, 0)
    v4 = PHX.geometry.Vertex(-10, 0, 0)
    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]
    return p1


@pytest.fixture()
def polygon_4():
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 10, 0)
    v3 = PHX.geometry.Vertex(10, 10, 0)
    v4 = PHX.geometry.Vertex(10, 0, 0)
    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]
    return p1


# -- FloorSegments
# -------------------------------------------------------------------------------
@pytest.fixture()
def flr_seg_101_no_geometry():
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 0
    seg.space_name = "A First Floor Segment"
    seg.space_number = 101
    seg.geometry = []

    return seg


@pytest.fixture()
def flr_seg_101_with_geometry(polygon_1):
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 100
    seg.space_name = "A First Floor Segment"
    seg.space_number = 101
    seg.geometry = [polygon_1]

    return seg


@pytest.fixture()
def flr_seg_201_with_geometry(polygon_1):
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 100
    seg.space_name = "A Second Floor Segment"
    seg.space_number = 102
    seg.geometry = [polygon_1]

    return seg


@pytest.fixture()
def flr_seg_301_with_geometry_a(polygon_1):
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 100
    seg.space_name = "A Third Floor Segment"
    seg.space_number = 103
    seg.geometry = [polygon_1]

    return seg


@pytest.fixture()
def flr_seg_301_with_geometry_b(polygon_2):
    """Same name/number, different geomtery"""
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 100
    seg.space_name = "A Third Floor Segment"
    seg.space_number = 103
    seg.geometry = [polygon_2]

    return seg


@pytest.fixture()
def flr_seg_301_with_geometry_c(polygon_3, polygon_4):
    """Same name/number, different geomtery"""
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 200
    seg.space_name = "A Third Floor Segment"
    seg.space_number = 103
    seg.geometry = [polygon_3, polygon_4]

    return seg
