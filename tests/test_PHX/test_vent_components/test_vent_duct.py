import PHX.ventilation_components


def test_vent_duct(reset_vent_components):
    c1 = PHX.ventilation_components.Ventilation_Duct()
    c2 = PHX.ventilation_components.Ventilation_Duct()

    assert c1 and c2
    assert c1 != c2


def test_default_vent_duct(reset_vent_components):
    c1 = PHX.ventilation_components.Ventilation_Duct.default()
    c2 = PHX.ventilation_components.Ventilation_Duct.default()

    assert c1 and c2
    assert c1 == c2


def test_duct_length(reset_vent_components):
    seg1 = PHX.ventilation_components.Ventilation_Duct_Segment()
    seg1.length = 12
    seg2 = PHX.ventilation_components.Ventilation_Duct_Segment()
    seg2.length = 13
    seg3 = PHX.ventilation_components.Ventilation_Duct_Segment()
    seg3.length = 25

    c1 = PHX.ventilation_components.Ventilation_Duct()
    c1.segments = [seg1, seg2]
    assert c1.length == 25

    c1.segments.append(seg3)
    assert c1.length == 50


def test_add_ducts(reset_vent_components):
    seg1 = PHX.ventilation_components.Ventilation_Duct_Segment()
    seg1.length = 12
    seg2 = PHX.ventilation_components.Ventilation_Duct_Segment()
    seg2.length = 13
    seg3 = PHX.ventilation_components.Ventilation_Duct_Segment()
    seg3.length = 25

    c1 = PHX.ventilation_components.Ventilation_Duct()
    c1.segments = [seg1, seg2]
    assert c1.length == 25

    c2 = PHX.ventilation_components.Ventilation_Duct()
    c2.segments.append(seg3)
    assert c2.length == 25

    c3 = c1 + c2
    assert c3.length == 50


def test_sum_ducts(reset_vent_components):
    seg1 = PHX.ventilation_components.Ventilation_Duct_Segment()
    seg1.length = 12
    seg2 = PHX.ventilation_components.Ventilation_Duct_Segment()
    seg2.length = 13
    c1 = PHX.ventilation_components.Ventilation_Duct()
    c1.segments = [seg1, seg2]
    assert len(c1.segments) == 2
    assert c1.length == 25

    seg3 = PHX.ventilation_components.Ventilation_Duct_Segment()
    seg3.length = 25
    c2 = PHX.ventilation_components.Ventilation_Duct()
    c2.segments.append(seg3)
    assert len(c2.segments) == 1
    assert c2.length == 25

    seg4 = PHX.ventilation_components.Ventilation_Duct_Segment()
    seg4.length = 35
    c3 = PHX.ventilation_components.Ventilation_Duct()
    c3.segments.append(seg4)
    assert len(c3.segments) == 1
    assert c3.length == 35

    c4 = sum((c1, c2, c3))
    assert len(c4.segments) == 4
    assert c4.length == 85

    c5 = sum((c1, c2, c3), start=PHX.ventilation_components.Ventilation_Duct())
    assert len(c5.segments) == 4
    assert c5.length == 85
