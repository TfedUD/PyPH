import PHX.bldg_segment


def test_PHIUS_Cert_serialization(reset_bldg_segment_count):
    o1 = PHX.bldg_segment.PHIUSCertification()
    d = o1.to_dict()

    o2 = PHX.bldg_segment.PHIUSCertification.from_dict(d)

    assert d == o2.to_dict()
