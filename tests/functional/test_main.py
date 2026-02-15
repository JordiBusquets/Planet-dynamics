"""Unit tests for main module."""
from unittest.mock import patch

import pytest

from src.main import planet_dynamics
from src.constants import M_earth, R_sun, D_earth_sun, V_earth
from src.models.planet import Planet, static_sun


@pytest.fixture
def planets() -> list[Planet]:
    """Create test planets."""
    return [
        static_sun("1"),
        Planet("2", R_sun, M_earth, D_earth_sun, 0.0, 0.0, 0.0, V_earth, 0.0)
    ]


@patch('src.main.set_up_plot')
@patch('src.main.update_plot')
@patch('src.main.plt.show')
def test_planet_dynamics_without_plot(mock_show, mock_update, mock_setup, planets):
    """Test planet_dynamics runs without plotting."""
    x, y, z = planet_dynamics(planets=planets, time_horizon=0.1, time_step=0.01, make_plot=False)
    
    assert x is not None
    assert y is not None
    assert z is not None
    # Verify plot functions were not called
    mock_setup.assert_not_called()
    mock_update.assert_not_called()
    mock_show.assert_not_called()


@patch('src.main.plt.show')
def test_planet_dynamics_returns_positions(mock_show, planets):
    """Test planet_dynamics returns position arrays."""
    x, y, z = planet_dynamics(planets=planets, time_horizon=0.01, time_step=0.01, make_plot=False)
    
    # Should return three lists (one for each planet)
    assert isinstance(x, list)
    assert isinstance(y, list)
    assert isinstance(z, list)
    
    # Should have data for at least 2 planets
    assert len(x) >= 2
    assert len(y) >= 2
    assert len(z) >= 2
