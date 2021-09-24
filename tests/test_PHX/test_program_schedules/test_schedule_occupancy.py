import PHX.schedules
import pytest


def test_schedule(reset_schedules):
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    pattern_2 = PHX.schedules.Schedule_Occupancy()

    assert pattern_1.id == 1
    assert pattern_2.id == 2

    assert pattern_1.unique_key == pattern_2.unique_key


def test_default_schedule(reset_schedules):
    pattern_1 = PHX.schedules.Schedule_Occupancy.default()
    pattern_2 = PHX.schedules.Schedule_Occupancy.default()

    assert pattern_1.id == 1
    assert pattern_2.id == 1

    assert pattern_1.unique_key == pattern_2.unique_key


def test_schedule_different_values(reset_schedules):
    # Different Start Hour
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    pattern_1.start_hour = 1
    pattern_2 = PHX.schedules.Schedule_Occupancy()
    pattern_2.start_hour = 2

    assert pattern_1.unique_key != pattern_2.unique_key

    # Different End Hour
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    pattern_1.end_hour = 1
    pattern_2 = PHX.schedules.Schedule_Occupancy()
    pattern_2.end_hour = 2

    assert pattern_1.unique_key != pattern_2.unique_key

    # Different annual_utilization_days
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    pattern_1.annual_utilization_days = 1
    pattern_2 = PHX.schedules.Schedule_Occupancy()
    pattern_2.annual_utilization_days = 2

    assert pattern_1.unique_key != pattern_2.unique_key

    # Different annual_utilization_factor
    pattern_1 = PHX.schedules.Schedule_Occupancy()
    pattern_1.annual_utilization_factor = 0.12
    pattern_2 = PHX.schedules.Schedule_Occupancy()
    pattern_2.annual_utilization_factor = 0.13

    assert pattern_1.unique_key != pattern_2.unique_key


def test_calc_annual_utilization_fac_when_changing_rel_frac(reset_schedules):
    # -- Try rel_fac = 1
    sched = PHX.schedules.Schedule_Occupancy.default()
    sched.start_hour = 0
    sched.end_hour = 24
    sched.annual_utilization_days = 365
    sched.relative_utilization_factor = 1  # <-----

    assert sched.annual_utilization_factor == 1

    # -- Try rel_fac = 0.5
    sched.start_hour = 0
    sched.end_hour = 24
    sched.annual_utilization_days = 365
    sched.relative_utilization_factor = 0.5  # <-----

    assert sched.annual_utilization_factor == pytest.approx(0.5)

    # -- Try rel_fac = 0.0
    sched.start_hour = 0
    sched.end_hour = 24
    sched.annual_utilization_days = 365
    sched.relative_utilization_factor = 0  # <-----

    assert sched.annual_utilization_factor == pytest.approx(0)


def test_calc_annual_utilization_fac_when_changing_operating_period(reset_schedules):
    # -- Try with different hour
    sched = PHX.schedules.Schedule_Occupancy.default()
    sched.start_hour = 0
    sched.end_hour = 12  # <-----
    sched.annual_utilization_days = 365
    sched.relative_utilization_factor = 1

    assert sched.annual_utilization_factor == pytest.approx(0.5)

    # --
    sched.start_hour = 0
    sched.end_hour = 6  # <-----
    sched.annual_utilization_days = 365
    sched.relative_utilization_factor = 1

    assert sched.annual_utilization_factor == pytest.approx(0.25)

    # --
    sched.start_hour = 0
    sched.end_hour = 0  # <-----
    sched.annual_utilization_days = 365
    sched.relative_utilization_factor = 1

    assert sched.annual_utilization_factor == pytest.approx(0)

    # -- Different Days
    sched.start_hour = 0
    sched.end_hour = 24
    sched.annual_utilization_days = 182.5  # <-----
    sched.relative_utilization_factor = 1

    assert sched.annual_utilization_factor == pytest.approx(0.5)

    # --
    sched.start_hour = 0
    sched.end_hour = 24
    sched.annual_utilization_days = 91.25  # <-----
    sched.relative_utilization_factor = 1

    assert sched.annual_utilization_factor == pytest.approx(0.25)

    # -- Both different
    sched.start_hour = 0
    sched.end_hour = 24
    sched.annual_utilization_days = 182.5  # <----- (1/2)
    sched.relative_utilization_factor = 0.5  # <----- (1/2)

    assert sched.annual_utilization_factor == pytest.approx(0.25)  # = 0.5 * 0.5

    # --
    sched.start_hour = 0
    sched.end_hour = 12  # <----- (1/2)
    sched.annual_utilization_days = 91.25  # <----- (1/4)
    sched.relative_utilization_factor = 0.25  # <----- (1/4)

    assert sched.annual_utilization_factor == pytest.approx(0.03125)  # = 0.5 * 0.25 * 0.25


def test_setting_annual_utilization_fact(reset_schedules):
    sched = PHX.schedules.Schedule_Occupancy()
    sched.start_hour = 6
    sched.end_hour = 18
    sched.annual_utilization_days = 182.5
    sched.relative_utilization_factor = 1

    assert sched.annual_utilization_factor == 0.25

    # -- Reset everything
    sched.annual_utilization_factor = 0.5

    assert sched.start_hour == 0
    assert sched.end_hour == 24
    assert sched.annual_utilization_days == 365
    assert sched.relative_utilization_factor == 0.5
