import PHX
import PHX._base
import PHX.hvac


class Ventilation_Duct_Segment(PHX._base._Base):
    """A single duct length/segment"""

    _default = None

    def __init__(self):
        super(Ventilation_Duct_Segment, self).__init__()
        self.length = 0.0
        self.diameter = 0.0
        self.width = 0.0
        self.height = 0.0
        self.insulation_thickness = 0.0
        self.insulation_conductivity = 0.0

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Ventilation_Duct_Segment(cls, _dict)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns the default Duct-Segment"""

        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.length = 5  # m
        new_obj.diameter = 0.160  # m
        new_obj.width = 0.0
        new_obj.height = 0.0
        new_obj.insulation_thickness = 0.0254  # m
        new_obj.insulation_conductivity = 0.04

        cls._default = new_obj
        return new_obj


class Ventilation_Duct(PHX._base._Base):
    """A duct, made of 1 or more duct-segments"""

    _default = None

    def __init__(self):
        super(Ventilation_Duct, self).__init__()
        self.segments = []

    @property
    def length(self):
        return sum(seg.length for seg in self.segments)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Ventilation_Duct(cls, _dict)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns the default Duct"""

        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.segments = [Ventilation_Duct_Segment.default()]

        cls._default = new_obj
        return new_obj

    def __add__(self, other):
        self.segments.extend(other.segments)
        return self

    def __radd__(self, other):
        return self.__add__(other)


class Ventilator_PH_Parameters(PHX._base._Base):
    def __init__(self):
        super(Ventilator_PH_Parameters, self).__init__()
        self.ElectricEfficiency = 0.45  # W/m3h
        self.FrostProtection = True
        self.Quantity = 1
        self.SubsoilHeatExchangeEfficiency = 0.0
        self.HumidityRecoveryEfficiency = 0.0
        self.HeatRecoveryEfficiency = 0.75
        self.VolumeFlowRateFrom = 0.0
        self.VolumeFlowRateTo = 0.0
        self.TemperatureBelowDefrostUsed = -5  # C
        self.DefrostRequired = True
        self.NoSummerBypass = False
        self.HRVCalculatorData = None
        self.Maximum_VOS = 0
        self.Maximum_PP = 100
        self.Standard_VOS = 0
        self.Standard_PP = 0
        self.Basic_VOS = 0
        self.Basic_PP = 0
        self.Minimum_VOS = 0
        self.Minimum_PP = 0
        self.AuxiliaryEnergy = 0.0
        self.AuxiliaryEnergyDHW = 0.0
        self.InConditionedSpace = True

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Ventilator_PH_Parameters(cls, _dict)


class Ventilator(PHX.hvac.HVAC_Device):

    _default = None

    def __init__(self):
        super(Ventilator, self).__init__()
        self.UsedFor_Ventilation = True
        self.PH_Parameters = Ventilator_PH_Parameters()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(Ventilator, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns a new Device for a default Ventilator (HRV/ERV)"""
        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.Name = "__default_ventilator__"
        new_obj.TypeDevice = 1
        new_obj.SystemType = 1

        cls._default = new_obj
        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Ventilator(cls, _dict)


class Ventilation_System(PHX._base._Base):
    """HVAC System for Fresh-Air Ventilation Devices and Distribution"""

    _count = 0
    _default = None

    def __init__(self):
        self.id = self._count
        super(Ventilation_System, self).__init__()
        self.name = ""
        self.type = 2
        self.ventilator = Ventilator()
        self.duct_01 = Ventilation_Duct()
        self.duct_02 = Ventilation_Duct()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""

        cls._count += 1
        return super(Ventilation_System, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Ventilation_System(cls, _dict)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns the new Ventilation System"""

        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.name = "__default_ventilation_system__"
        new_obj.type = 2
        new_obj.ventilator = Ventilator.default()
        new_obj.duct_01 = Ventilation_Duct.default()
        new_obj.duct_02 = Ventilation_Duct.default()

        cls._default = new_obj
        return new_obj
