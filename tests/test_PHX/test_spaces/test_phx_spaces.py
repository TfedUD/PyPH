import PHX.spaces

#---- Space
#-------------------------------------------------------------------------------
def test_space_basics(space_data_1, space_data_2):
    
    new_space_01 = PHX.spaces.Space()
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
    
    new_space_02 = PHX.spaces.Space()
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
