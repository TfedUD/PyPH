import PHX.variant

def  test_variant_identifier():
    v1 = PHX.variant.Variant()
    v2 = PHX.variant.Variant()

    assert v1.identifier != v2.identifier