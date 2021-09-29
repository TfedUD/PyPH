import PHX.bldg_segment
import PHX.spaces


def test_Zone_identifier(reset_bldg_segment_count):
    z1 = PHX.bldg_segment.Zone()
    z2 = PHX.bldg_segment.Zone()

    assert z1.identifier != z2.identifier


def test_Zone_ID(reset_bldg_segment_count):
    assert PHX.bldg_segment.Zone._count == 0

    z1 = PHX.bldg_segment.Zone()
    assert PHX.bldg_segment.Zone._count == 1

    z2 = PHX.bldg_segment.Zone()
    assert PHX.bldg_segment.Zone._count == 2


def test_Room_add_new_Space(reset_bldg_segment_count):
    r1 = PHX.bldg_segment.Room()
    s1 = PHX.spaces.Space()

    assert len(r1.spaces) == 0
    r1.add_spaces(r1)
    assert r1 in r1.spaces
    assert len(r1.spaces) == 1


def test_Room_add_single_Space_sets_values(flr_seg_101_with_geometry):
    # -- Build Space
    flr = PHX.spaces.Floor()
    flr.add_new_floor_segment(flr_seg_101_with_geometry)
    assert flr_seg_101_with_geometry.floor_area_weighted == 100
    assert flr.floor_area_weighted == 100

    vol_1 = PHX.spaces.Volume()
    vol_1.set_Floor(flr)
    vol_1.average_ceiling_height = 2.5
    assert vol_1.floor_area_weighted == 100
    assert vol_1.average_ceiling_height == 2.5
    assert vol_1.volume == 250

    space_1 = PHX.spaces.Space()
    space_1.add_new_volume(vol_1)

    # -- Add Space to the Room
    r1 = PHX.bldg_segment.Room()
    r1.add_spaces(space_1)

    # -- Build Zone, add Room to Zone
    z1 = PHX.bldg_segment.Zone()
    z1.add_rooms(r1)

    assert r1
    assert z1
    assert z1.volume_net == 250
    assert z1.volume_net_selection == 6  # user-defined
    assert z1.floor_area == 100
    assert z1.floor_area_selection == 6  # user-defined


def test_Room_add_multiple_Spaces_sets_values(flr_seg_101_with_geometry, flr_seg_102_with_geometry):
    # -- Build Space 1
    flr_1 = PHX.spaces.Floor()
    flr_1.add_new_floor_segment(flr_seg_101_with_geometry)
    assert flr_seg_101_with_geometry.floor_area_weighted == 100
    assert flr_1.floor_area_weighted == 100

    vol_1 = PHX.spaces.Volume()
    vol_1.set_Floor(flr_1)
    vol_1.average_ceiling_height = 2.5
    assert vol_1.floor_area_weighted == 100
    assert vol_1.average_ceiling_height == 2.5
    assert vol_1.volume == 250

    space_1 = PHX.spaces.Space()
    space_1.add_new_volume(vol_1)

    # -- Build Space 2
    flr_2 = PHX.spaces.Floor()
    flr_2.add_new_floor_segment(flr_seg_102_with_geometry)
    assert flr_seg_102_with_geometry.floor_area_weighted == 200
    assert flr_2.floor_area_weighted == 200

    vol_2 = PHX.spaces.Volume()
    vol_2.set_Floor(flr_2)
    vol_2.average_ceiling_height = 2.5
    assert vol_2.floor_area_weighted == 200
    assert vol_2.average_ceiling_height == 2.5
    assert vol_2.volume == 500

    space_2 = PHX.spaces.Space()
    space_2.add_new_volume(vol_2)

    # -- Add Space to the Room
    r1 = PHX.bldg_segment.Room()
    r1.add_spaces([space_1, space_2])

    # -- Build a Zone, Add the Room to the Zone
    z1 = PHX.bldg_segment.Zone()
    z1.add_rooms(r1)

    assert r1
    assert z1
    assert z1.volume_net == 250 + 500
    assert z1.volume_net_selection == 6  # user-defined
    assert z1.floor_area == 100 + 200
    assert z1.floor_area_selection == 6  # user-defined


def test_Zone_add_with_empty_params(reset_bldg_segment_count):
    z1 = PHX.bldg_segment.Zone()
    z2 = PHX.bldg_segment.Zone()

    z3 = z1 + z2
    assert z3
    assert z3 != z1 and z3 != z2


def test_Zone_add_with_values(reset_bldg_segment_count):
    z1 = PHX.bldg_segment.Zone()
    z1.volume_gross = 100
    z1.volume_net = 200
    z1.floor_area = 300
    z1.clearance_height = 2.5
    z1.spec_heat_cap = 132

    z2 = PHX.bldg_segment.Zone()
    z2.volume_gross = 400
    z2.volume_net = 500
    z2.floor_area = 600
    z2.clearance_height = 4
    z2.spec_heat_cap = 96

    z3 = z1 + z2
    assert z3

    # -- Sumes
    assert z3.volume_gross == 500
    assert z3.volume_net == 700
    assert z3.floor_area == 900

    # -- Flr Area Weighted
    assert z3.clearance_height == (750 + 2400) / 900
    assert z3.spec_heat_cap == (39_600 + 57_600) / 900


def test_Zone_sum_with_empty_params(reset_bldg_segment_count):
    z1 = PHX.bldg_segment.Zone()
    z2 = PHX.bldg_segment.Zone()
    z3 = PHX.bldg_segment.Zone()

    z4 = sum([z1, z2, z3])
    assert z4
    assert z4 != z1 and z4 != z2 and z4 != z3

    z5 = sum([z1, z2, z3], start=PHX.bldg_segment.Zone())
    assert z5
    assert z5 != z1 and z5 != z2 and z5 != z3
