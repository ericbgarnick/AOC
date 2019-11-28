import pytest

from team_unit import TeamUnit


def using_health(health_e, health_g):
    """A decorator to set the health_to_set
    attribute for individual tests."""
    def wrap(func):
        setattr(func, 'health_for_e', health_e)
        setattr(func, 'health_for_g', health_g)
        return func
    return wrap


@pytest.fixture(scope='function')
def unit_health(request):
    max_health_e = getattr(request.function, 'health_for_e')
    max_health_g = getattr(request.function, 'health_for_g')
    setattr(TeamUnit, 'MAX_HEALTH_E', max_health_e)
    setattr(TeamUnit, 'MAX_HEALTH_G', max_health_g)
