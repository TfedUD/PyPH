import PHX.hvac


def test_hvac_system_serialization():
    pattern_1 = PHX.hvac.HVAC_System()
    d = pattern_1.to_dict()
    pattern_2 = PHX.hvac.HVAC_System.from_dict(d)

    assert d == pattern_2.to_dict()


def test_hvac_device_serialization():
    o1 = PHX.hvac.HVAC_Device()
    d = o1.to_dict()
    o2 = PHX.hvac.HVAC_Device.from_dict(d)

    assert d == o2.to_dict()
