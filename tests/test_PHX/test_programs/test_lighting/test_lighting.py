import PHX.lighting
import PHX.schedules


def test_lighting_unique_key():

    # -- When values are the same
    l1 = PHX.lighting.SpaceLighting()
    l2 = PHX.lighting.SpaceLighting()

    assert l1.unique_key == l2.unique_key

    l1 = PHX.lighting.SpaceLighting.default()
    l2 = PHX.lighting.SpaceLighting.default()

    assert l1.unique_key == l2.unique_key

    # -- When name values are different
    l1 = PHX.lighting.SpaceLighting()
    l1.name = "test"
    l2 = PHX.lighting.SpaceLighting()
    l2.name = "not_test"

    assert l1.unique_key != l2.unique_key

    # -- When illumination values are different
    l1 = PHX.lighting.SpaceLighting()
    l1.loads.space_illumination = 1
    l2 = PHX.lighting.SpaceLighting()
    l2.loads.space_illumination = 2

    assert l1.unique_key != l2.unique_key

    # -- When power-density values are different
    l1 = PHX.lighting.SpaceLighting()
    l1.loads.installed_power_density = 1
    l2 = PHX.lighting.SpaceLighting()
    l2.loads.installed_power_density = 2

    assert l1.unique_key != l2.unique_key

    # -- When utilization values are different
    l1 = PHX.lighting.SpaceLighting()
    l1.schedule = PHX.schedules.Schedule_Lighting()
    l2 = PHX.lighting.SpaceLighting()
    l2.schedule = PHX.schedules.Schedule_Lighting()

    assert l1.unique_key == l2.unique_key
