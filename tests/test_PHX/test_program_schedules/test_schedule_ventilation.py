import PHX.schedules


def test_util_pat(reset_schedules):
    pattern_1 = PHX.schedules.Schedule_Ventilation()
    pattern_2 = PHX.schedules.Schedule_Ventilation()

    assert pattern_1.id == 1
    assert pattern_2.id == 2


def test_default_util_pat(reset_schedules):
    pattern_1 = PHX.schedules.Schedule_Ventilation.default()
    pattern_2 = PHX.schedules.Schedule_Ventilation.default()

    assert pattern_1.id == 1
    assert pattern_2.id == 1


def test_util_pat_validation_passes(reset_schedules):
    pattern_1 = PHX.schedules.Schedule_Ventilation()
    pattern_1.utilization_rates.maximum.daily_op_sched = 5
    pattern_1.utilization_rates.standard.daily_op_sched = 5
    pattern_1.utilization_rates.basic.daily_op_sched = 9
    pattern_1.utilization_rates.minimum.daily_op_sched = 5

    # if all is well, returns nothing
    assert not pattern_1.validate_total_hours()


def test_util_pat_validation_fails(reset_schedules):
    pattern_1 = PHX.schedules.Schedule_Ventilation()
    pattern_1.utilization_rates.maximum.daily_op_sched = 5
    pattern_1.utilization_rates.standard.daily_op_sched = 5
    pattern_1.utilization_rates.basic.daily_op_sched = 8.99  # <--
    pattern_1.utilization_rates.minimum.daily_op_sched = 5

    # if total != 24, returns a string with the warning message
    assert pattern_1.validate_total_hours()
