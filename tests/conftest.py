from collections import namedtuple
import pytest
import ladybug_geometry.geometry3d

# -- Ladybug Geometry
# -------------------------------------------------------------------------------
@pytest.fixture()
def face3D_1():
    pt_1 = ladybug_geometry.geometry3d.Point3D(0, 0, 0)
    pt_2 = ladybug_geometry.geometry3d.Point3D(10, 0, 0)
    pt_3 = ladybug_geometry.geometry3d.Point3D(10, 10, 0)
    pt_4 = ladybug_geometry.geometry3d.Point3D(0, 10, 0)

    return ladybug_geometry.geometry3d.Face3D([pt_1, pt_2, pt_3, pt_4])


@pytest.fixture()
def face3D_2():
    pt_1 = ladybug_geometry.geometry3d.Point3D(0, 0, 0)
    pt_2 = ladybug_geometry.geometry3d.Point3D(-10, 0, 0)
    pt_3 = ladybug_geometry.geometry3d.Point3D(-10, -10, 0)
    pt_4 = ladybug_geometry.geometry3d.Point3D(0, -10, 0)

    return ladybug_geometry.geometry3d.Face3D([pt_1, pt_2, pt_3, pt_4])


# -- FloorSegments
# -------------------------------------------------------------------------------
FloorSegment_Data = namedtuple(
    "FloorSegment_Data",
    [
        "weighting_factor",
        "floor_area_gross",
        "space_name",
        "space_number",
        "non_res_lighting",
        "non_res_motion",
        "non_res_usage",
        "ventilation_v_sup",
        "ventilation_v_eta",
        "ventilation_v_trans",
        "geometry",
        "host_zone_identifier",
    ],
)


@pytest.fixture()
def floor_segment_a():
    return FloorSegment_Data(
        weighting_factor=1,
        floor_area_gross=100,
        space_name="A First Floor Segment",
        space_number=101,
        non_res_lighting=None,
        non_res_motion=None,
        non_res_usage=None,
        ventilation_v_sup=0.0,
        ventilation_v_eta=0.0,
        ventilation_v_trans=0.0,
        geometry=[],
        host_zone_identifier="ABC-123",
    )


@pytest.fixture()
def floor_segment_b(face3D_1):
    return FloorSegment_Data(
        weighting_factor=1,
        floor_area_gross=200,
        space_name="A Second Floor Segment",
        space_number=102,
        non_res_lighting=None,
        non_res_motion=None,
        non_res_usage=None,
        ventilation_v_sup=0.0,
        ventilation_v_eta=0.0,
        ventilation_v_trans=0.0,
        geometry=[face3D_1],
        host_zone_identifier="DEF-456",
    )


@pytest.fixture()
def floor_segment_c1(face3D_2):
    return FloorSegment_Data(
        weighting_factor=1,
        floor_area_gross=300,
        space_name="A Third Floor Segment",
        space_number=103,
        non_res_lighting=None,
        non_res_motion=None,
        non_res_usage=None,
        ventilation_v_sup=0.0,
        ventilation_v_eta=0.0,
        ventilation_v_trans=0.0,
        geometry=[face3D_2],
        host_zone_identifier="GHI-789",
    )


@pytest.fixture()
def floor_segment_c2(face3D_2):
    """Same name/number as c_1, different geomtery"""

    return FloorSegment_Data(
        weighting_factor=1,
        floor_area_gross=400,
        space_name="A Third Floor Segment",
        space_number=103,
        non_res_lighting=None,
        non_res_motion=None,
        non_res_usage=None,
        ventilation_v_sup=0.0,
        ventilation_v_eta=0.0,
        ventilation_v_trans=0.0,
        geometry=[face3D_1],
        host_zone_identifier="GHI-789",
    )


# -- Space
# -------------------------------------------------------------------------------
Space_Data = namedtuple(
    "Space_Data",
    [
        "space_name",
        "space_number",
        "host_zone_identifier",
        "volumes",
        "occupancy",
        "equipment",
        "ventilation",
    ],
)


@pytest.fixture()
def space_data_1():
    return Space_Data("A First Space", 101, "ABC-123", [], None, None, None)


@pytest.fixture()
def space_data_2():
    return Space_Data("A Second Space", 102, "DEF-456", [], None, None, None)
