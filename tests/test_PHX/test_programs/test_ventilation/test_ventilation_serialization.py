import PHX.programs.ventilation
import PHX.programs.loads


def test_Load_Ventilation_serialization(reset_ventilation):
    o1 = PHX.programs.loads.Load_Ventilation()
    d = o1.to_dict()

    o2 = PHX.programs.loads.Load_Ventilation.from_dict(d)

    assert d == o2.to_dict()


def test_RoomVentilation_serialization(reset_ventilation):
    o1 = PHX.programs.ventilation.RoomVentilation()
    d = o1.to_dict()

    o2 = PHX.programs.ventilation.RoomVentilation.from_dict(d)

    assert d == o2.to_dict()
