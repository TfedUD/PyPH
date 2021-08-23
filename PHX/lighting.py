import PHX._base
import PHX.utilization_patterns


class SpaceLighting(PHX._base._Base):

    _default = None

    def __init__(self):
        super(SpaceLighting, self).__init__()
        self.name = ""
        self.utilization = PHX.utilization_patterns.UtilPat_Lighting()
        self.space_illumination = 0  # Lux
        self.installed_power_density = 0.0  # installed power density (W/m2)

    @classmethod
    def default(cls):
        if cls._default is not None:
            return cls._default

        new_obj = cls()

        new_obj.name = "_default_lighting_"
        new_obj.utilization = PHX.utilization_patterns.UtilPat_Lighting.default()
        new_obj.space_illumination = 300
        new_obj.installed_power_density = 1.0

        cls._default = new_obj

        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._SpaceLighting(cls, _dict)
