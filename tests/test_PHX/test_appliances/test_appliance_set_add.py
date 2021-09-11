import PHX.appliances


def test_basic_add():
    s1 = PHX.appliances.ApplianceSet()
    s2 = PHX.appliances.ApplianceSet()

    assert len(s1) == 0
    assert len(s2) == 0

    # -- Add two sets
    s1.add_appliances_to_set(PHX.appliances.Appliance.PHIUS_Dishwasher())
    s3 = s1 + s2
    assert len(s3) == 1

    # -- Add a not-a-set
    s4 = None
    s5 = s3 + s4
    assert len(s5) == 1
