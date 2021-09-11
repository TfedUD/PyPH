import PHX.lighting
import PHX.utilization_patterns


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
    l1.space_illumination = 1
    l2 = PHX.lighting.SpaceLighting()
    l2.space_illumination = 2

    assert l1.unique_key != l2.unique_key

    # -- When power-density values are different
    l1 = PHX.lighting.SpaceLighting()
    l1.installed_power_density = 1
    l2 = PHX.lighting.SpaceLighting()
    l2.installed_power_density = 2

    assert l1.unique_key != l2.unique_key

    # -- When utilization values are different
    l1 = PHX.lighting.SpaceLighting()
    l1.utilization = PHX.utilization_patterns.UtilPat_Lighting()
    l2 = PHX.lighting.SpaceLighting()
    l2.utilization = PHX.utilization_patterns.UtilPat_Lighting()

    assert l1.unique_key == l2.unique_key
