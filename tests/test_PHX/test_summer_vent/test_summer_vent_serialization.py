import PHX.summer_ventilation


def test_summer_vent_serialization():
    o1 = PHX.summer_ventilation.SummerVent()
    d = o1.to_dict()

    o2 = PHX.summer_ventilation.SummerVent.from_dict(d)

    assert d == o2.to_dict()
