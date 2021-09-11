import PHX.hvac


def test_hvac_device(reset_hvac):
    d1 = PHX.hvac.HVAC_Device()
    d2 = PHX.hvac.HVAC_Device()

    assert d1 and d2
    assert d1 != d2
    assert d1.id != d2.id