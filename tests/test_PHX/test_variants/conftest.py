import pytest
import PHX.variant

@pytest.fixture
def reset_variant_count():
    """Re-set the class _count variable in order to test incrementing properly"""

    PHX.variant.Zone._count = 0
    PHX.variant.Variant._count = 0

    yield

    PHX.variant.Zone._count = 0
    PHX.variant.Variant._count = 0