import PHX.programs.ventilation


def test_SpaceVentilation(reset_ventilation):
    sv1 = PHX.programs.ventilation.SpaceVentilation()
    sv2 = PHX.programs.ventilation.SpaceVentilation()

    assert sv1 and sv2
    assert sv1 != sv2
    assert sv1.id != sv2.id


def test_add_SpaceVentilations(reset_ventilation):
    sv1 = PHX.programs.ventilation.SpaceVentilation()
    sv2 = PHX.programs.ventilation.SpaceVentilation()

    sv3 = sv1 + sv2
    assert sv3 == sv1 and sv3 != sv2
