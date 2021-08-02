import PHX.spaces
import pytest

@pytest.fixture()
def floor_segments(floor_segment_a, floor_segment_b, floor_segment_c1, floor_segment_c2):
    """Create new FloorSegments based on the input namedtuples"""
    
    params_a = floor_segment_a._asdict()
    params_b = floor_segment_b._asdict()
    params_c1 = floor_segment_c1._asdict()
    params_c2 = floor_segment_c2._asdict()
    
    seg_1 = PHX.spaces.FloorSegment()
    seg_2 = PHX.spaces.FloorSegment()
    seg_3 = PHX.spaces.FloorSegment()
    seg_4 = PHX.spaces.FloorSegment()

    for k,v in params_a.items():
        setattr(seg_1, k, v)

    for k,v in params_b.items():
        setattr(seg_2, k, v)
    
    for k,v in params_c1.items():
        setattr(seg_3, k, v)

    for k,v in params_c2.items():
        setattr(seg_4, k, v)

    return seg_1, seg_2, seg_3, seg_4

#---- Floor Segments
#-------------------------------------------------------------------------------
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
    assert seg_1.space_name == 'A First Floor Segment'
    assert seg_1.display_name == '101-A First Floor Segment'
    assert seg_1.space_number == 101
    assert seg_1.non_res_lighting == None
    assert seg_1.non_res_motion == None
    assert seg_1.non_res_usage == None
    assert seg_1.ventilation_v_sup == 0.0
    assert seg_1.ventilation_v_eta == 0.0
    assert seg_1.ventilation_v_trans == 0.0
    assert seg_1.geometry == []
    assert seg_1.host_zone_identifier == 'ABC-123'

def test_add_geomgetry_to_floor_segment(floor_segments, face3D_1):
    
    seg_1 = floor_segments[0]
    seg_2 = floor_segments[1]
    seg_3 = floor_segments[2]

    assert len(seg_1.geometry) == 0
    assert len(seg_2.geometry) == 1
    assert len(seg_3.geometry) == 1

    seg_1.geometry.append( face3D_1 )
    seg_3.geometry.append( face3D_1 )

    assert len(seg_1.geometry) == 1
    assert len(seg_2.geometry) == 1
    assert len(seg_3.geometry) == 2
