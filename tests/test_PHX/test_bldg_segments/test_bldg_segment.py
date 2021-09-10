import PHX.bldg_segment
import PHX.component
import PHX.geometry
import pytest


def test_segment_identifier(reset_bldg_segment_count):
    v1 = PHX.bldg_segment.BldgSegment()
    v2 = PHX.bldg_segment.BldgSegment()

    assert v1.identifier != v2.identifier


def test_segment_id(reset_bldg_segment_count):
    assert PHX.bldg_segment.BldgSegment._count == 0

    v1 = PHX.bldg_segment.BldgSegment()
    assert PHX.bldg_segment.BldgSegment._count == 1

    v2 = PHX.bldg_segment.BldgSegment()
    assert PHX.bldg_segment.BldgSegment._count == 2


def test_segment_default(reset_bldg_segment_count):
    s = PHX.bldg_segment.BldgSegment.default()

    assert s
    assert isinstance(s, PHX.bldg_segment.BldgSegment)
    assert PHX.bldg_segment.BldgSegment._default == s

    # -- Try again, now that Default has been called once
    s2 = PHX.bldg_segment.BldgSegment.default()
    assert s == s2


def test_add_Zones_basic(reset_bldg_segment_count):
    var1 = PHX.bldg_segment.BldgSegment()
    z1 = PHX.bldg_segment.Zone()
    z2 = PHX.bldg_segment.Zone()
    z3 = PHX.bldg_segment.Zone()

    var1.add_zones(z1)
    assert z1 in var1.zones
    assert len(var1.zones) == 1

    var1.add_zones([z2, z3])
    assert z1 in var1.zones
    assert z2 in var1.zones
    assert z3 in var1.zones
    assert len(var1.zones) == 3


def test_add_Zones_twice(reset_bldg_segment_count):
    var1 = PHX.bldg_segment.BldgSegment()
    z1 = PHX.bldg_segment.Zone()

    var1.add_zones(z1)
    assert z1 in var1.zones
    assert len(var1.zones) == 1

    # Add the same zone again, should ignore it
    var1.add_zones(z1)
    assert z1 in var1.zones
    assert len(var1.zones) == 1


def test_add_not_a_Zone_error(reset_bldg_segment_count):
    var1 = PHX.bldg_segment.BldgSegment()
    z1 = "Not a Zone"

    with pytest.raises(PHX.bldg_segment.ZoneTypeError):
        var1.add_zones(z1)


def test_add_components(reset_bldg_segment_count):
    var1 = PHX.bldg_segment.BldgSegment()

    c1 = PHX.component.Component()
    p1 = PHX.geometry.Polygon()
    p2 = PHX.geometry.Polygon()
    c1.add_polygons([p1, p2])

    c2 = PHX.component.Component()
    p3 = PHX.geometry.Polygon()
    p4 = PHX.geometry.Polygon()
    c2.add_polygons([p3, p4])

    c3 = PHX.component.Component()
    p5 = PHX.geometry.Polygon()
    p6 = PHX.geometry.Polygon()
    c3.add_polygons([p5, p6])

    # Add a component
    var1.add_components(c1)

    # Check that the Building updated properly
    assert c1 in var1.components
    assert len(var1.components) == 1

    # Check that the Geom updated properly
    assert p1 in var1.geom.polygons
    assert p2 in var1.geom.polygons
    assert p3 not in var1.geom.polygons
    assert p4 not in var1.geom.polygons
    assert p5 not in var1.geom.polygons
    assert p6 not in var1.geom.polygons

    # add more components
    var1.add_components([c2, c3])

    # Check that the Building updated properly
    assert c1 in var1.components
    assert c2 in var1.components
    assert len(var1.components) == 3

    # Check that the Geom updated properly
    assert p1 in var1.geom.polygons
    assert p2 in var1.geom.polygons
    assert p3 in var1.geom.polygons
    assert p4 in var1.geom.polygons
    assert p5 in var1.geom.polygons
    assert p6 in var1.geom.polygons


def test_add_Component_twice(reset_bldg_segment_count):
    var1 = PHX.bldg_segment.BldgSegment()
    c1 = PHX.component.Component()

    var1.add_components(c1)
    assert c1 in var1.components
    assert len(var1.components) == 1

    # Add the same zone again, should ignore it
    var1.add_components(c1)
    assert c1 in var1.components
    assert len(var1.components) == 1


