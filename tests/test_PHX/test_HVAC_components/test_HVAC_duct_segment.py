import PHX.hvac_components


def test_duct_segment(reset_vent_components):
    c1 = PHX.hvac_components.HVAC_Duct_Segment()
    c2 = PHX.hvac_components.HVAC_Duct_Segment()

    assert c1 != c2


def test_default_duct_segment(reset_vent_components):
    c1 = PHX.hvac_components.HVAC_Duct_Segment.default()
    c2 = PHX.hvac_components.HVAC_Duct_Segment.default()

    assert c1 == c2
