import PHX.appliances


def test_dishwasher_serialization():
    app_1 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_clothes_washer_serialization():
    app_1 = PHX.appliances.Appliance.PHIUS_Clothes_Washer()
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_clothes_dryer_serialization():
    app_1 = PHX.appliances.Appliance.PHIUS_Clothes_Dryer()
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_cooktop_serialization():
    app_1 = PHX.appliances.Appliance.PHIUS_Cooktop()
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_fridge_serialization():
    app_1 = PHX.appliances.Appliance.PHIUS_Fridge()
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_freezer_serialization():
    app_1 = PHX.appliances.Appliance.PHIUS_Freezer()
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_combo_fridge_serialization():
    app_1 = PHX.appliances.Appliance.PHIUS_Combo_Fridge()
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_PHIUS_lighting_int_serialization_basic():
    app_1 = PHX.appliances.Appliance.PHIUS_Lighting_Int()
    d = app_1.to_dict()

    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_PHIUS_lighting_int_serialization_custom():
    app_1 = PHX.appliances.Appliance.PHIUS_Lighting_Int(
        energy_demand=123,
        energy_demand_per_use=456,
        combined_energy_facor=789,
    )
    d = app_1.to_dict()

    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_PHIUS_lighing_ext_serialization_basic():
    app_1 = PHX.appliances.Appliance.PHIUS_Lighting_Ext()
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_PHIUS_lighing_ext_serialization_custom():
    app_1 = PHX.appliances.Appliance.PHIUS_Lighting_Ext(
        energy_demand=123,
        energy_demand_per_use=456,
        combined_energy_facor=789,
    )
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_PHIUS_MEL_serialization_basic():
    app_1 = PHX.appliances.Appliance.PHIUS_MEL()
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2


def test_PHIUS_MEL_serialization_custom():
    app_1 = PHX.appliances.Appliance.PHIUS_MEL(
        energy_demand=123,
        energy_demand_per_use=456,
        combined_energy_facor=789,
    )
    d = app_1.to_dict()
    app_2 = PHX.appliances.Appliance.from_dict(d)
    assert d == app_2.to_dict()
    assert app_1 == app_2
