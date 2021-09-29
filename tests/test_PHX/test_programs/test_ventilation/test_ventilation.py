import PHX.programs.ventilation


def test_RoomVentilation(reset_ventilation):
    sv1 = PHX.programs.ventilation.RoomVentilation()
    sv2 = PHX.programs.ventilation.RoomVentilation()

    assert sv1 and sv2
    assert sv1 != sv2
    assert sv1.id != sv2.id


def test_add_RoomVentilations(reset_ventilation):
    sv1 = PHX.programs.ventilation.RoomVentilation()
    sv2 = PHX.programs.ventilation.RoomVentilation()

    sv3 = sv1 + sv2
    assert sv3 == sv1 and sv3 != sv2
