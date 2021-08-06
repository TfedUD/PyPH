import PHX.spaces
import pytest

# ---- Floor
# -------------------------------------------------------------------------------
def test_Floor_add_FloorSegment(floor_segments):
    flr_seg_3 = floor_segments[2]  # The one with some Geometry

    new_flr = PHX.spaces.Floor()

    assert new_flr.geometry == []

    new_flr.add_new_floor_segment(flr_seg_3)

    assert len(new_flr.geometry) == 1
    assert new_flr.display_name == "103-A Third Floor Segment"

    assert new_flr.non_res_lighting == None
    assert new_flr.non_res_motion == None
    assert new_flr.non_res_usage == None

    assert new_flr.ventilation.airflows.supply == 0.0
    assert new_flr.ventilation.airflows.extract == 0.0
    assert new_flr.ventilation.airflows.transfer == 0.0

    assert new_flr.host_zone_identifier == "GHI-789"


def test_Floor_add_two_FloorSegments_with_different_names(floor_segments):
    flr_seg_2 = floor_segments[1]  # The one with some Geometry
    flr_seg_3a = floor_segments[2]  # The one with some Geometry

    new_flr = PHX.spaces.Floor()

    assert len(new_flr.geometry) == 0

    new_flr.add_new_floor_segment(flr_seg_2)

    assert len(new_flr.geometry) == 1
    assert flr_seg_2.display_name != flr_seg_3a.display_name
    with pytest.raises(Exception):
        new_flr.add_new_floor_segment(flr_seg_3a)


def test_Floor_add_two_FloorSegments_with_same_names(floor_segments):
    flr_seg_3a = floor_segments[2]
    flr_seg_3b = floor_segments[3]

    new_flr = PHX.spaces.Floor()

    assert len(new_flr.geometry) == 0

    new_flr.add_new_floor_segment(flr_seg_3a)

    assert len(new_flr.geometry) == 1
    assert flr_seg_3a.geometry != flr_seg_3b.geometry
    assert flr_seg_3a.display_name == flr_seg_3b.display_name

    new_flr.add_new_floor_segment(flr_seg_3b)

    assert len(new_flr.geometry) == 2


def test_floor_areas(floor_segments):
    # -- Build some FloorSegments, add to the Floor
    flr_seg_2 = floor_segments[2]
    flr_seg_2.floor_area_gross = 400
    flr_seg_2.weighting_factor = 1
    flr_seg_3 = floor_segments[3]
    flr_seg_3.floor_area_gross = 200
    flr_seg_3.weighting_factor = 0.5

    new_flr = PHX.spaces.Floor()
    new_flr.add_new_floor_segment([flr_seg_2, flr_seg_3])

    # Check that the floor weighting factors work
    assert new_flr.floor_area_gross == 600
    assert new_flr.floor_area_weighted == 500

    # --- Check the geometry comes through
    for g in flr_seg_2.geometry:
        assert g in new_flr.geometry

    for g in flr_seg_3.geometry:
        assert g in new_flr.geometry
