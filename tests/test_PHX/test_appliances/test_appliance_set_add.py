import PHX.appliances


def test_basic_add():
    s1 = PHX.appliances.ApplianceSet()
    s2 = PHX.appliances.ApplianceSet()

    assert len(s1) == 0
    assert len(s2) == 0

    # -- Add two sets
    s1.add_appliance(PHX.appliances.Appliance.PHIUS_Dishwasher())
    s3 = s1 + s2
    assert len(s3) == 1

    # -- Add a not-a-set
    s4 = None
    s5 = s3 + s4
    assert len(s5) == 1


def test_add_appliances():
    s1 = PHX.appliances.ApplianceSet()
    s2 = PHX.appliances.ApplianceSet()

    dw1 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw1.dishwasher_capacity_type = 1
    dw1.dishwasher_capacity = 10
    dw1.dishwasher_water_connection = 2

    dw2 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw2.dishwasher_capacity_type = 1
    dw2.dishwasher_capacity = 20
    dw2.dishwasher_water_connection = 2

    s1.add_appliance(dw1)
    s2.add_appliance(dw2)

    s3 = s1 + s2
    assert len(s3) == 1
    assert s3.dishwasher.type == 1
    assert s3.dishwasher.quantity == 2
    assert s3.dishwasher.dishwasher_capacity_type == 1
    assert s3.dishwasher.dishwasher_capacity == 15
    assert s3.dishwasher.dishwasher_water_connection == 2


def test_add_not_appliances():
    s1 = PHX.appliances.ApplianceSet()
    s2 = PHX.appliances.ApplianceSet()

    dw1 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw1.dishwasher_capacity_type = 1
    dw1.dishwasher_capacity = 10
    dw1.dishwasher_water_connection = 2

    s1.add_appliance(dw1)
    s2.dishwasher = None

    # Try in order
    s3 = s1 + s2
    assert len(s3) == 1
    assert s3.dishwasher.type == 1
    assert s3.dishwasher.quantity == 1
    assert s3.dishwasher.dishwasher_capacity_type == 1
    assert s3.dishwasher.dishwasher_capacity == 10
    assert s3.dishwasher.dishwasher_water_connection == 2

    # Try reversing the order
    s4 = s2 + s1
    assert len(s4) == 1
    assert s4.dishwasher.type == 1
    assert s4.dishwasher.quantity == 1
    assert s4.dishwasher.dishwasher_capacity_type == 1
    assert s4.dishwasher.dishwasher_capacity == 10
    assert s4.dishwasher.dishwasher_water_connection == 2


def test_set_sum():
    s1 = PHX.appliances.ApplianceSet()
    s2 = PHX.appliances.ApplianceSet()
    s3 = PHX.appliances.ApplianceSet()

    dw1 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw1.dishwasher_capacity_type = 1
    dw1.dishwasher_capacity = 10
    dw1.dishwasher_water_connection = 2

    dw2 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw2.dishwasher_capacity_type = 1
    dw2.dishwasher_capacity = 20
    dw2.dishwasher_water_connection = 2

    dw3 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw3.dishwasher_capacity_type = 1
    dw3.dishwasher_capacity = 20
    dw3.dishwasher_water_connection = 2

    s1.add_appliance(dw1)
    s2.add_appliance(dw2)
    s3.add_appliance(dw3)

    s4 = sum([s1, s2, s3])
    assert len(s4) == 1
    assert s4.dishwasher.type == 1
    assert s4.dishwasher.quantity == 3
    assert s4.dishwasher.dishwasher_capacity_type == 1
    assert s4.dishwasher.dishwasher_capacity == (10 + 20 + 20) / 3
    assert s4.dishwasher.dishwasher_water_connection == 2

    s5 = sum([s3, s2, s1])
    assert len(s5) == 1
    assert s5.dishwasher.type == 1
    assert s5.dishwasher.quantity == 3
    assert s5.dishwasher.dishwasher_capacity_type == 1
    assert s5.dishwasher.dishwasher_capacity == (10 + 20 + 20) / 3
    assert s5.dishwasher.dishwasher_water_connection == 2

    s6 = sum([s1])
    assert len(s6) == 1
    assert s6.dishwasher.type == 1
    assert s6.dishwasher.quantity == 1
    assert s6.dishwasher.dishwasher_capacity_type == 1
    assert s6.dishwasher.dishwasher_capacity == 10
    assert s6.dishwasher.dishwasher_water_connection == 2
