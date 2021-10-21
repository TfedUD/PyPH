import PHX._base
import PHX.programs.schedules
import PHX.serialization.from_dict
from collections import defaultdict


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


class ApplianceTypeMismatchError(Exception):
    def __init__(self, _a, _b, _attr_name):
        self.message = (
            'Error: Cannot add Appliance "{}" with attribute: "{}:{}" to Appliance {}'
            'with attribute: "{}:{}"'.format(
                _a, _attr_name, getattr(_a, _attr_name), _b, _attr_name, getattr(_b, _attr_name)
            )
        )
        super(ApplianceTypeMismatchError, self).__init__(self.message)


class Appliance(PHX._base._Base):
    """An individual PHX-Appliance such as a cooktop or dishwasher."""

    def __init__(self):
        super(Appliance, self).__init__()
        self.name = ""
        self.type = 1
        self.comment = None
        self.reference_quantity = 2  # Zone Occupants
        self.quantity = 0
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
        self._user_defined_total = 0

        # -- PHIUS Non-Res Cooking
        self.num_meals_per_day = 0
        self.usage = None  # For Non-Res Kitchen Schedules

    @property
    def user_defined_total(self):
        return self._user_defined_total

    @user_defined_total.setter
    def user_defined_total(self, _in):
        if not _in:
            return None
        self._user_defined_total = _in
        self.reference_quantity = 5  # User Defined

    def __eq__(self, other):
        # type: (Appliance, Appliance) -> Appliance
        if type(self) != type(other):
            return False

        fields = (
            "name",
            "type",
            "usage",
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
            "num_meals_per_day",
        )

        for field in fields:
            attr_a = getattr(self, field)
            attr_b = getattr(other, field)
            if attr_a != attr_b:
                return False

        return True

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Appliance(cls, _dict)

    def __add__(self, other):
        # type: (Appliance, Appliance) -> Appliance

        def _set_quantity_weighted_average(_new_obj, _obj_a, _obj_b, _attr_name):
            # type: (Appliance, Appliance, Appliance, str) -> None
            """Utility function used by __add__: Sets appliance energy demand on a unit-weighted average basis"""

            a = getattr(_obj_a, _attr_name, 0) * _obj_a.quantity
            b = getattr(_obj_b, _attr_name, 0) * _obj_b.quantity
            weighted_avg = (float(a) + float(b)) / (_obj_a.quantity + _obj_b.quantity)
            setattr(_new_obj, _attr_name, weighted_avg)

            return None

        def _set_type_value(_new_obj, _obj_a, _obj_b, _attr_name):
            # type (Appliance, Appliance, Appliance, str) -> None
            """Utility function used by __add__: Checks Appliance 'type' values are the same when adding"""

            a = getattr(_obj_a, _attr_name)
            b = getattr(_obj_b, _attr_name)
            if a != b:
                raise ApplianceTypeMismatchError(_obj_a, _obj_b, _attr_name)
            else:
                setattr(_new_obj, _attr_name, a)

        if self and not other:
            return self
        elif self.type != other.type:
            raise ApplianceAdditionError(self, other)
        elif self.type not in {1, 2, 3, 4, 5, 6, 7, 11, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24}:
            raise ApplianceAdditionError(self, other)

        new_appliance = self.__class__()
        new_appliance.type = self.type
        new_appliance.quantity = self.quantity + other.quantity

        # -- Set the comment
        if self.comment == other.comment:
            new_appliance.comment = self.comment
        else:
            new_appliance.comment = self.comment or "" + other.comment or ""

        # -- General Appliance Values
        _set_type_value(new_appliance, self, other, "reference_energy_norm")
        _set_quantity_weighted_average(new_appliance, self, other, "energy_demand")
        _set_quantity_weighted_average(new_appliance, self, other, "energy_demand_per_use")
        _set_quantity_weighted_average(new_appliance, self, other, "combined_energy_facor")

        # -- Dishwasher
        _set_type_value(new_appliance, self, other, "dishwasher_capacity_type")
        _set_quantity_weighted_average(new_appliance, self, other, "dishwasher_capacity")
        _set_type_value(new_appliance, self, other, "dishwasher_water_connection")

        # -- Laundry Washer
        _set_quantity_weighted_average(new_appliance, self, other, "washer_capacity")
        _set_quantity_weighted_average(new_appliance, self, other, "washer_modified_energy_factor")
        _set_type_value(new_appliance, self, other, "washer_connection")
        _set_quantity_weighted_average(new_appliance, self, other, "washer_utilization_factor")

        # -- Laundry Dryer
        _set_type_value(new_appliance, self, other, "dryer_type")
        _set_quantity_weighted_average(new_appliance, self, other, "dryer_gas_consumption")
        _set_quantity_weighted_average(new_appliance, self, other, "dryer_gas_efficiency_factor")
        _set_type_value(new_appliance, self, other, "dryer_field_utilization_factor_type")
        _set_quantity_weighted_average(new_appliance, self, other, "dryer_field_utilization_factor")

        # -- Cooktop
        _set_type_value(new_appliance, self, other, "cooktop_type")

        # -- PHIUS Lighting and MEL
        _set_quantity_weighted_average(new_appliance, self, other, "lighting_frac_high_efficiency")

        # -- User-Determine Loads (and PHIUS Multifamily)
        if self.type == 11:
            if self.reference_quantity == 5 or other.reference_quantity == 5:  # User defined
                new_appliance.quantity = 1
                new_appliance.reference_quantity = 5
                new_appliance.energy_demand = float(self.energy_demand) + float(other.energy_demand)
                new_appliance.energy_demand_per_use = 0

        # -- PHIUS Non-Res Kitchen
        new_appliance.name = self.name
        # print("here", new_appliance, new_appliance.name, new_appliance.quantity)
        # new_appliance.num_meals_per_day = _set_quantity_weighted_average(
        #     new_appliance, self, other, "num_meals_per_day"
        # )

        return new_appliance

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    # --- PHIUS Residential Standard
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

    # -- PHIUS Resi Loads
    @classmethod
    def PHIUS_MEL(cls, **kwargs):
        app = cls()

        # -- Standard
        app.type = 13  # PHIUS+ MEL
        app.reference_quantity = 3  # Bedroooms
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 2  # Year
        app.energy_demand = 0  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        for k, v in kwargs.items():
            setattr(app, k, v)

        return app

    @classmethod
    def PHIUS_Lighting_Int(cls, **kwargs):
        app = cls()

        # -- Standard
        app.type = 14  # PHIUS+ Interior lighting
        app.reference_quantity = 6  # PH case floor area
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 2  # Year
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
        app.reference_energy_norm = 2  # Year
        app.energy_demand = 0  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        app.lighting_frac_high_efficiency = 1  # CEF

        for k, v in kwargs.items():
            setattr(app, k, v)

        return app

    @classmethod
    def PHIUS_Lighting_Garage(cls, **kwargs):
        app = cls()

        # -- Standard
        app.type = 16  # PHIUS+ Garage lighting
        app.reference_quantity = 6  # PH case floor area
        app.quantity = 1
        app.in_conditioned_space = False
        app.reference_energy_norm = 2  # Year
        app.energy_demand = 0  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        app.lighting_frac_high_efficiency = 1  # CEF

        for k, v in kwargs.items():
            setattr(app, k, v)

        return app

    # --- Residential Custom
    @classmethod
    def Custom_Electric_per_Year(cls, **kwargs):
        app = cls()

        # -- Standard
        app.type = 11  # User defined
        app.reference_quantity = 5  # User Defined
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 2  # Year
        app.energy_demand = 0  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        for k, v in kwargs.items():
            setattr(app, k, v)

        return app

    @classmethod
    def Custom_Electric_per_Use(cls, **kwargs):
        app = cls()

        # -- Standard
        app.type = 18  # User defined - Misc electric loads
        app.reference_quantity = 5  # User Defined
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 99  # Use
        app.energy_demand = 0  # kwh
        app.energy_demand_per_use = 0  # kwh/use
        app.combined_energy_facor = 0  # CEF

        for k, v in kwargs.items():
            setattr(app, k, v)

        return app

    # --- PHIUS NonResidential Kitchen
    @classmethod
    def PHIUS_NonResKitchen_Dishwasher(cls, **kwargs):
        app = cls()

        # -- Standard
        app.name = "_Default_Dishwasher_"
        app.type = 21
        app.reference_quantity = 5  # User Defined
        app.quantity = 1
        app.in_conditioned_space = True
        app.reference_energy_norm = 99  # Use
        app.energy_demand = 0
        app.energy_demand_per_use = 0
        app.combined_energy_facor = 0

        # -- Custom
        app.num_meals_per_day = 1
        app.usage = PHX.programs.schedules.Schedule_NonResAppliance()

        for k, v in kwargs.items():
            setattr(app, k, v)

        return app


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
        16: "PHIUS_Lighting_Garage",
        11: "Custom_Electric_per_Year",
        17: "Custom_Electric_Lighting_per_Year",
        18: "Custom_Electric_MEL_per_Use",
        21: "Commercial_Dishwasher",
        22: "Commercial_Refrigerator",
        23: "Commercial_Cooking",
        24: "Commercial_Custom",
    }

    def __init__(self):
        super(ApplianceSet, self).__init__()
        self.appliance_dict = defaultdict(list)  # {'washer': [w1, w2,...], 'dryer':[...], ...}

    def add_appliances_to_set(self, _appliances):
        # type: (ApplianceSet, list[Appliance]) -> None
        """Adds Appliances to the set if they are of a known type."""

        if not isinstance(_appliances, list):
            _appliances = [_appliances]

        for appliance in _appliances:
            if not appliance:
                continue

            app_type_name = self.known_types.get(appliance.type, None)
            if not app_type_name:
                raise UnknownApplianceError(appliance)

            self.appliance_dict[app_type_name].append(appliance)

    def remove_type_from_set(self, _type_name):
        # type: (str) -> None
        if _type_name not in self.known_types.values():
            raise UnknownApplianceError(_type_name)

        self.appliance_dict.pop(_type_name, None)

    @property
    def appliances(self):
        # type: (ApplianceSet) -> list[Appliance]
        """Return a flat list of all the appliances in the ApplianceSet"""
        appliance_list = []
        for appliance_type_list in self.appliance_dict.values():
            for appliance in appliance_type_list:
                if appliance:
                    appliance_list.append(appliance)

        return appliance_list

    def __iter__(self):
        for _ in self.appliances:
            if not _:
                continue
            yield _

    def __len__(self):
        return len(self.appliances)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._ApplianceSet(cls, _dict)

    def __add__(self, other):
        # type: (ApplianceSet, ApplianceSet) -> ApplianceSet
        if other is None:
            return self

        new_set = self.__class__()

        # -- Merge together Appliance Lists one Type at a time
        for app_type_name in self.known_types.values():
            self_appliances = self.appliance_dict.get(app_type_name, [])
            other_appliances = other.appliance_dict.get(app_type_name, [])

            appliances = []
            appliances.extend(self_appliances)
            appliances.extend(other_appliances)

            if not appliances:
                continue

            # ------------------------------------------------------------------
            # -- Also Breakup/Sort the appliance of this type based on the 'comment'. This
            # -- allows for multiple instances of a single type to be included
            # -- in the ApplianceSet, if the user gives each a different 'comment' attr
            appliances_by_comment_type = defaultdict(list)
            for app in appliances:
                appliances_by_comment_type[app.comment].append(app)

            # ------------------------------------------------------------------
            # -- Merge all the appliances of that Type into a single instance,
            for app_list in appliances_by_comment_type.values():
                merged_appliance = sum(app_list)
                new_set.add_appliances_to_set(merged_appliance)

            # ------------------------------------------------------------------
            # -- Keep track of the count
            #
            #
            #
            # TODO

        return new_set

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __str__(self):
        return "{}: [{} appliances]".format(self.__class__.__name__, len(self.appliances))
