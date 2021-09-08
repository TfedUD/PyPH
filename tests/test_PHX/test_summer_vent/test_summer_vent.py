import PHX.summer_ventilation


def test_add_summer_vent():
    sv1 = PHX.summer_ventilation.SummerVent()
    sv1.avg_mech_ach = 25
    sv1.day_window_ach = 35
    sv1.night_window_ach = 18
    sv1.additional_mech_ach = 13
    sv1.additional_mech_spec_power = 115
    sv1.exhaust_ach = 12
    sv1.exhaust_spec_power = 56
    sv1.additional_mech_control_mode = 1
    sv1.avg_mech_control_mode = 1

    sv2 = PHX.summer_ventilation.SummerVent()
    sv2.avg_mech_ach = 50
    sv2.day_window_ach = 40
    sv2.night_window_ach = 22
    sv2.additional_mech_ach = 94
    sv2.additional_mech_spec_power = 86
    sv2.exhaust_ach = 76
    sv2.exhaust_spec_power = 4
    sv2.additional_mech_control_mode = 1
    sv2.avg_mech_control_mode = 1

    vol_1 = 2_000
    vol_2 = 3_000

    sv3 = PHX.summer_ventilation.SummerVent.weighted_join(sv1, vol_1, sv2, vol_2)
    assert sv3.avg_mech_ach == 40
    assert sv3.day_window_ach == 38
    assert sv3.night_window_ach == 20.40
    assert sv3.additional_mech_ach == 61.6
    assert sv3.additional_mech_spec_power == 97.6
    assert sv3.exhaust_ach == 50.4
    assert sv3.exhaust_spec_power == 24.80
    assert sv3.additional_mech_control_mode == 1
    assert sv3.avg_mech_control_mode == 1
