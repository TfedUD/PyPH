import PHX
import PHX._base
import PHX.hvac_system


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
        # type: (Ventilation_Duct, Ventilation_Duct) -> Ventilation_Duct
        new_obj = self.__class__()
        new_obj.segments.extend(self.segments)
        new_obj.segments.extend(other.segments)
        return new_obj

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
