import PHX.ventilation


def test_AirFlowRates_serialization(reset_ventilation):
    o1 = PHX.ventilation.AirflowRates()
    d = o1.to_dict()

    o2 = PHX.ventilation.AirflowRates.from_dict(d)

    assert d == o2.to_dict()


def test_SpaceVentilation_serialization(reset_ventilation):
    o1 = PHX.ventilation.SpaceVentilation()
    d = o1.to_dict()

    o2 = PHX.ventilation.SpaceVentilation.from_dict(d)

    assert d == o2.to_dict()
