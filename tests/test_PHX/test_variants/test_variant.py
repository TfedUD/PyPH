import PHX.variant
import PHX.component
import PHX.geometry

def  test_variant_identifier(reset_variant_count):
    v1 = PHX.variant.Variant()
    v2 = PHX.variant.Variant()

    assert v1.identifier != v2.identifier

def test_variant_id(reset_variant_count):
    assert PHX.variant.Variant._count == 0
    
    v1 = PHX.variant.Variant()
    assert PHX.variant.Variant._count == 1
    
    v2 = PHX.variant.Variant()
    assert PHX.variant.Variant._count == 2

def test_add_zones():
    var1 = PHX.variant.Variant()
    z1 = PHX.variant.Zone()
    z2 = PHX.variant.Zone()
    z3 = PHX.variant.Zone()

    var1.add_zones( z1 )
    assert z1 in var1.zones
    assert len(var1.zones) == 1

    var1.add_zones( [z2, z3] )
    assert z1 in var1.zones
    assert z2 in var1.zones
    assert z3 in var1.zones
    assert len(var1.zones) == 3

def test_add_components():
    var1 = PHX.variant.Variant()

    c1 = PHX.component.Component()
    p1 = PHX.geometry.Polygon()
    p2 = PHX.geometry.Polygon()
    c1.add_polygons( [p1, p2] )

    c2 = PHX.component.Component()
    p3 = PHX.geometry.Polygon()
    p4 = PHX.geometry.Polygon()
    c2.add_polygons( [p3, p4] )

    c3 = PHX.component.Component()
    p5 = PHX.geometry.Polygon()
    p6 = PHX.geometry.Polygon()
    c3.add_polygons( [p5, p6] )

    # Add a component
    var1.add_components( c1 )

    # Check that the Building updated properly
    assert c1 in var1.building.lComponent
    assert len(var1.building.lComponent) == 1

    # Check that the Geom updated properly
    assert p1 in var1.geom.polygons
    assert p2 in var1.geom.polygons
    assert p3 not in var1.geom.polygons
    assert p4 not in var1.geom.polygons
    assert p5 not in var1.geom.polygons
    assert p6 not in var1.geom.polygons

    # add more components
    var1.add_components( [c2, c3] )

    # Check that the Building updated properly
    assert c1 in var1.building.lComponent
    assert c2 in var1.building.lComponent
    assert len(var1.building.lComponent) == 3

    # Check that the Geom updated properly
    assert p1 in var1.geom.polygons
    assert p2 in var1.geom.polygons
    assert p3 in var1.geom.polygons
    assert p4 in var1.geom.polygons
    assert p5 in var1.geom.polygons
    assert p6 in var1.geom.polygons

def test_get_zone_by_identifier():
    var1 = PHX.variant.Variant()
    z1 = PHX.variant.Zone()
    z2 = PHX.variant.Zone()
    z3 = PHX.variant.Zone()
    z4 = PHX.variant.Zone()
    z5 = PHX.variant.Zone()

    var1.add_zones( [z1, z2, z3, z4] )

    # Check an Identigier
    got_zone = var1.get_zone_by_identifier( z1.identifier )
    assert got_zone == z1
    assert z1 in var1.zones
    assert z2 in var1.zones
    assert z3 in var1.zones
    assert z4 in var1.zones

    # Check an Identifier
    got_zone = var1.get_zone_by_identifier( z5.identifier )
    assert not got_zone
    assert z1 in var1.zones
    assert z2 in var1.zones
    assert z3 in var1.zones
    assert z4 in var1.zones

    # Check not an Identifier
    got_zone = var1.get_zone_by_identifier('not an identifier')
    assert not got_zone
    assert z1 in var1.zones
    assert z2 in var1.zones
    assert z3 in var1.zones
    assert z4 in var1.zones