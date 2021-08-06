import PHX.component
import pytest


@pytest.fixture
def reset_component_count():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.component.Component._count = 0

    yield

    PHX.component.Component._count = 0
