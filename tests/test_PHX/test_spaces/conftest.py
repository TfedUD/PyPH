import PHX.spaces
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


@pytest.fixture()
def face3D_3():
    pt_1 = ladybug_geometry.geometry3d.Point3D(0, 0, 0)
    pt_2 = ladybug_geometry.geometry3d.Point3D(-10, 0, 0)
    pt_3 = ladybug_geometry.geometry3d.Point3D(-10, -10, 0)
    pt_4 = ladybug_geometry.geometry3d.Point3D(0, -10, 0)

    return ladybug_geometry.geometry3d.Face3D([pt_1, pt_2, pt_3, pt_4])


@pytest.fixture()
def face3D_4():
    pt_1 = ladybug_geometry.geometry3d.Point3D(0, 0, 0)
    pt_2 = ladybug_geometry.geometry3d.Point3D(10, 0, 0)
    pt_3 = ladybug_geometry.geometry3d.Point3D(10, 10, 0)
    pt_4 = ladybug_geometry.geometry3d.Point3D(0, 10, 0)

    return ladybug_geometry.geometry3d.Face3D([pt_1, pt_2, pt_3, pt_4])


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
def flr_seg_101_with_geometry(face3D_1):
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 100
    seg.space_name = "A First Floor Segment"
    seg.space_number = 101
    seg.geometry = [face3D_1]

    return seg


@pytest.fixture()
def flr_seg_201_with_geometry(face3D_1):
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 100
    seg.space_name = "A Second Floor Segment"
    seg.space_number = 102
    seg.geometry = [face3D_1]

    return seg


@pytest.fixture()
def flr_seg_301_with_geometry_a(face3D_1):
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 100
    seg.space_name = "A Third Floor Segment"
    seg.space_number = 103
    seg.geometry = [face3D_1]

    return seg


@pytest.fixture()
def flr_seg_301_with_geometry_b(face3D_2):
    """Same name/number, different geomtery"""
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 100
    seg.space_name = "A Third Floor Segment"
    seg.space_number = 103
    seg.geometry = [face3D_2]

    return seg


@pytest.fixture()
def flr_seg_301_with_geometry_c(face3D_3, face3D_4):
    """Same name/number, different geomtery"""
    seg = PHX.spaces.FloorSegment()

    seg.weighting_factor = 1
    seg.floor_area_gross = 200
    seg.space_name = "A Third Floor Segment"
    seg.space_number = 103
    seg.geometry = [face3D_3, face3D_4]

    return seg


# # -- Space
# # ------------------------------------------------------------------------------
# Space_Data = namedtuple(
#     "Space_Data",
#     [
#         "space_name",
#         "space_number",
#         "host_zone_identifier",
#         "volumes",
#         "occupancy",
#         "equipment",
#         "ventilation",
#     ],
# )


# @pytest.fixture()
# def space_data_1():
#     return Space_Data("A First Space", 101, "ABC-123", [], None, None, None)


# @pytest.fixture()
# def space_data_2():
#     return Space_Data("A Second Space", 102, "DEF-456", [], None, None, None)
