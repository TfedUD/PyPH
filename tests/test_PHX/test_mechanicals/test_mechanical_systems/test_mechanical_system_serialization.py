import PHX.mechanicals.systems


def test_Mechanicals_serialization_empty(reset_mechanicals):
    o1 = PHX.mechanicals.systems.Mechanicals()
    d = o1.to_dict()

    o2 = PHX.mechanicals.systems.Mechanicals.from_dict(d)
    assert d == o2.to_dict()


def test_Mechanicals_serialization_with_system(reset_mechanicals):
    o1 = PHX.mechanicals.systems.Mechanicals()
    s1 = PHX.mechanicals.systems.MechanicalSystem()
    o1.add_system(s1)
    d = o1.to_dict()

    o2 = PHX.mechanicals.systems.Mechanicals.from_dict(d)
    assert d == o2.to_dict()


def test_MechanicalSystem_serialization(reset_mechanicals):
    o1 = PHX.mechanicals.systems.MechanicalSystem()
    d = o1.to_dict()

    o2 = PHX.mechanicals.systems.MechanicalSystem.from_dict(d)
    assert d == o2.to_dict()


def test_MechanicalSystem_default_Ventilation_serialization(reset_mechanicals):
    o1 = PHX.mechanicals.systems.MechanicalSystem.default_ventilation()
    d = o1.to_dict()

    o2 = PHX.mechanicals.systems.MechanicalSystem.from_dict(d)
    assert d == o2.to_dict()
