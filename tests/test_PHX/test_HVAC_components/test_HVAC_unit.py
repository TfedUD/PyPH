import PHX.hvac_components


def test_vent_unit(reset_vent_components):
    u1 = PHX.hvac_components.HVAC_Ventilator()
    u2 = PHX.hvac_components.HVAC_Ventilator()

    assert u1 and u2
    assert u1.id != u2.id


def test_default_vent_unit(reset_vent_components):
    u1 = PHX.hvac_components.HVAC_Ventilator.default()
    u2 = PHX.hvac_components.HVAC_Ventilator.default()

    assert u1 and u2
    assert u1.id == u2.id
