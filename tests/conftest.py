from collections import namedtuple
import pytest
from ladybug_geometry.geometry3d import Point3D, Face3D


#-- Ladybug Geometry
#-------------------------------------------------------------------------------
@pytest.fixture()
def face3D_1():
    pt_1 = Point3D(0,0,0)
    pt_2 = Point3D(10,0,0)
    pt_3 = Point3D(10,10,0)
    pt_4 = Point3D(0,10,0)

    return Face3D([pt_1, pt_2, pt_3, pt_4])

@pytest.fixture()
def face3D_2():
    pt_1 = Point3D(0,0,0)
    pt_2 = Point3D(-10,0,0)
    pt_3 = Point3D(-10,-10,0)
    pt_4 = Point3D(0,-10,0)

    return Face3D([pt_1, pt_2, pt_3, pt_4])


#-- FloorSegments
#-------------------------------------------------------------------------------
FloorSegment_Data = namedtuple('FloorSegment_Data', [
                                    'weighting_factor',
                                    'floor_area_gross',
                                    'floor_area_weighted',
                                    'space_name',
                                    'space_number',
                                    'non_res_lighting',
                                    'non_res_motion',
                                    'non_res_usage',
                                    'ventilation_v_sup',
                                    'ventilation_v_eta',
                                    'ventilation_v_trans',
                                    'geometry',
                                    'host_zone_identifier',
                                    ])

@pytest.fixture()
def floor_segment_a():
    return FloorSegment_Data(1, None, None,
                            'A First Floor Segment', 101, None,
                            None, None, 0.0, 0.0, 0.0, [], 'ABC-123')

@pytest.fixture()
def floor_segment_b(face3D_1):
    return FloorSegment_Data(1, None, None,
                            'A Second Floor Segment', 102, None,
                            None, None, 0.0, 0.0, 0.0, [face3D_1], 'DEF-456')

@pytest.fixture()
def floor_segment_c1(face3D_2):
    return FloorSegment_Data(1, None, None,
                        'A Third Floor Segment', 103, None,
                        None, None, 0.0, 0.0, 0.0, [face3D_2], 'GHI-789')

@pytest.fixture()
def floor_segment_c2(face3D_2):
    """Same name/number as c_1, different geomtery"""

    return FloorSegment_Data(1, None, None,
                        'A Third Floor Segment', 103, None,
                        None, None, 0.0, 0.0, 0.0, [face3D_1], 'GHI-789')

#-- Space
#-------------------------------------------------------------------------------
Space_Data = namedtuple('Space_Data', [
                                    'space_name',
                                    'space_number',
                                    'host_zone_identifier',
                                    'volumes',
                                    'occupancy',
                                    'equipment',
                                    'ventilation',
                                    ])

@pytest.fixture()
def space_data_1():
    return Space_Data('A First Space', 101, 'ABC-123', [], None, None, None)

@pytest.fixture()
def space_data_2():
    return Space_Data('A Second Space', 102, 'DEF-456', [], None, None, None)

