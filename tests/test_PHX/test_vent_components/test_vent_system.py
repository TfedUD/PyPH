import PHX.ventilation_components


def test_vent_system():
    s1 = PHX.ventilation_components.Ventilation_System()
    s2 = PHX.ventilation_components.Ventilation_System()

    assert s1 and s2
    assert s1 != s2
    assert s1.id != s2.id
    assert s2.id == s1.id + 1


def test_default_vent_system():
    s1 = PHX.ventilation_components.Ventilation_System.default()
    s2 = PHX.ventilation_components.Ventilation_System.default()

    assert s1 and s2
    assert s1 == s2
    assert s1.id == s2.id
