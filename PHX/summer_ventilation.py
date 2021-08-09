import PHX._base
import PHX.serialization.from_dict


class SummerVent(PHX._base._Base):
    def __init__(self):
        super(SummerVent, self).__init__()
        self.avg_mech_ach = 0.0  # Should normaly be same as winter ACH
        self.day_window_ach = 0.0
        self.night_window_ach = 0.0
        self.additional_mech_ach = 0.0
        self.additional_mech_spec_power = 0.0
        self.exhaust_ach = 0.0
        self.exhaust_spec_power = 0.0

        self.additional_mech_control_mode = 1
        self.avg_mech_control_mode = 1

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._SummerVent(cls, _dict)
