import PHX._base


def test_base():
    b = PHX._base._Base()

    assert str(b.identifier_short) in str(b)
    assert str(b.identifier_short) in b.ToString()
    assert str(b.identifier_short) in repr(b)


def test_base_to_dict():
    b = PHX._base._Base()
    assert hasattr(b, "to_dict")

    d = b.to_dict()
    assert str(b.identifier) in d.values()
    assert b.user_data in d.values()
