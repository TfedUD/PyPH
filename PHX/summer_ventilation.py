import PHX._base
import PHX.serialization.from_dict


class PHX_SummerVent(PHX._base._Base):
    def __init__(self):
        super(PHX_SummerVent, self).__init__()
        self.day_ach = 0.0
        self.night_ach = 0.0

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._PHX_SummerVent(cls, _dict)
