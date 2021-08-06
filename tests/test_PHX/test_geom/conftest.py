import PHX.geometry
import pytest


@pytest.fixture
def reset_geometry_count():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.geometry.Polygon._count = 9_999_999
    PHX.geometry.Vertex._count = 0

    yield

    PHX.geometry.Polygon._count = 9_999_999
    PHX.geometry.Vertex._count = 0
