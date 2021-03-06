# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PHX Summer Ventilation Class"""

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

    @staticmethod
    def _clean_volume_weighted_join(_a, _vol_a, _b, _vol_b, _attr_str):
        # type: (SummerVent, float, SummerVent, float, str) -> float
        """
        Util function to cleanly join together two SummerVent attributes,
        weighted by volume. Handles ZeroDivisionErrors and None values

        Arguments:
        ----------
            * _a (SummerVent): The first Room's SummerVent object.
            * _vol_a (float): The volume of the first Room.
            * _b (SummerVent): The first SummerVent object.
            * _vol_b (float): The volume of the second Room.
            * _attr_str (str): The name of the attribute to try and join.

        Returns:
        --------
            * (float | None): The weighed joined value for the new joined Room.
        """

        # -- Get the attribute values from the 2 SummVent objects
        val_a = getattr(_a, _attr_str, None)
        val_b = getattr(_b, _attr_str, None)

        if (val_a is None) and (val_b is None):
            return None
        elif (val_a is None) and (val_b is not None):
            return val_a
        elif (val_a is not None) and (val_b is None):
            return val_b
        else:
            try:
                return ((val_a * _vol_a) + (val_b * _vol_b)) / (_vol_a + _vol_b)
            except ZeroDivisionError:
                return 0

    @classmethod
    def weighted_join(cls, obj_1, vol_1, obj_2, vol_2):
        # type: (SummerVent, float, SummerVent, float) -> SummerVent
        """Joins two SummerVent objects weighted by host PHX-Zone volume"""
        new_obj = cls()

        join = SummerVent._clean_volume_weighted_join
        new_obj.avg_mech_ach = join(obj_1, vol_1, obj_2, vol_2, "avg_mech_ach")
        new_obj.day_window_ach = join(obj_1, vol_1, obj_2, vol_2, "day_window_ach")
        new_obj.night_window_ach = join(obj_1, vol_1, obj_2, vol_2, "night_window_ach")
        new_obj.additional_mech_ach = join(obj_1, vol_1, obj_2, vol_2, "additional_mech_ach")
        new_obj.additional_mech_spec_power = join(obj_1, vol_1, obj_2, vol_2, "additional_mech_spec_power")
        new_obj.exhaust_ach = join(obj_1, vol_1, obj_2, vol_2, "exhaust_ach")
        new_obj.exhaust_spec_power = join(obj_1, vol_1, obj_2, vol_2, "exhaust_spec_power")

        return new_obj
