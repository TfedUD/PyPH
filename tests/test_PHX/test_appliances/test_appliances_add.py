import PHX.appliances
import pytest

# -- Basic / General Appliances
def test_add_Nones():
    app1 = PHX.appliances.Appliance()
    app2 = None

    # Works in this order
    app3 = app1 + app2
    assert app1 == app3

    # And works in the other order
    app4 = app2 + app1
    assert app4 == app1


def test_generic_appliance_add():
    app_1 = PHX.appliances.Appliance()
    app_1.type = 1
    app_1.reference_energy_norm = 2
    app_1.energy_demand = 100
    app_1.energy_demand_per_use = 100
    app_1.combined_energy_facor = 10

    app_2 = PHX.appliances.Appliance()
    app_2.type = 1
    app_2.reference_energy_norm = 2
    app_2.energy_demand = 200
    app_2.energy_demand_per_use = 200
    app_2.combined_energy_facor = 20

    app_3 = app_1 + app_2
    assert app_3.type == 1
    assert app_3.reference_energy_norm == 2
    assert app_3.energy_demand == 150
    assert app_3.energy_demand_per_use == 150
    assert app_3.combined_energy_facor == 15


def test_unequal_reference_energy_norm():
    app_1 = PHX.appliances.Appliance()
    app_1.reference_energy_norm = 1

    app_2 = PHX.appliances.Appliance()
    app_2.reference_energy_norm = 2

    with pytest.raises(PHX.appliances.ApplianceTypeMismatchError):
        app_1 + app_2


def test_unkown_type():
    app1 = PHX.appliances.Appliance()
    app1.type = 999_999
    app2 = PHX.appliances.Appliance()
    app2.type = 999_999

    with pytest.raises(PHX.appliances.ApplianceAdditionError):
        app1 + app2


def test_unequal_types():
    app_1 = PHX.appliances.Appliance()
    app_1.type = 1
    app_2 = PHX.appliances.Appliance()
    app_2.type = 2

    with pytest.raises(PHX.appliances.ApplianceAdditionError):
        app_1 + app_2


# -- Dishwasher
def test_add_PHIUS_dishwashers():
    dw1 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw1.dishwasher_capacity_type = 1
    dw1.dishwasher_capacity = 10
    dw1.dishwasher_water_connection = 2

    dw2 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw2.dishwasher_capacity_type = 1
    dw2.dishwasher_capacity = 10
    dw2.dishwasher_water_connection = 2

    # Add the two appliances
    dw3 = dw1 + dw2
    assert dw3.type == 1
    assert dw3.quantity == 2
    assert dw3.dishwasher_capacity_type == 1
    assert dw3.dishwasher_capacity == 10
    assert dw3.dishwasher_water_connection == 2

    # Add an third one
    dw4 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    dw4.dishwasher_capacity_type == 1
    dw4.dishwasher_capacity = 25
    dw4.dishwasher_water_connection == 2

    dw5 = dw3 + dw4
    assert dw5.type == 1
    assert dw5.quantity == 3
    assert dw5.dishwasher_capacity_type == 1
    assert dw5.dishwasher_capacity == (10 + 10 + 25) / 3
    assert dw5.dishwasher_water_connection == 2


def test_add_dw_mismatch_types():
    app_1 = PHX.appliances.Appliance.PHIUS_Dishwasher()
    app_2 = PHX.appliances.Appliance.PHIUS_Dishwasher()

    # Diffetent Capacity Types
    app_1.dishwasher_capacity_type = 1
    app_2.dishwasher_capacity_type = 2
    app_1.dishwasher_water_connection = 2
    app_2.dishwasher_water_connection = 2

    with pytest.raises(PHX.appliances.ApplianceTypeMismatchError):
        app_1 + app_2

    # Try with different water connections
    app_1.dishwasher_capacity_type = 1
    app_2.dishwasher_capacity_type = 1
    app_1.dishwasher_water_connection = 1
    app_2.dishwasher_water_connection = 2

    with pytest.raises(PHX.appliances.ApplianceTypeMismatchError):
        app_1 + app_2


# -- Clothes Washer
def test_add_PHIUS_washer():
    app_1 = PHX.appliances.Appliance.PHIUS_Clothes_Washer()
    app_1.washer_capacity = 2
    app_1.washer_modified_energy_factor = 5
    app_1.washer_connection = 1
    app_1.washer_utilization_factor = 1

    app_2 = PHX.appliances.Appliance.PHIUS_Clothes_Washer()
    app_2.washer_capacity = 4
    app_2.washer_modified_energy_factor = 10
    app_2.washer_connection = 1
    app_2.washer_utilization_factor = 1

    # Add the two appliances
    app_3 = app_1 + app_2
    assert app_3.type == 2
    assert app_3.quantity == 2
    assert app_3.washer_capacity == 3
    assert app_3.washer_modified_energy_factor == 7.5
    assert app_3.washer_connection == 1
    assert app_3.washer_utilization_factor == 1


def test_add_PHIUS_washer_unequal_types():
    app_1 = PHX.appliances.Appliance.PHIUS_Clothes_Washer()
    app_2 = PHX.appliances.Appliance.PHIUS_Clothes_Washer()

    app_1.washer_connection = 1
    app_2.washer_connection = 2  # <--

    with pytest.raises(PHX.appliances.ApplianceTypeMismatchError):
        app_1 + app_2


