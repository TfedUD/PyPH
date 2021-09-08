import PHX.geometry
import PHX.component
import PHX.bldg_segment
import PHX.infiltration


def test_n50_with_no_zones():
    host_segment = PHX.bldg_segment.BldgSegment()
    i = PHX.infiltration.Infiltration(host_segment)
    i.annual_avg_airflow = 500

    assert i.n50 == 0


def test_n50_with_one_zone():
    host_segment = PHX.bldg_segment.BldgSegment()

    z1 = PHX.bldg_segment.Zone()
    z1.volume_net = 100
    host_segment.add_zones(z1)

    i = PHX.infiltration.Infiltration(host_segment)
    i.annual_avg_airflow = 500

    assert i.n50 == 5


def test_n50_with_multiple_zones():
    host_segment = PHX.bldg_segment.BldgSegment()

    z1 = PHX.bldg_segment.Zone()
    z1.volume_net = 100

    z2 = PHX.bldg_segment.Zone()
    z2.volume_net = 50

    z3 = PHX.bldg_segment.Zone()
    z3.volume_net = 25

    host_segment.add_zones([z1, z2, z3])

    i = PHX.infiltration.Infiltration(host_segment)
    i.annual_avg_airflow = 500

    assert i.n50 == 500 / (100 + 50 + 25)
