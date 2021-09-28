import PHX.spaces
import PHX.programs.ventilation
import pytest

# ---- Floor Segments
# -------------------------------------------------------------------------------
def test_floor_segment_basics():
    # -- Make a Floor segment
    seg_1 = PHX.spaces.FloorSegment()
    vent_1 = PHX.programs.ventilation.RoomVentilation()

    seg_1.weighting_factor = 1.0
    seg_1.space_name = "A First Segment"
    seg_1.space_number = 100

    seg_1.non_res_lighting = None
    seg_1.non_res_motion = None
    seg_1.non_res_usage = None

    seg_1.ventilation = vent_1

    # -- Make another one
    seg_2 = PHX.spaces.FloorSegment()
    vent_2 = PHX.programs.ventilation.RoomVentilation()

    seg_2.weighting_factor = 1.0
    seg_2.space_name = "A First Segment"
    seg_2.space_number = 100

    seg_2.non_res_lighting = None
    seg_2.non_res_motion = None
    seg_2.non_res_usage = None

    seg_2.ventilation = vent_2

    assert seg_1 and seg_2
    assert seg_1 != seg_2
    assert str(seg_1.space_number) in str(seg_1)
    assert str(seg_2.space_number) in str(seg_2)


def test_floor_segment_area_weighting_works():
    seg_1 = PHX.spaces.FloorSegment()
    seg_1.weighting_factor = 1.0
    seg_1.floor_area_gross = 200
    assert seg_1.floor_area_weighted == 200

    seg_1.weighting_factor = 0.5
    seg_1.floor_area_gross = 200
    assert seg_1.floor_area_weighted == 100

    seg_1.weighting_factor = 0.1
    seg_1.floor_area_gross = 200
    assert seg_1.floor_area_weighted == 20

    seg_1.weighting_factor = 50
    seg_1.floor_area_gross = 200
    assert seg_1.floor_area_weighted == 100

    seg_1.weighting_factor = None
    seg_1.floor_area_gross = None
    assert seg_1.floor_area_weighted == 100


def test_floor_segment_input_errors():
    seg_1 = PHX.spaces.FloorSegment()

    with pytest.raises(PHX.spaces.FloorAreaWeightingInputError):
        seg_1.floor_area_weighted = 200

    with pytest.raises(PHX.spaces.WeightingFactorInputError):
        seg_1.weighting_factor = "not a factor"
        seg_1.weighting_factor = [1, 2, 3]

    with pytest.raises(PHX.spaces.FloorAreaGrossInputError):
        seg_1.floor_area_gross = "not a floor area"
        seg_1.floor_area_gross = [1, 2, 3]

    with pytest.raises(PHX.spaces.RoomVentilationInputError):
        seg_1.ventilation = "not a ventilation object"