# -- Clothes Dryer
def test_add_PHIUS_dryer():
    app_1 = PHX.appliances.Appliance.PHIUS_Clothes_Dryer()
    app_1.dryer_type = 4
    app_1.dryer_gas_consumption = 10
    app_1.dryer_gas_efficiency_factor = 4
    app_1.dryer_field_utilization_factor_type = 1
    app_1.dryer_field_utilization_factor = 5

    app_2 = PHX.appliances.Appliance.PHIUS_Clothes_Dryer()
    app_2.dryer_type = 4
    app_2.dryer_gas_consumption = 20
    app_2.dryer_gas_efficiency_factor = 2
    app_2.dryer_field_utilization_factor_type = 1
    app_2.dryer_field_utilization_factor = 10

    # Add the two appliances
    app_3 = app_1 + app_2
    assert app_3.type == 3
    assert app_3.quantity == 2
    assert app_3.dryer_gas_consumption == 15
    assert app_3.dryer_gas_efficiency_factor == 3
    assert app_3.dryer_field_utilization_factor_type == 1
    assert app_3.dryer_field_utilization_factor == 7.5


def test_add_PHIUS_dryer_unequal_types():
    app_1 = PHX.appliances.Appliance.PHIUS_Clothes_Dryer()
    app_2 = PHX.appliances.Appliance.PHIUS_Clothes_Dryer()

    app_1.dryer_type = 1
    app_1.dryer_type = 2
    app_2.dryer_field_utilization_factor_type = 1
    app_2.dryer_field_utilization_factor_type = 1

    with pytest.raises(PHX.appliances.ApplianceTypeMismatchError):
        app_1 + app_2

    app_1.dryer_type = 1
    app_1.dryer_type = 1
    app_2.dryer_field_utilization_factor_type = 1
    app_2.dryer_field_utilization_factor_type = 2

    with pytest.raises(PHX.appliances.ApplianceTypeMismatchError):
        app_1 + app_2


# -- Cooktop
def test_add_PHIUS_cooktop_unequal_types():
    app_1 = PHX.appliances.Appliance.PHIUS_Cooktop()
    app_2 = PHX.appliances.Appliance.PHIUS_Cooktop()

    app_1.cooktop_type = 1
    app_1.cooktop_type = 2

    with pytest.raises(PHX.appliances.ApplianceTypeMismatchError):
        app_1 + app_2


# -- Lighting & MEL
def test_add_PHIUS_Lighting_Int():
    app_1 = PHX.appliances.Appliance.PHIUS_Lighting_Int()
    app_2 = PHX.appliances.Appliance.PHIUS_Lighting_Int()

    # Test basic usage
    app_1.lighting_frac_high_efficiency = 2
    app_2.lighting_frac_high_efficiency = 4

    app_3 = app_1 + app_2
    assert app_3.quantity == 2
    assert app_3.lighting_frac_high_efficiency == 3

    # Test User-Defined + None
    app_1.user_defined_total = 200
    app_2.user_defined_total = None

    app_4 = app_1 + app_2
    assert app_4.quantity == 1
    assert app_4.lighting_frac_high_efficiency == 3
    assert app_4.reference_quantity == 5
    assert app_4.user_defined_total == 200
    assert app_4.energy_demand == 100
    assert app_4.energy_demand_per_use == 100

    # Test 2 User-Defined
    app_2.user_defined_total = 400
    app_5 = app_1 + app_2
    assert app_5.quantity == 1
    assert app_5.lighting_frac_high_efficiency == 3
    assert app_5.reference_quantity == 5
    assert app_5.user_defined_total == 600
    assert app_5.energy_demand == 100
    assert app_5.energy_demand_per_use == 100


def test_add_PHIUS_Lighting_Ext():
    app_1 = PHX.appliances.Appliance.PHIUS_Lighting_Ext()
    app_2 = PHX.appliances.Appliance.PHIUS_Lighting_Ext()

    # Test basic usage
    app_1.lighting_frac_high_efficiency = 2
    app_2.lighting_frac_high_efficiency = 4

    app_3 = app_1 + app_2
    assert app_3.quantity == 2
    assert app_3.lighting_frac_high_efficiency == 3

    # Test User-Defined + None
    app_1.user_defined_total = 200
    app_2.user_defined_total = None

    app_4 = app_1 + app_2
    assert app_4.quantity == 1
    assert app_4.lighting_frac_high_efficiency == 3
    assert app_4.reference_quantity == 5
    assert app_4.user_defined_total == 200
    assert app_4.energy_demand == 100
    assert app_4.energy_demand_per_use == 100

    # Test 2 User-Defined
    app_2.user_defined_total = 400
    app_5 = app_1 + app_2
    assert app_5.quantity == 1
    assert app_5.lighting_frac_high_efficiency == 3
    assert app_5.reference_quantity == 5
    assert app_5.user_defined_total == 600
    assert app_5.energy_demand == 100
    assert app_5.energy_demand_per_use == 100


def test_add_PHIUS_MEL():
    app_1 = PHX.appliances.Appliance.PHIUS_MEL()
    app_2 = PHX.appliances.Appliance.PHIUS_MEL()

    app_3 = app_1 + app_2
    assert app_3.quantity == 2

    # Test User-Defined + None
    app_1.user_defined_total = 200
    app_2.user_defined_total = None

    app_4 = app_1 + app_2
    assert app_4.quantity == 1
    assert app_4.reference_quantity == 5
    assert app_4.user_defined_total == 200
    assert app_4.energy_demand == 100
    assert app_4.energy_demand_per_use == 100

    # Test 2 User-Defined
    app_2.user_defined_total = 400
    app_5 = app_1 + app_2
    assert app_5.quantity == 1
    assert app_5.reference_quantity == 5
    assert app_5.user_defined_total == 600
    assert app_5.energy_demand == 100
    assert app_5.energy_demand_per_use == 100
