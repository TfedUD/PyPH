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

#---- Floor
#-------------------------------------------------------------------------------
def test_Floor_add_FloorSegment(floor_segments):
    flr_seg_3 = floor_segments[2] # The one with some Geometry
    
    new_flr = PHX.spaces.Floor()

    assert new_flr.geometry == []

    new_flr.add_new_floor_segment( flr_seg_3 )

    assert len(new_flr.geometry) == 1
    assert new_flr.display_name == '103-A Third Floor Segment'

    assert new_flr.non_res_lighting == None
    assert new_flr.non_res_motion == None
    assert new_flr.non_res_usage == None

    assert new_flr.ventilation_v_sup == 0.0
    assert new_flr.ventilation_v_eta == 0.0
    assert new_flr.ventilation_v_trans == 0.0

    assert new_flr.host_zone_identifier == 'GHI-789'

def test_Floor_add_two_FloorSegments_with_different_names(floor_segments):
    flr_seg_2 = floor_segments[1] # The one with some Geometry
    flr_seg_3a = floor_segments[2] # The one with some Geometry

    new_flr = PHX.spaces.Floor()

    assert len(new_flr.geometry) == 0

    new_flr.add_new_floor_segment( flr_seg_2 )

    assert len(new_flr.geometry) == 1
    assert flr_seg_2.display_name != flr_seg_3a.display_name
    with pytest.raises(Exception):
        new_flr.add_new_floor_segment( flr_seg_3a )

def test_Floor_add_two_FloorSegments_with_same_names(floor_segments):
    flr_seg_3a = floor_segments[2]
    flr_seg_3b = floor_segments[3]

    new_flr = PHX.spaces.Floor()

    assert len(new_flr.geometry) == 0

    new_flr.add_new_floor_segment( flr_seg_3a )

    assert len(new_flr.geometry) == 1
    assert flr_seg_3a.geometry != flr_seg_3b.geometry
    assert flr_seg_3a.display_name == flr_seg_3b.display_name
    
    new_flr.add_new_floor_segment( flr_seg_3b )
    
    assert len(new_flr.geometry) == 2
