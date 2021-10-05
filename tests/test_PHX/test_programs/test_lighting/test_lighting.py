import PHX.programs.lighting
import PHX.programs.schedules


def test_lighting_unique_key():

    # -- When values are the same
    l1 = PHX.programs.lighting.RoomLighting()
    l2 = PHX.programs.lighting.RoomLighting()

    assert l1.unique_key == l2.unique_key

    l1 = PHX.programs.lighting.RoomLighting.default()
    l2 = PHX.programs.lighting.RoomLighting.default()

    assert l1.unique_key == l2.unique_key

    # -- When name values are different
    l1 = PHX.programs.lighting.RoomLighting()
    l1.name = "test"
    l2 = PHX.programs.lighting.RoomLighting()
    l2.name = "not_test"

    assert l1.unique_key != l2.unique_key

    # -- When illumination values are different
    l1 = PHX.programs.lighting.RoomLighting()
    l1.loads.target_lux = 1
    l2 = PHX.programs.lighting.RoomLighting()
    l2.loads.target_lux = 2

    assert l1.unique_key != l2.unique_key

    # -- When power-density values are different
    l1 = PHX.programs.lighting.RoomLighting()
    l1.loads.watts_per_area = 1
    l2 = PHX.programs.lighting.RoomLighting()
    l2.loads.watts_per_area = 2

    assert l1.unique_key != l2.unique_key

    # -- When utilization values are different
    l1 = PHX.programs.lighting.RoomLighting()
    l1.schedule = PHX.programs.schedules.Schedule_Lighting()
    l2 = PHX.programs.lighting.RoomLighting()
    l2.schedule = PHX.programs.schedules.Schedule_Lighting()

    assert l1.unique_key == l2.unique_key
