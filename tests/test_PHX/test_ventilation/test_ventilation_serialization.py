import PHX.ventilation
import PHX.loads


def test_Load_Ventilation_serialization(reset_ventilation):
    o1 = PHX.loads.Load_Ventilation()
    d = o1.to_dict()

    o2 = PHX.loads.Load_Ventilation.from_dict(d)

    assert d == o2.to_dict()


def test_SpaceVentilation_serialization(reset_ventilation):
    o1 = PHX.ventilation.SpaceVentilation()
    d = o1.to_dict()

    o2 = PHX.ventilation.SpaceVentilation.from_dict(d)

    assert d == o2.to_dict()
