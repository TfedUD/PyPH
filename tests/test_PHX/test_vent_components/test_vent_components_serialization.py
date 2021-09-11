import PHX.ventilation_components


def test_duct_segment_serialization(reset_vent_components):
    o1 = PHX.ventilation_components.Ventilation_Duct_Segment()
    d = o1.to_dict()

    o2 = PHX.ventilation_components.Ventilation_Duct_Segment.from_dict(d)

    assert d == o2.to_dict()


def test_default_duct_segment_serialization(reset_vent_components):
    o1 = PHX.ventilation_components.Ventilation_Duct_Segment.default()
    d = o1.to_dict()

    o2 = PHX.ventilation_components.Ventilation_Duct_Segment.from_dict(d)

    assert d == o2.to_dict()


def test_duct_serialization(reset_vent_components):
    o1 = PHX.ventilation_components.Ventilation_Duct()
    d = o1.to_dict()

    o2 = PHX.ventilation_components.Ventilation_Duct.from_dict(d)

    assert d == o2.to_dict()


def test_default_duct_serialization(reset_vent_components):
    o1 = PHX.ventilation_components.Ventilation_Duct.default()
    d = o1.to_dict()

    o2 = PHX.ventilation_components.Ventilation_Duct.from_dict(d)

    assert d == o2.to_dict()


def test_unit_serialization(reset_vent_components):
    o1 = PHX.ventilation_components.Ventilator()
    d = o1.to_dict()

    o2 = PHX.ventilation_components.Ventilator.from_dict(d)

    assert d == o2.to_dict()


def test_default_unit_serialization(reset_vent_components):
    o1 = PHX.ventilation_components.Ventilator.default()
    d = o1.to_dict()

    o2 = PHX.ventilation_components.Ventilator.from_dict(d)

    assert d == o2.to_dict()


def test_system_serialization(reset_vent_components):
    o1 = PHX.ventilation_components.Ventilation_System()
    d = o1.to_dict()

    o2 = PHX.ventilation_components.Ventilation_System.from_dict(d)

    assert d == o2.to_dict()


def test_default_sytem_serialization(reset_vent_components):
    o1 = PHX.ventilation_components.Ventilation_System.default()
    d = o1.to_dict()

    o2 = PHX.ventilation_components.Ventilation_System.from_dict(d)

    assert d == o2.to_dict()


def test_PH_Params_serialization(reset_vent_components):
    o1 = PHX.ventilation_components.Ventilator_PH_Parameters()
    d = o1.to_dict()

    o2 = PHX.ventilation_components.Ventilator_PH_Parameters.from_dict(d)

    assert d == o2.to_dict()
