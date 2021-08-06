import PHX.spaces
import pytest

# ---- Floor Segments
# -------------------------------------------------------------------------------
def test_floor_segment_basics(floor_segment_a):
    seg_1 = PHX.spaces.FloorSegment()

    assert seg_1.geometry == []

    seg_1.weighting_factor = floor_segment_a.weighting_factor
    seg_1.space_name = floor_segment_a.space_name
    seg_1.space_number = floor_segment_a.space_number
    seg_1.space_name = floor_segment_a.space_name
    seg_1.non_res_lighting = floor_segment_a.non_res_lighting
    seg_1.non_res_motion = floor_segment_a.non_res_motion
    seg_1.non_res_usage = floor_segment_a.non_res_usage
    seg_1.ventilation_v_sup = floor_segment_a.ventilation_v_sup
    seg_1.ventilation_v_eta = floor_segment_a.ventilation_v_eta
    seg_1.ventilation_v_trans = floor_segment_a.ventilation_v_trans
    seg_1.host_zone_identifier = floor_segment_a.host_zone_identifier

    assert seg_1.weighting_factor == 1
    assert seg_1.space_name == "A First Floor Segment"
    assert seg_1.display_name == "101-A First Floor Segment"
    assert seg_1.space_number == 101
    assert seg_1.non_res_lighting == None
    assert seg_1.non_res_motion == None
    assert seg_1.non_res_usage == None
    assert seg_1.ventilation_v_sup == 0.0
    assert seg_1.ventilation_v_eta == 0.0
    assert seg_1.ventilation_v_trans == 0.0
    assert seg_1.geometry == []
    assert seg_1.host_zone_identifier == "ABC-123"


def test_add_geomgetry_to_floor_segment(floor_segments, face3D_1):

    seg_1 = floor_segments[0]
    seg_2 = floor_segments[1]
    seg_3 = floor_segments[2]

    assert len(seg_1.geometry) == 0
    assert len(seg_2.geometry) == 1
    assert len(seg_3.geometry) == 1

    seg_1.geometry.append(face3D_1)
    seg_3.geometry.append(face3D_1)

    assert len(seg_1.geometry) == 1
    assert len(seg_2.geometry) == 1
    assert len(seg_3.geometry) == 2


def test_floor_segments_weighting(floor_segment_a):

    seg_1 = PHX.spaces.FloorSegment()
    seg_1.floor_area_gross = 200

    assert seg_1.weighting_factor == 1
    assert seg_1.floor_area_weighted == 200

    seg_1.weighting_factor = 0.6
    assert seg_1.floor_area_weighted == 120

    seg_1.weighting_factor = 0.2
    assert seg_1.floor_area_weighted == 40

    with pytest.raises(Exception):
        seg_1.floor_area_weighted = 1000
