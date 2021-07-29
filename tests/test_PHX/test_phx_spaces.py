from PHX.spaces import FloorSegment, Floor, Volume, Space
import pytest

@pytest.fixture()
def floor_segments(floor_segment_a, floor_segment_b, floor_segment_c1, floor_segment_c2):
    """Create new FloorSegments based on the input namedtuples"""
    
    params_a = floor_segment_a._asdict()
    params_b = floor_segment_b._asdict()
    params_c1 = floor_segment_c1._asdict()
    params_c2 = floor_segment_c2._asdict()
    
    seg_1 = FloorSegment()
    seg_2 = FloorSegment()
    seg_3 = FloorSegment()
    seg_4 = FloorSegment()

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
    seg_1 = FloorSegment()

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

#---- Floor
#-------------------------------------------------------------------------------
def test_Floor_add_FloorSegment(floor_segments):
    flr_seg_3 = floor_segments[2] # The one with some Geometry
    
    new_flr = Floor()

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

    new_flr = Floor()

    assert len(new_flr.geometry) == 0

    new_flr.add_new_floor_segment( flr_seg_2 )

    assert len(new_flr.geometry) == 1
    assert flr_seg_2.display_name != flr_seg_3a.display_name
    with pytest.raises(Exception):
        new_flr.add_new_floor_segment( flr_seg_3a )

def test_Floor_add_two_FloorSegments_with_same_names(floor_segments):
    flr_seg_3a = floor_segments[2]
    flr_seg_3b = floor_segments[3]

    new_flr = Floor()

    assert len(new_flr.geometry) == 0

    new_flr.add_new_floor_segment( flr_seg_3a )

    assert len(new_flr.geometry) == 1
    assert flr_seg_3a.geometry != flr_seg_3b.geometry
    assert flr_seg_3a.display_name == flr_seg_3b.display_name
    
    new_flr.add_new_floor_segment( flr_seg_3b )
    
    assert len(new_flr.geometry) == 2

#---- Volume
#-------------------------------------------------------------------------------


#---- Space
#-------------------------------------------------------------------------------
def test_space_basics(space_data_1, space_data_2):
    
    new_space_01 = Space()
    new_space_01.space_name = space_data_1.space_name
    new_space_01.space_number = space_data_1.space_number
    new_space_01.host_zone_identifier = space_data_1.host_zone_identifier
    new_space_01.volumes = space_data_1.volumes
    new_space_01.occupancy = space_data_1.occupancy
    new_space_01.equipment = space_data_1.equipment
    new_space_01.ventilation = space_data_1.ventilation

    assert new_space_01.space_name == 'A First Space'
    assert new_space_01.space_number == 101
    assert new_space_01.host_zone_identifier == 'ABC-123'
    assert len(new_space_01.volumes) == 0
    
    new_space_02 = Space()
    new_space_02.space_name = space_data_2.space_name
    new_space_02.space_number = space_data_2.space_number
    new_space_02.host_zone_identifier = space_data_2.host_zone_identifier
    new_space_02.volumes = space_data_2.volumes
    new_space_02.occupancy = space_data_2.occupancy
    new_space_02.equipment = space_data_2.equipment
    new_space_02.ventilation = space_data_2.ventilation

    assert new_space_01.space_name == 'A First Space'
    assert new_space_02.space_name == 'A Second Space'
    assert new_space_01.space_number == 101
    assert new_space_02.space_number == 102
    assert new_space_01.host_zone_identifier == 'ABC-123'
    assert new_space_02.host_zone_identifier == 'DEF-456'
    assert len(new_space_01.volumes) == 0
    assert len(new_space_02.volumes) == 0
