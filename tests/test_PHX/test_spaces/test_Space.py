import PHX.spaces
import PHX.ventilation
import pytest


def test_Space_basics():
    sp_1 = PHX.spaces.Space()
    sp_1.space_number = 101
    sp_1.space_name = "test 1"
    sp_2 = PHX.spaces.Space()
    sp_2.space_number = 102
    sp_2.space_name = "test 2"

    assert sp_1 and sp_2
    assert sp_1 != sp_2

    assert "test 1" in str(sp_1) and "101" in str(sp_1)
    assert "test 2" in str(sp_2) and "102" in str(sp_2)


def test_Space_add_new_Volume_works(flr_seg_301_with_geometry_a):
    # Build the FloorSegment, Floor, Volume, Space
    flr = PHX.spaces.Floor()
    flr.add_new_floor_segment(flr_seg_301_with_geometry_a)

    vol = PHX.spaces.Volume()
    vol.set_Floor(flr)
    vol.average_ceiling_height = 2.5

    spc = PHX.spaces.Space()
    spc.space_name = None
    spc.space_number = None
    spc.host_zone_identifier = None
    spc.add_new_volume(vol)

    # --
    assert vol in spc.volumes
    assert spc.space_name == flr_seg_301_with_geometry_a.space_name
    assert spc.space_number == flr_seg_301_with_geometry_a.space_number
    assert spc.host_zone_identifier == flr_seg_301_with_geometry_a.host_zone_identifier


def test_Space_add_new_Volume_errors():
    # Build the Volumes
    vol_1 = PHX.spaces.Volume()
    vol_1.space_name = "test_123"
    vol_1.space_number = "test_456"
    vol_1.host_zone_identifier = "test_789"

    # -- Setup the Space
    spc = PHX.spaces.Space()
    spc.add_new_volume(vol_1)

    # -- Try and add an new Volume with mismatched attrs
    vol_2 = PHX.spaces.Volume()
    vol_2.space_name = "a different name"  # <-----
    vol_2.space_number = "test_456"
    vol_2.host_zone_identifier = "test_789"
    with pytest.raises(PHX.spaces.AddVolumeToSpaceNameError):
        spc.add_new_volume(vol_2)

    vol_2.space_name = "test_123"
    vol_2.space_number = "a different number"  # <----
    vol_2.host_zone_identifier = "test_789"
    with pytest.raises(PHX.spaces.AddVolumeToSpaceNumberError):
        spc.add_new_volume(vol_2)

    vol_2.space_name = "test_123"
    vol_2.space_number = "test_456"
    vol_2.host_zone_identifier = "a different host id"  # <----
    with pytest.raises(PHX.spaces.AddVolumeToSpaceHostZoneIDError):
        spc.add_new_volume(vol_2)


def test_set_Space_ventilation(flr_seg_301_with_geometry_a):

    flr = PHX.spaces.Floor()
    flr.add_new_floor_segment(flr_seg_301_with_geometry_a)

    vol_1 = PHX.spaces.Volume()
    vol_1.set_Floor(flr)
    assert vol_1.floor == flr

    sp_1 = PHX.spaces.Space()
    sp_1.add_new_volume(vol_1)
    assert vol_1 in sp_1.volumes

    # -- Set the ventilation at the Space level
    vent_1 = PHX.ventilation.SpaceVentilation()
    sp_1.ventilation = vent_1

    # -- Should ripple down through all the sub-elements of the Space
    assert sp_1.ventilation == vent_1
    assert vol_1.ventilation == vent_1
    assert vol_1.floor.ventilation == vent_1
    assert flr.ventilation == vent_1
    assert flr_seg_301_with_geometry_a.ventilation == vent_1


def test_set_Space_ventilation_error():
    sp_1 = PHX.spaces.Space()

    # -- Set the ventilation at the Space level
    with pytest.raises(PHX.spaces.SpaceVentilationInputError):
        sp_1.ventilation = "Not a SpaceVentilation Object"


def test_Space_floor_area_weighted(
    flr_seg_301_with_geometry_a, flr_seg_301_with_geometry_b, flr_seg_301_with_geometry_c
):
    # Build the FloorSegment, Floor, Volume, Space
    flr = PHX.spaces.Floor()
    flr.add_new_floor_segment(flr_seg_301_with_geometry_a)

    vol = PHX.spaces.Volume()
    vol.set_Floor(flr)
    vol.average_ceiling_height = 2.5

    spc = PHX.spaces.Space()
    spc.add_new_volume(vol)

    # --
    assert spc.floor_area_weighted == 100


def test_Space_clear_height_single_volume(flr_seg_301_with_geometry_a):
    # Build the FloorSegment, Floor, Volume, Space
    flr = PHX.spaces.Floor()
    flr.add_new_floor_segment(flr_seg_301_with_geometry_a)

    vol = PHX.spaces.Volume()
    vol.set_Floor(flr)
    vol.average_ceiling_height = 2.5

    spc = PHX.spaces.Space()
    spc.add_new_volume(vol)

    # --
    assert spc.clear_height == 2.5


def test_Space_clear_height_multiple_volumes(flr_seg_301_with_geometry_a, flr_seg_301_with_geometry_b):
    # Build the FloorSegment, Floor, Volume, Space
    flr_1 = PHX.spaces.Floor()
    flr_1.add_new_floor_segment(flr_seg_301_with_geometry_a)
    vol_1 = PHX.spaces.Volume()
    vol_1.set_Floor(flr_1)

    flr_2 = PHX.spaces.Floor()
    flr_2.add_new_floor_segment(flr_seg_301_with_geometry_b)
    vol_2 = PHX.spaces.Volume()
    vol_2.set_Floor(flr_2)

    vol_1.average_ceiling_height = 4
    vol_2.average_ceiling_height = 2

    spc = PHX.spaces.Space()
    spc.add_new_volume(vol_1)
    spc.add_new_volume(vol_2)

    # --
    assert spc.clear_height == 3  # = (4m * 100m2) + (2m * 100m2) / 200m2


def test_Space_peak_occupancy(flr_seg_101_with_geometry):
    flr = PHX.spaces.Floor()
    flr.add_new_floor_segment(flr_seg_101_with_geometry)

    vol = PHX.spaces.Volume()
    vol.set_Floor(flr)

    spc = PHX.spaces.Space()
    spc.add_new_volume(vol)

    flr_seg_101_with_geometry.floor_area_gross = 0.0
    spc.occupancy.people_per_area = 0.0
    assert spc.peak_occupancy == 0

    flr_seg_101_with_geometry.floor_area_gross = 0.0
    spc.occupancy.people_per_area = 10
    assert spc.peak_occupancy == 0

    flr_seg_101_with_geometry.floor_area_gross = 100
    spc.occupancy.people_per_area = 0.0
    assert spc.peak_occupancy == 0

    flr_seg_101_with_geometry.floor_area_gross = 100
    spc.occupancy.people_per_area = 10
    assert spc.peak_occupancy == 1000
