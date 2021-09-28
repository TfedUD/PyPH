import PHX.spaces
import pytest

# ---- Floor
# -------------------------------------------------------------------------------
def test_Floor():
    flr = PHX.spaces.Floor()
    flr.space_name = "test name"
    flr.space_number = 101

    assert flr
    assert not flr.geometry
    assert "test name" in str(flr)
    assert "101" in str(flr)


def test_Floor_add_basic_FloorSegment_with_no_geom(flr_seg_101_no_geometry):
    new_flr = PHX.spaces.Floor()

    # -- Add the new floor segment with no geometry
    new_flr.add_new_floor_segment(flr_seg_101_no_geometry)
    assert len(new_flr.geometry) == 0


def test_Floor_add_basic_FloorSegment_with_geom(flr_seg_101_with_geometry):
    new_flr = PHX.spaces.Floor()
    assert not new_flr.geometry

    # -- Add the new floor segment with geometry
    new_flr.add_new_floor_segment(flr_seg_101_with_geometry)
    assert len(new_flr.geometry) == 1


def test_Floor_add_basic_FloorSegment_twice(flr_seg_101_with_geometry):
    new_flr = PHX.spaces.Floor()
    assert not new_flr.geometry

    # -- Add the new floor segment with geometry
    new_flr.add_new_floor_segment(flr_seg_101_with_geometry)
    assert len(new_flr.geometry) == 1

    # -- Try adding it again, should ignore it
    new_flr.add_new_floor_segment(flr_seg_101_with_geometry)
    assert len(new_flr.geometry) == 1


def test_Floor_add_two_FloorSegments_with_different_names(flr_seg_101_with_geometry, flr_seg_201_with_geometry):
    new_flr = PHX.spaces.Floor()
    assert not new_flr.geometry

    # -- Add the new floor segment with geometry
    new_flr.add_new_floor_segment(flr_seg_101_with_geometry)
    assert len(new_flr.geometry) == 1

    # -- Try and add more with geom, but a different name
    with pytest.raises(Exception):
        new_flr.add_new_floor_segment(flr_seg_201_with_geometry)


def test_Floor_add_two_FloorSegments_with_same_names(flr_seg_301_with_geometry_a, flr_seg_301_with_geometry_b):
    new_flr = PHX.spaces.Floor()
    assert not new_flr.geometry

    # -- Add first one
    new_flr.add_new_floor_segment(flr_seg_301_with_geometry_a)
    assert len(new_flr.geometry) == 1

    # -- Add second one
    new_flr.add_new_floor_segment(flr_seg_301_with_geometry_b)
    assert len(new_flr.geometry) == 2


def test_Floor_areas(flr_seg_301_with_geometry_a, flr_seg_301_with_geometry_b, flr_seg_301_with_geometry_c):
    new_flr = PHX.spaces.Floor()

    # -- Check the floor areas update properly
    new_flr.add_new_floor_segment(flr_seg_301_with_geometry_a)
    assert new_flr.floor_area_gross == 100
    assert new_flr.floor_area_weighted == 100

    new_flr.add_new_floor_segment([flr_seg_301_with_geometry_b, flr_seg_301_with_geometry_c])
    assert new_flr.floor_area_gross == 400
    assert new_flr.floor_area_weighted == 400

    # --- Check the geometry comes through
    for g in flr_seg_301_with_geometry_a.geometry:
        assert g in new_flr.geometry

    for g in flr_seg_301_with_geometry_b.geometry:
        assert g in new_flr.geometry

    for g in flr_seg_301_with_geometry_c.geometry:
        assert g in new_flr.geometry


def test_Floor_join_string_values():
    flr = PHX.spaces.Floor()

    # -- Test non-existant
    seg = PHX.spaces.FloorSegment()
    assert not flr._join_string_values(seg, "this_attr_doesnt_exist")

    # -- Test "None" in new floor seg
    seg.test_attr = "None"
    assert not flr._join_string_values(seg, "test_attr")

    # -- Test "None" in existing floor segment
    flr.add_new_floor_segment(seg)
    assert not flr._join_string_values(seg, "test_attr")


def test_set_ventilation_error():
    o = PHX.spaces.Floor()

    # -- Set the ventilation at the Space level
    with pytest.raises(PHX.spaces.RoomVentilationInputError):
        o.ventilation = "Not a RoomVentilation Object"
