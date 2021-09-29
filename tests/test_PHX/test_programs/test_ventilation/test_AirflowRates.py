import PHX.programs.ventilation
import PHX.programs.loads


def test_Load_Ventilation(reset_ventilation):
    af1 = PHX.programs.loads.Load_Ventilation()
    af1.supply = 200
    af1.extract = 300
    af1.transfer = 400

    af2 = PHX.programs.loads.Load_Ventilation()
    af2.supply = 500
    af2.extract = 600
    af2.transfer = 700

    assert af1 and af2
    assert af1 != af2

    assert str(af1.supply) in repr(af1)
    assert str(af2.supply) in repr(af2)

    assert str(af1.supply) in str(af1)
    assert str(af2.supply) in str(af2)


def test_add_Load_Ventilation(reset_ventilation):
    af1 = PHX.programs.loads.Load_Ventilation()
    af1.supply = 200
    af1.extract = 600
    af1.transfer = 400

    af2 = PHX.programs.loads.Load_Ventilation()
    af2.supply = 500
    af2.extract = 300
    af2.transfer = 700

    af3 = af1.join(af2)
    assert af3.supply == 500
    assert af3.extract == 600
    assert af3.transfer == 700
