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

    @classmethod
    def weighted_join(cls, obj_1, vol_1, obj_2, vol_2):
        """Joins two SummerVent objects weighted by host PHX-Zone volume"""

        total_vol = vol_1 + vol_2

        new_obj = cls()

        new_obj.avg_mech_ach = (
            (obj_1.avg_mech_ach * vol_1) + (obj_2.avg_mech_ach * vol_2)
        ) / total_vol

        new_obj.day_window_ach = (
            (obj_1.day_window_ach * vol_1) + (obj_2.day_window_ach * vol_2)
        ) / total_vol

        new_obj.night_window_ach = (
            (obj_1.night_window_ach * vol_1) + (obj_2.night_window_ach * vol_2)
        ) / total_vol

        new_obj.additional_mech_ach = (
            (obj_1.additional_mech_ach * vol_1) + (obj_2.additional_mech_ach * vol_2)
        ) / total_vol

        new_obj.additional_mech_spec_power = (
            (obj_1.additional_mech_spec_power * vol_1)
            + (obj_2.additional_mech_spec_power * vol_2)
        ) / total_vol

        new_obj.exhaust_ach = (
            (obj_1.exhaust_ach * vol_1) + (obj_2.exhaust_ach * vol_2)
        ) / total_vol

        new_obj.exhaust_spec_power = (
            (obj_1.exhaust_spec_power * vol_1) + (obj_2.exhaust_spec_power * vol_2)
        ) / total_vol

        return new_obj
