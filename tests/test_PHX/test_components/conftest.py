import PHX.component
import pytest
import PHX.geometry

# -- Ladybug Geometry
# -------------------------------------------------------------------------------
@pytest.fixture()
def poly_1():
    p1 = PHX.geometry.Polygon()
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 10, 0)
    v3 = PHX.geometry.Vertex(10, 10, 0)
    v4 = PHX.geometry.Vertex(0, 10, 0)

    p1.vertices.append(v1)
    p1.vertices.append(v2)
    p1.vertices.append(v3)
    p1.vertices.append(v4)

    return p1


@pytest.fixture()
def poly_2():
    p1 = PHX.geometry.Polygon()
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, -10, 0)
    v3 = PHX.geometry.Vertex(-10, -10, 0)
    v4 = PHX.geometry.Vertex(0, -10, 0)

    p1.vertices.append(v1)
    p1.vertices.append(v2)
    p1.vertices.append(v3)
    p1.vertices.append(v4)

    return p1


@pytest.fixture()
def poly_3():
    p1 = PHX.geometry.Polygon()
    v1 = PHX.geometry.Vertex(0, 0, 0)
    v2 = PHX.geometry.Vertex(0, 10, 0)
    v3 = PHX.geometry.Vertex(10, 10, 0)
    v4 = PHX.geometry.Vertex(0, 10, 0)

    p1.vertices.append(v1)
    p1.vertices.append(v2)
    p1.vertices.append(v3)
    p1.vertices.append(v4)

    return p1


@pytest.fixture
def reset_component_count():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.component.Component._count = 0

    yield

    PHX.component.Component._count = 0
