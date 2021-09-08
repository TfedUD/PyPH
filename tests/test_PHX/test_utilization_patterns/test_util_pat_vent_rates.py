import PHX.utilization_patterns
import pytest


def test_set_rates_valid_inputs():
    rates = PHX.utilization_patterns.Vent_UtilRates()

    rates.maximum.daily_op_sched = 1
    rates.maximum.daily_op_sched = None
    rates.maximum.frac_of_design_airflow = 0.5
    rates.maximum.frac_of_design_airflow = None
    assert rates.maximum.daily_op_sched == 1
    assert rates.maximum.frac_of_design_airflow == 0.5

    rates.standard.daily_op_sched = 1
    rates.standard.daily_op_sched = None
    rates.standard.frac_of_design_airflow = 0.5
    rates.standard.frac_of_design_airflow = None
    assert rates.standard.daily_op_sched == 1
    assert rates.standard.frac_of_design_airflow == 0.5

    rates.basic.daily_op_sched = 1
    rates.basic.daily_op_sched = None
    rates.basic.frac_of_design_airflow = 0.5
    rates.basic.frac_of_design_airflow = None
    assert rates.basic.daily_op_sched == 1
    assert rates.basic.frac_of_design_airflow == 0.5

    rates.minimum.daily_op_sched = 1
    rates.minimum.daily_op_sched = None
    rates.minimum.frac_of_design_airflow = 0.5
    rates.minimum.frac_of_design_airflow = None
    assert rates.minimum.daily_op_sched == 1
    assert rates.minimum.frac_of_design_airflow == 0.5

    rates.maximum.frac_of_design_airflow = 20
    assert rates.maximum.frac_of_design_airflow == 0.2
    rates.standard.frac_of_design_airflow = 30
    assert rates.standard.frac_of_design_airflow == 0.3
    rates.basic.frac_of_design_airflow = 100
    assert rates.basic.frac_of_design_airflow == 1.0
    rates.minimum.frac_of_design_airflow = 15
    assert rates.minimum.frac_of_design_airflow == 0.15

    assert rates


def test_set_rates_invalid_inputs():
    rates = PHX.utilization_patterns.Vent_UtilRates()

    with pytest.raises(ValueError):
        rates.maximum.daily_op_sched = 100
        rates.standard.daily_op_sched = 100
        rates.basic.daily_op_sched = 100
        rates.minimum.daily_op_sched = 100

    with pytest.raises(ValueError):
        rates.maximum.daily_op_sched = "not a number"
        rates.standard.daily_op_sched = "not a number"
        rates.basic.daily_op_sched = "not a number"
        rates.minimum.daily_op_sched = "not a number"

    with pytest.raises(ValueError):
        rates.maximum.frac_of_design_airflow = "not a number"
        rates.standard.frac_of_design_airflow = "not a number"
        rates.basic.frac_of_design_airflow = "not a number"
        rates.minimum.frac_of_design_airflow = "not a number"

    assert rates
