from PHX.geometry import Vector

def test_Vector_identifier():
    v1 = Vector()
    v2 = Vector()

    assert v1.identifier != v2.identifier

def test_Vector_attributes():
    v1 = Vector()

    assert v1.x == 0
    assert v1.y == 0
    assert v1.z == 0
    assert not v1.user_data

    v1.x = 12
    v1.y = 13
    v1.z = 14
    
    assert v1.x == 12
    assert v1.y == 13
    assert v1.z == 14

    v2 = Vector(15,16,17)
    assert v2.x == 15
    assert v2.y == 16
    assert v2.z == 17
    assert not v2.user_data
