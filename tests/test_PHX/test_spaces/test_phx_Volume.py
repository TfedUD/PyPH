import PHX.spaces


def test_Volume_basics(floor_segments):
    # -- Setup the Floor first
    new_flr = PHX.spaces.Floor()
    new_flr.add_new_floor_segment(floor_segments[2])

    assert new_flr.display_name == "103-A Third Floor Segment"

    # -- Create the new Volume
    new_vol = PHX.spaces.Volume()
    new_vol.add_Floor(new_flr)

    assert new_vol.space_name == "A Third Floor Segment"
    assert new_vol.space_number == 103
    assert new_vol.display_name == "103-A Third Floor Segment"
    assert new_vol.host_zone_identifier == "GHI-789"

    # -- Reset the Volume attributes by changing the floor
    new_flr = PHX.spaces.Floor()
    new_flr.add_new_floor_segment(floor_segments[1])
    new_vol.add_Floor(new_flr)

    assert new_vol.space_name == "A Second Floor Segment"
    assert new_vol.space_number == 102
    assert new_vol.display_name == "102-A Second Floor Segment"
    assert new_vol.host_zone_identifier == "DEF-456"


def test_Volume_floor_areas(floor_segments):
    # -- Setup the Floor first
    new_flr = PHX.spaces.Floor()
    flr_2 = floor_segments[2]
    new_flr.add_new_floor_segment(flr_2)

    # -- Create the new Volume
    new_vol = PHX.spaces.Volume()
    new_vol.add_Floor(new_flr)

    # -- Check the floor areas
    assert new_vol.floor_area_gross == 300

    # -- Add another Floor Segment
    flr_3 = floor_segments[3]
    new_flr.add_new_floor_segment(flr_3)
    assert new_vol.floor_area_gross == 300 + 400
    assert new_vol.floor_area_weighted == (300 * 1) + (400 * 1)

    # -- Apply some weighting factors to the FloorSegments
    flr_2.weighting_factor = 0.5
    assert new_vol.floor_area_gross == 300 + 400
    assert new_vol.floor_area_weighted == (300 * 0.5) + (400 * 1)

    flr_3.weighting_factor = 0.6
    assert new_vol.floor_area_gross == 300 + 400
    assert new_vol.floor_area_weighted == (300 * 0.5) + (400 * 0.6)


def test_Volume_Clg_Heights(floor_segments):
    # -- Setup the Floor first
    new_flr = PHX.spaces.Floor()
    flr_2 = floor_segments[2]
    flr_3 = floor_segments[3]
    new_flr.add_new_floor_segment([flr_2, flr_3])

    # -- Create the new Volume
    new_vol = PHX.spaces.Volume()
    new_vol.add_Floor(new_flr)
    new_vol.volume = (flr_2.floor_area_gross * 2.5) + (flr_3.floor_area_gross * 2.5)

    assert new_vol.volume == (flr_2.floor_area_gross * 2.5) + (
        flr_3.floor_area_gross * 2.5
    )
    assert new_vol.average_ceiling_height == 2.5
