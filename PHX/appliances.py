import PHX._base
import PHX.serialization.from_dict


class UnknownApplianceError(Exception):
    def __init__(self, _in):
        self.message = (
            'Error: Unknown Appliance "{}" with type: "{}". Please check'
            "inputs and enter a valid Appliance type.".format(_in, _in.type)
        )
        super(UnknownApplianceError, self).__init__(self.message)


class ApplianceAdditionError(Exception):
    def __init__(self, _a, _b):
        self.message = 'Error: Cannot add Appliance "{}" with type: "{}" to Appliance {}' 'with type: "{}"'.format(
            _a, _a.type, _b, _b.type
        )
        super(ApplianceAdditionError, self).__init__(self.message)


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

        # -- Handle None cases
        if self and not other:
            return self
        elif other and not self:
            return other
        elif not self and not other:
            return None

        # -- Merge together Appliances
        new_set = self.__class__()
        for app_type_num, app_type_name in self.known_types.items():
            self_appliance = getattr(self, app_type_name)
            other_appliance = getattr(other, app_type_name)

            # -- Handle None cases
            if self_appliance and other_appliance:
                new_appliance = self_appliance + other_appliance
            elif self_appliance and not other_appliance:
                new_appliance = self_appliance
            elif other_appliance and not self_appliance:
                new_appliance = other_appliance
            elif not self_appliance and not other_appliance:
                new_appliance = None

            new_set.add_appliance(new_appliance)

        return new_set


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
        self.user_defined_total = 0

    def __eq__(self, other):
        # type: (Appliance, Appliance) -> Appliance
        fields = (
            "type",
            "comment",
            "reference_quantity",
            "quantity",
            "in_conditioned_space",
            "reference_energy_norm",
            "energy_demand",
            "energy_demand_per_use",
            "combined_energy_facor",
            "dishwasher_capacity_type",
            "dishwasher_capacity",
            "dishwasher_water_connection",
            "washer_capacity",
            "washer_modified_energy_factor",
            "washer_connection",
            "washer_utilization_factor",
            "dryer_type",
            "dryer_gas_consumption",
            "dryer_gas_efficiency_factor",
            "dryer_field_utilization_factor_type",
            "dryer_field_utilization_factor",
            "cooktop_type",
            "lighting_frac_high_efficiency",
            "user_defined_total",
        )

        for field in fields:
            attr_a = getattr(self, field)
            attr_b = getattr(other, field)
            if attr_a != attr_b:
                # print("{}:{} does not equal {}:{}".format(field, attr_a, field, attr_b))
                return False

        return True

    def __add__(self, other):
        # type: (Appliance, Appliance) -> Appliance
        def _set_quantity_weighted_average(_new_obj, _obj_a, _obj_b, _attr):
            # type: (Appliance, Appliance, Appliance, str) -> None
            """Utility function, sets appliance energy demand on a unit-weighted average basis"""

            a = getattr(_obj_a, _attr) * _obj_a.quantity
            b = getattr(_obj_b, _attr) * _obj_b.quantity
            weighted_avg = (a + b) / (_obj_a.quantity + _obj_b.quantity)
            setattr(_new_obj, _attr, weighted_avg)

            return None

        def _set_average_energy(_new_obj, _obj_a, _obj_b):
            # type: (Appliance, Appliance, Appliance) -> None
            """Utility function sets the averaged basic energy attributes for all appliances"""

            _set_quantity_weighted_average(_new_obj, _obj_a, _obj_b, "energy_demand")
            _set_quantity_weighted_average(_new_obj, _obj_a, _obj_b, "energy_demand_per_use")
            _set_quantity_weighted_average(_new_obj, _obj_a, _obj_b, "combined_energy_facor")

            return None

        # -- Handle None case
        if self and not other:
            return self

        # -- Join appliances
        # -- Mostly just averaging the values
        if self.type == 1 and other.type == 1:
            new_appliance = self.__class__.PHIUS_Dishwasher()
            new_appliance.quantity = self.quantity + other.quantity
            _set_average_energy(new_appliance, self, other)
            _set_quantity_weighted_average(new_appliance, self, other, "dishwasher_capacity")
        elif self.type == 2 and other.type == 2:
            new_appliance = self.__class__.PHIUS_Clothes_Washer()
            new_appliance.quantity += other.quantity
            _set_average_energy(new_appliance, self, other)
            _set_quantity_weighted_average(new_appliance, self, other, "washer_modified_energy_factor")
        elif self.type == 3 and other.type == 3:
            new_appliance = self.__class__.PHIUS_Clothes_Dryer()
            new_appliance.quantity += other.quantity
            _set_average_energy(new_appliance, self, other)
            _set_quantity_weighted_average(new_appliance, self, other, "dryer_gas_consumption")
            _set_quantity_weighted_average(new_appliance, self, other, "dryer_gas_efficiency_factor")
            _set_quantity_weighted_average(new_appliance, self, other, "dryer_field_utilization_factor")
        elif self.type == 4 and other.type == 4:
            new_appliance = self.__class__.PHIUS_Fridge()
            _set_average_energy(new_appliance, self, other)
        elif self.type == 5 and other.type == 5:
            new_appliance = self.__class__.PHIUS_Freezer()
            _set_average_energy(new_appliance, self, other)
        elif self.type == 6 and other.type == 6:
            new_appliance = self.__class__.PHIUS_Combo_Fridge()
            _set_average_energy(new_appliance, self, other)
        elif self.type == 7 and other.type == 7:
            new_appliance = self.__class__.PHIUS_Cooktop()
            new_appliance.quantity += other.quantity
            _set_average_energy(new_appliance, self, other)
        elif self.type == 13 and other.type == 13:
            new_appliance = self.__class__.PHIUS_MEL()
            if self.reference_quantity == 5 or other.reference_quantity == 5:  # User defined
                new_appliance.reference_quantity = 5
                new_appliance.user_defined_total = self.user_defined_total + other.user_defined_total
                new_appliance.energy_demand = 100
                new_appliance.energy_demand_per_use = 100
        elif self.type == 14 and other.type == 14:
            new_appliance = self.__class__.PHIUS_Lighting_Int()
            if self.reference_quantity == 5 or other.reference_quantity == 5:  # User defined
                new_appliance.reference_quantity = 5
                new_appliance.user_defined_total = self.user_defined_total + other.user_defined_total
                new_appliance.energy_demand = 100
                new_appliance.energy_demand_per_use = 100
        elif self.type == 15 and other.type == 15:
            new_appliance = self.__class__.PHIUS_Lighting_Ext()
            if self.reference_quantity == 5 or other.reference_quantity == 5:  # User defined
                new_appliance.reference_quantity = 5
                new_appliance.user_defined_total = self.user_defined_total + other.user_defined_total
                new_appliance.energy_demand = 100
                new_appliance.energy_demand_per_use = 100
        else:
            raise ApplianceAdditionError(self, other)

        return new_appliance

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
        app.type = 2  # clothes washer
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
        app.energy_demand = 0  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

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
        app.energy_demand = 0  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

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
        app.energy_demand = 0  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        for k, v in kwargs.items():
            setattr(app, k, v)

        return app
