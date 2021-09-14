import PHX._base
import PHX.schedules
import PHX.loads
import PHX.serialization.from_dict


class SpaceLighting(PHX._base._Base):

    _default = None

    def __init__(self):
        super(SpaceLighting, self).__init__()
        self.name = ""
        self.schedule = PHX.schedules.Schedule_Lighting()
        self.loads = PHX.loads.Load_Lighting()

    @classmethod
    def default(cls):
        if cls._default is not None:
            return cls._default

        new_obj = cls()

        new_obj.name = "_default_space_lighting_"
        new_obj.schedule = PHX.schedules.Schedule_Lighting.default()
        new_obj.loads = PHX.loads.Load_Lighting.default()

        cls._default = new_obj

        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._SpaceLighting(cls, _dict)

    @property
    def unique_key(self):
        return "{}_{}_{}_".format(self.name, self.loads.unique_key, self.schedule.unique_key)
