from PHX.geometry import Vector, Vertex, Polygon
import pytest

@pytest.fixture
def reset_geometry_count():
    Polygon._count = 9_999_999
    Vertex._count = 0
    yield
    Polygon._count = 9_999_999
    Vertex._count = 0