def test_add_not_a_Component(reset_bldg_segment_count):
    var1 = PHX.bldg_segment.BldgSegment()
    c1 = "Not a Component"

    with pytest.raises(PHX.component.ComponentTypeError):
        var1.add_components(c1)


def test_get_zone_by_identifier(reset_bldg_segment_count):
    var1 = PHX.bldg_segment.BldgSegment()
    z1 = PHX.bldg_segment.Zone()
    z2 = PHX.bldg_segment.Zone()
    z3 = PHX.bldg_segment.Zone()
    z4 = PHX.bldg_segment.Zone()
    z5 = PHX.bldg_segment.Zone()

    var1.add_zones([z1, z2, z3, z4])

    # Check an Identigier
    got_zone = var1.get_zone_by_identifier(z1.identifier)
    assert got_zone == z1
    assert z1 in var1.zones
    assert z2 in var1.zones
    assert z3 in var1.zones
    assert z4 in var1.zones

    # Check an Identifier
    got_zone = var1.get_zone_by_identifier(z5.identifier)
    assert not got_zone
    assert z1 in var1.zones
    assert z2 in var1.zones
    assert z3 in var1.zones
    assert z4 in var1.zones

    # Check not an Identifier
    got_zone = var1.get_zone_by_identifier("not an identifier")
    assert not got_zone
    assert z1 in var1.zones
    assert z2 in var1.zones
    assert z3 in var1.zones
    assert z4 in var1.zones


def test_BldgSegment_volume_with_single_zone(reset_bldg_segment_count):
    # -- Build zones, Volume Net
    z1 = PHX.bldg_segment.Zone()
    z1.volume_net = 1000
    z1.volume_gross = 1500

    seg = PHX.bldg_segment.BldgSegment()
    seg.add_zones(z1)

    assert seg.total_volume_net == 1000
    assert seg.total_volume_gross == 1500


def test_BldgSegment_volume_with_multiple_zones(reset_bldg_segment_count):
    # -- Build zones, Volume Net
    z1 = PHX.bldg_segment.Zone()
    z1.volume_net = 1000
    z1.volume_gross = 1500

    # -- Build zones, Volume Net
    z2 = PHX.bldg_segment.Zone()
    z2.volume_net = 2000
    z2.volume_gross = 2500

    # -- Build zones, Volume Net
    z3 = PHX.bldg_segment.Zone()
    z3.volume_net = None
    z3.volume_gross = None

    # -- Build zones, Volume Net
    z4 = PHX.bldg_segment.Zone()
    z4.volume_net = 0
    z4.volume_gross = 0

    seg = PHX.bldg_segment.BldgSegment()
    seg.add_zones([z1, z2, z3, z4])

    assert seg.total_volume_net == 3000
    assert seg.total_volume_gross == 4000


def test_BldgSegment_total_exposed_area_with_single_zone(reset_bldg_segment_count):

    assert True


def test_BldgSegment_get_component_groups(reset_bldg_segment_count):
    # -- Build Zone with Components
    z1 = PHX.bldg_segment.Zone()
    c1 = PHX.component.Component()
    c2 = PHX.component.Component()
    c1.set_host_zone_name(z1)
    c2.set_host_zone_name(z1)

    # -- Build Zone with Components
    z2 = PHX.bldg_segment.Zone()
    c3 = PHX.component.Component()
    c4 = PHX.component.Component()
    c3.set_host_zone_name(z2)
    c4.set_host_zone_name(z2)

    # -- Add the Zones and the Components to the Segement
    seg = PHX.bldg_segment.BldgSegment()
    seg.add_zones([z1, z2])
    seg.add_components([c1, c2, c3, c4])

    # Group by Segment ID (single group)
    group_dict = seg.get_component_groups()
    assert len(group_dict) == 1

    # Group by Zone ID (one group for each Zone)
    group_dict = seg.get_component_groups(group_by="Zone")
    assert len(group_dict) == 2

    # Error
    with pytest.raises(PHX.bldg_segment.GroupTypeNotImplementedError):
        group_dict = seg.get_component_groups(group_by="Other")


def test_get_zone_by_id():
    z1 = PHX.bldg_segment.Zone()
    seg = PHX.bldg_segment.BldgSegment()
    seg.add_zones(z1)

    z2 = seg.get_zone_by_identifier(z1.identifier)
    assert z1 == z2

    z3 = seg.get_zone_by_identifier("not a valid id")
    assert not z3


