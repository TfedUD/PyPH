import PHX._base


class Appliance(PHX._base._Base):
    def __init__(self):
        self.reference_quantity = 2  # Zone Occupants
        self.quantity = 1
        self.in_conditioned_space = True
        self.reference_energy_norm = 2  # Year
        self.energy_demand = 100  # kwh
        self.energy_demand_per_use = 100  # kwh/use
        self.combined_energy_facor = 0  # CEF

        # -- Dishwasher
        self.dishwasher_capacity_type = 1  # standard
        self.dishwasher_capacity = 12
        self.dishwasher_water_connection = 2  # Cold Water

        # -- Laundry Washer
        self.washer_capacity = 0.0814  # m3
        self.washer_modified_energy_factor = 2.38
        self.washer_connection = 1  # DHW Connection

        # -- Laundry Dryer
        self.dryer_type = 1
        self.dryer_gas_consumption = 0  # kWh
        self.dryer_gas_efficiency_factor = 2.67
        self.dryer_field_utilization_factor_type = 1
        self.dryer_field_utilization_factor = 1.18

        # -- Cooktop
        self.cooktop_type = 1  # Electric

        # -- PHIUS Lighting
        self.lighting_frac_high_efficiency = 1

    @classmethod
    def PHIUS_dishwasher(cls):
        app = cls()

        # -- Standard
        app.reference_quantity = 2  # Zone Occupants
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 2  # Year
        app.energy_demand = 260  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        # -- Specific
        app.dishwasher_capacity_type = 1  # standard
        app.dishwasher_capacity = 12
        app.dishwasher_water_connection = 2  # Cold Water

        return app
