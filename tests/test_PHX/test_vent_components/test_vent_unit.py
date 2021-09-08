import PHX.ventilation_components


def test_vent_unit(reset_vent_components):
    u1 = PHX.ventilation_components.Ventilator()
    u2 = PHX.ventilation_components.Ventilator()

    assert u1 and u2
    assert u1.id != u2.id


def test_default_vent_unit(reset_vent_components):
    u1 = PHX.ventilation_components.Ventilator.default()
    u2 = PHX.ventilation_components.Ventilator.default()

    assert u1 and u2
    assert u1.id == u2.id