def test_merge_components_normal():
    # -- Build Zones with Components
    c1 = PHX.component.Component()
    c1.assembly_id_num = 1
    c2 = PHX.component.Component()
    c2.assembly_id_num = 1
    c3 = PHX.component.Component()
    c3.assembly_id_num = 2
    c4 = PHX.component.Component()
    c4.assembly_id_num = 2
    c5 = PHX.component.Component()
    c5.assembly_id_num = 3
    c6 = PHX.component.Component()
    c6.assembly_id_num = 3
    c7 = PHX.component.Component()
    c7.assembly_id_num = -1
    c8 = PHX.component.Component()
    c8.assembly_id_num = -1
    w1 = PHX.component.Component()
    w1.win_type_id_num = 12
    w2 = PHX.component.Component()
    w2.win_type_id_num = 12

    z1 = PHX.bldg_segment.Zone()
    c1.set_host_zone_name(z1)
    c2.set_host_zone_name(z1)
    w1.set_host_zone_name(z1)
    w2.set_host_zone_name(z1)

    z2 = PHX.bldg_segment.Zone()
    c3.set_host_zone_name(z2)
    c4.set_host_zone_name(z2)
    c5.set_host_zone_name(z2)
    c6.set_host_zone_name(z2)
    c7.set_host_zone_name(z2)
    c8.set_host_zone_name(z2)

    # -- Add the Zones and the Components to the Segement
    seg_1 = PHX.bldg_segment.BldgSegment()
    seg_1.add_zones([z1, z2])
    seg_1.add_components([w1, w2, c1, c2, c3, c4, c5, c6, c7, c8])

    assert len(seg_1.components) == 10

    # -- Test with no arguments
    seg_1.merge_components()
    assert len(seg_1.components) == 5

    # -- Add the Zones and the Components to the Segement
    seg_2 = PHX.bldg_segment.BldgSegment()
    seg_2.add_zones([z1, z2])
    seg_2.add_components([w1, w2, c1, c2, c3, c4, c5, c6, c7, c8])

    assert len(seg_2.components) == 10

    # -- Test with no arg
    seg_2.merge_components(by="Assembly")
    assert len(seg_2.components) == 5


def test_merge_components_error():
    # -- Add the Zones and the Components to the Segement
    seg = PHX.bldg_segment.BldgSegment()

    # -- Test with no arguments
    with pytest.raises(PHX.bldg_segment.GroupTypeNotImplementedError):
        seg.merge_components(by="not allowed type")


def test_merge_zones_when_empty():
    # -- Add the Zones and the Components to the Segement
    seg_1 = PHX.bldg_segment.BldgSegment()

    assert len(seg_1.zones) == 0
    assert len(seg_1.components) == 0

    # --
    seg_1.merge_zones()

    assert len(seg_1.zones) == 0
    assert len(seg_1.components) == 0


def test_merge_zones_with_zones():
    # -- Build Zones with Components
    c1 = PHX.component.Component()
    c2 = PHX.component.Component()
    c3 = PHX.component.Component()
    c4 = PHX.component.Component()
    w1 = PHX.component.Component()
    w2 = PHX.component.Component()

    z1 = PHX.bldg_segment.Zone()
    c1.set_host_zone_name(z1)
    c2.set_host_zone_name(z1)
    w1.set_host_zone_name(z1)

    z2 = PHX.bldg_segment.Zone()
    c3.set_host_zone_name(z2)
    c4.set_host_zone_name(z2)
    w2.set_host_zone_name(z2)

    # -- Add the Zones and the Components to the Segement
    seg_1 = PHX.bldg_segment.BldgSegment()
    seg_1.add_zones([z1, z2])
    seg_1.add_components([w1, w2, c1, c2, c3, c4])

    assert len(seg_1.zones) == 2
    assert len(seg_1.components) == 6

    # --
    seg_1.merge_zones()

    assert len(seg_1.zones) == 1
    assert len(seg_1.components) == 6
    for c in seg_1.components:
        assert c.int_exposure_zone_id == seg_1.zones[0].id

    # -- Check the zone ID
    got_zone_1 = seg_1.get_zone_by_identifier(z1.identifier)
    assert got_zone_1
