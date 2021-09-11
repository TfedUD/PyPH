import pytest
import PHX.bldg_segment
import PHX.spaces
import PHX.geometry

# --- Floor Segments


@pytest.fixture()
def flr_seg_101_with_geometry():
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 10, 0)
    v3 = PHX.geometry.Vertex(10, 10, 0)
    v4 = PHX.geometry.Vertex(10, 0, 0)
    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]

    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 100
    seg.space_name = "A First Floor Segment"
    seg.space_number = 101
    seg.geometry = [p1]

    return seg


@pytest.fixture()
def flr_seg_102_with_geometry():
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 10, 0)
    v3 = PHX.geometry.Vertex(10, 10, 0)
    v4 = PHX.geometry.Vertex(10, 0, 0)
    p1 = PHX.geometry.Polygon()
    p1.vertices = [v1, v2, v3, v4]

    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 200
    seg.space_name = "A Second Floor Segment"
    seg.space_number = 102
    seg.geometry = [p1]

    return seg


# ---
@pytest.fixture
def reset_bldg_segment_count():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.bldg_segment.Zone._count = 0
    PHX.bldg_segment.BldgSegment._count = 0
    PHX.bldg_segment.BldgSegment._default = None

    yield

    PHX.bldg_segment.Zone._count = 0
    PHX.bldg_segment.BldgSegment._count = 0
    PHX.bldg_segment.BldgSegment._default = None
