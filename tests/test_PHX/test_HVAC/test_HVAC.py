import PHX.hvac


def test_HVAC(reset_hvac):
    o = PHX.hvac.HVAC()

    assert len(o.lSystem) == 1
    assert o.default_system


def test_add_HVAC_System(reset_hvac):
    o = PHX.hvac.HVAC()

    assert len(o.lSystem) == 1

    s1 = PHX.hvac.HVAC_System()
    o.add_system(s1)

    assert len(o.lSystem) == 2
    assert s1 in o.lSystem
