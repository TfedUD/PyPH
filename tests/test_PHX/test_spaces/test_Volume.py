import PHX.spaces
import PHX.programs.ventilation
import pytest


def test_Volume_basics():
    v1 = PHX.spaces.Volume()
    v1.space_number = 101
    v1.space_name = "test 1"
    v2 = PHX.spaces.Volume()
    v2.space_number = 102
    v2.space_name = "test 2"

    assert v1 and v2
    assert v1 != v2

    assert "test 1" in str(v1) and "101" in str(v1)
    assert "test 2" in str(v2) and "102" in str(v2)


def test_Volume_attrs_from_Floor():
    v1 = PHX.spaces.Volume()

    assert v1.space_name == None
    assert v1.space_number == None
    assert v1.host_zone_identifier == None
    assert not v1.volume_geometry

    # -- Add a Floors
    flr = PHX.spaces.Floor()
    flr.space_name = "test"
    flr.space_number = 101
    v1.set_Floor(flr)

    # -- Check the volume attrs
    assert v1.space_name == "test"
    assert v1.space_number == 101
    assert v1.host_zone_identifier == flr.host_zone_identifier
    assert not v1.volume_geometry


def test_Volume_gross_floor_areas(
    flr_seg_301_with_geometry_a, flr_seg_301_with_geometry_b, flr_seg_301_with_geometry_c
):
    flr_1 = PHX.spaces.Floor()
    flr_1.add_new_floor_segment(flr_seg_301_with_geometry_a)

    v_1 = PHX.spaces.Volume()
    v_1.set_Floor(flr_1)

    assert v_1.floor_area_gross == 100

    # -- Reset the floor to a differenet one
    flr_2 = PHX.spaces.Floor()
    flr_2.add_new_floor_segment([flr_seg_301_with_geometry_b, flr_seg_301_with_geometry_c])

    v_1.set_Floor(flr_2)
    assert v_1.floor_area_gross == 300


def test_Volume_weighted_floor_areas(
    flr_seg_301_with_geometry_a, flr_seg_301_with_geometry_b, flr_seg_301_with_geometry_c
):
    flr_1 = PHX.spaces.Floor()
    seg = flr_seg_301_with_geometry_a
    seg.weighting_factor = 0.5
    flr_1.add_new_floor_segment(seg)

    v_1 = PHX.spaces.Volume()
    v_1.set_Floor(flr_1)

    assert v_1.floor_area_weighted == 50

    # -- Reset the Floor to a different one
    flr_2 = PHX.spaces.Floor()
    seg_2 = flr_seg_301_with_geometry_b
    seg_2.weighting_factor = 0.25
    flr_2.add_new_floor_segment([seg_2, flr_seg_301_with_geometry_c])

    v_1.set_Floor(flr_2)
    assert v_1.floor_area_weighted == 225


def test_Volume_ceiling_heights(flr_seg_301_with_geometry_a):
    flr_1 = PHX.spaces.Floor()
    flr_1.add_new_floor_segment(flr_seg_301_with_geometry_a)

    v_1 = PHX.spaces.Volume()
    v_1.set_Floor(flr_1)

    # -- Set the ceiling Height
    v_1.average_ceiling_height = 2.5
    assert v_1.volume == 250
    assert v_1.average_ceiling_height == 2.5

    # -- Set the Volume
    v_1.volume = 400
    assert v_1.volume == 400
    assert v_1.average_ceiling_height == 4


def test_Volume_set_ceiling_height_error():
    v1 = PHX.spaces.Volume()
    assert v1.floor_area_weighted == 0

    with pytest.raises(PHX.spaces.VolumeMissingFloorAreaWarning):
        v1.average_ceiling_height = 2.5


def test_Volume_set_volume_error():
    v1 = PHX.spaces.Volume()
    assert v1.floor_area_weighted == 0

    with pytest.raises(PHX.spaces.VolumeMissingFloorAreaWarning):
        v1.volume = 2000
