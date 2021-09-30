import PHX._base


class Distribution(PHX._base._Base):
    def __init__(self):
        super(Distribution, self).__init__()
        self.use_default_values = True
        self.device_in_conditioned_space = True


# ------------------------------------------------------------------------------
# -- HVAC
class HVAC_Duct_Segment(PHX._base._Base):
    """A single duct length/segment"""

    _default = None

    def __init__(self):
        super(HVAC_Duct_Segment, self).__init__()
        self.length = 0.0
        self.diameter = 0.0
        self.width = 0.0
        self.height = 0.0
        self.insulation_thickness = 0.0
        self.insulation_conductivity = 0.0

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Duct_Segment(cls, _dict)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns the default HVAC_Duct-Segment"""

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


class HVAC_Duct(PHX._base._Base):
    """A HVAC_Duct, made of 1 or more HVAC_Duct-segments"""

    _default = None

    def __init__(self):
        super(HVAC_Duct, self).__init__()
        self.segments = []

    @property
    def length(self):
        return sum(seg.length for seg in self.segments)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Duct(cls, _dict)

    @classmethod
    def default(cls, *args, **kwargs):
        """Returns the default HVAC_Duct"""

        if cls._default:
            return cls._default

        new_obj = cls()

        new_obj.segments = [HVAC_Duct_Segment.default()]

        cls._default = new_obj
        return new_obj

    def __add__(self, other):
        # type: (HVAC_Duct, HVAC_Duct) -> HVAC_Duct
        new_obj = self.__class__()
        new_obj.segments.extend(self.segments)
        new_obj.segments.extend(other.segments)
        return new_obj

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)


class HVAC_Distribution_Ventilation(PHX._base._Base):
    def __init__(self):
        super(HVAC_Distribution_Ventilation, self).__init__()
        self.fresh_air_duct = HVAC_Duct()
        self.exhaust_air_duct = HVAC_Duct()

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._HVAC_Distribution_Ventilation(cls, _dict)


# ------------------------------------------------------------------------------
# -- DHW
