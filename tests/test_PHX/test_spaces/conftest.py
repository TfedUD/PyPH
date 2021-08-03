import pytest
import PHX.spaces

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
