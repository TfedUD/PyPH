import PHX._base
import PHX.serialization.from_dict


class UnknownApplianceError(Exception):
    def __init__(self, _in):
        self.message = (
            'Error: Unknown Appliance "{}" with type: "{}". Please check'
            "inputs and enter a valid Appliance type.".format(_in, _in.type)
        )
        super(UnknownApplianceError, self).__init__(self.message)


class ApplianceSet(PHX._base._Base):
    """A Collection of Appliances"""

    known_types = {
        1: "dishwasher",
        2: "clothes_washer",
        3: "clothes_dryer",
        4: "fridge",
        5: "freezer",
        6: "fridge_freezer",
        7: "cooking",
        13: "PHIUS_MEL",
        14: "PHIUS_Lighting_Int",
        15: "PHIUS_Lighting_Ext",
    }

    def __init__(self):
        super(ApplianceSet, self).__init__()
        self.dishwasher = None
        self.clothes_washer = None
        self.clothes_dryer = None
        self.fridge = None
        self.freezer = None
        self.fridge_freezer = None
        self.cooking = None
        self.PHIUS_MEL = None
        self.PHIUS_Lighting_Int = None
        self.PHIUS_Lighting_Ext = None

    def add_appliance(self, _appliance):
        """Adds a (known type of) Appliance to the set"""

        if not _appliance:
            return

        app_type = self.known_types.get(_appliance.type)
        if app_type:
            setattr(self, app_type, _appliance)
        else:
            raise UnknownApplianceError(_appliance)

    @property
    def appliances(self):
        return [
            self.dishwasher,
            self.clothes_washer,
            self.clothes_dryer,
            self.fridge,
            self.freezer,
            self.fridge_freezer,
            self.cooking,
            self.PHIUS_MEL,
            self.PHIUS_Lighting_Int,
            self.PHIUS_Lighting_Ext,
        ]

    def __iter__(self):
        for _ in self.appliances:
            if not _:
                continue
            yield _

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._ApplianceSet(cls, _dict)

    def __add__(self, other):
        # type: (ApplianceSet, ApplianceSet) -> ApplianceSet

        # Not implemented yet....

        return self


class Appliance(PHX._base._Base):
    """An individual Appliance"""

    def __init__(self):
        super(Appliance, self).__init__()
        self.type = 1
        self.comment = None
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
        self.washer_utilization_factor = 1

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
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Appliance(cls, _dict)

    @classmethod
    def PHIUS_Dishwasher(cls):
        app = cls()

        # -- Standard
        app.type = 1  # dishwasher
        app.reference_quantity = 1  # PH-Case Occupants
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

    @classmethod
    def PHIUS_Clothes_Washer(cls):
        app = cls()

        # -- Standard
        app.type = 2  # dishwasher
        app.reference_quantity = 1  # PH-Case Occupants
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 2  # Year
        app.energy_demand = 116  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        # -- Specific
        app.washer_capacity = 0.0814  # m3
        app.washer_modified_energy_factor = 2.38
        app.washer_connection = 1  # DHW Connection
        app.washer_utilization_factor = 1

        return app

    @classmethod
    def PHIUS_Clothes_Dryer(cls):
        app = cls()

        # -- Standard
        app.type = 3  # Laundry - dryer
        app.reference_quantity = 1  # PH-Case Occupants
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 1  # Day/Use
        app.energy_demand = 0  # kwh
        app.energy_demand_per_use = 3.5  # kwh/use
        app.combined_energy_facor = 3.93  # CEF

        # -- Specific
        app.dryer_type = 4  # Condensation dryer
        app.dryer_gas_consumption = 0  # kWh
        app.dryer_gas_efficiency_factor = 2.67
        app.dryer_field_utilization_factor_type = 1  # Timer
        app.dryer_field_utilization_factor = 1.18

        return app

    @classmethod
    def PHIUS_Cooktop(cls):
        app = cls()

        # -- Standard
        app.type = 7  # Kitchen cooking
        app.reference_quantity = 1  # PH-Case Occupants
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 2  # Year
        app.energy_demand = 0.2  # kwh
        app.energy_demand_per_use = 0.2  # kwh/use
        app.combined_energy_facor = 0  # CEF

        # -- Specific
        app.cooktop_type = 1  # Electric

        return app

    @classmethod
    def PHIUS_Fridge(cls):
        app = cls()

        # -- Standard
        app.type = 4  # Kitchen refrigerator
        app.reference_quantity = 1  # PH-Case Occupants
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 1  # Day
        app.energy_demand = 0.28  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        return app

    @classmethod
    def PHIUS_Freezer(cls):
        app = cls()

        # -- Standard
        app.type = 5  # Kitchen freezer
        app.reference_quantity = 1  # PH-Case Occupants
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 1  # Day
        app.energy_demand = 1.08  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        return app

    @classmethod
    def PHIUS_Combo_Fridge(cls):
        app = cls()

        # -- Standard
        app.type = 6  # Kitchen fridge/freeze combo
        app.reference_quantity = 1  # PH-Case Occupants
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 1  # Day
        app.energy_demand = 0.99  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        return app

    @classmethod
    def PHIUS_Lighting_Int(cls, **kwargs):
        app = cls()

        # -- Standard
        app.type = 14  # PHIUS+ Interior lighting
        app.reference_quantity = 6  # PH case floor area
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 99  # Use
        app.energy_demand = None  # kwh
        app.energy_demand_per_use = None  # kwh/use
        app.combined_energy_facor = None  # CEF

        app.lighting_frac_high_efficiency = 1  # CEF

        for k, v in kwargs.items():
            setattr(app, k, v)

        return app

    @classmethod
    def PHIUS_Lighting_Ext(cls, **kwargs):
        app = cls()

        # -- Standard
        app.type = 15  # PHIUS+ Exterior lighting
        app.reference_quantity = 6  # PH case floor area
        app.quantity = 1
        app.in_conditioned_space = False
        app.reference_energy_norm = 99  # Use
        app.energy_demand = None  # kwh
        app.energy_demand_per_use = None  # kwh/use
        app.combined_energy_facor = None  # CEF

        app.lighting_frac_high_efficiency = 1  # CEF

        for k, v in kwargs.items():
            setattr(app, k, v)

        return app

    @classmethod
    def PHIUS_MEL(cls, **kwargs):
        app = cls()

        # -- Standard
        app.type = 13  # PHIUS+ MEL
        app.reference_quantity = 3  # Bedrooms
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 99  # Use
        app.energy_demand = None  # kwh
        app.energy_demand_per_use = None  # kwh/use
        app.combined_energy_facor = None  # CEF

        for k, v in kwargs.items():
            setattr(app, k, v)

        return app
