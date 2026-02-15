"""Unit tests for main module."""
import unittest
from unittest.mock import patch

from pytest import fixture
from src.main import planet_dynamics
from src.constants import M_earth, R_sun, D_earth_sun, V_earth, G
from src.models import Planet, static_sun, static_earth

@fixture
def planets() -> list[Planet]:
    return [
        static_sun("1"),
        Planet("2", R_sun, M_earth, D_earth_sun, 0.0, 0.0, 0.0, V_earth, 0.0)
    ]

class TestPlanetDynamics(unittest.TestCase):
    """Test planet_dynamics function."""

    @patch('src.main.set_up_plot')
    @patch('src.main.update_plot')
    @patch('src.main.plt.show')
    def test_planet_dynamics_without_plot(self, mock_show, mock_update, mock_setup, planets):
        """Test planet_dynamics runs without plotting."""
        x, y, z = planet_dynamics(planets=planets, time_horizon=0.1, time_step=0.01, make_plot=False)
        
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        self.assertIsNotNone(z)
        # Verify plot functions were not called
        mock_setup.assert_not_called()
        mock_update.assert_not_called()
        mock_show.assert_not_called()

    @patch('src.main.plt.show')
    def test_planet_dynamics_returns_positions(self, planets):
        """Test planet_dynamics returns position arrays."""
        x, y, z = planet_dynamics(planets=planets, time_horizon=0.01, time_step=0.01, make_plot=False)
        
        # Should return three lists (one for each planet)
        self.assertIsInstance(x, list)
        self.assertIsInstance(y, list)
        self.assertIsInstance(z, list)
        
        # Should have data for at least 2 planets
        self.assertGreaterEqual(len(x), 2)
        self.assertGreaterEqual(len(y), 2)
        self.assertGreaterEqual(len(z), 2)

    def test_planet_dynamics_short_simulation(self, planets):
        """Test a very short simulation completes."""
        try:
            x, y, z = planet_dynamics(planets=planets, time_horizon=0.001, time_step=0.001, make_plot=False)
            self.assertIsNotNone(x)
            self.assertIsNotNone(y)
            self.assertIsNotNone(z)
        except Exception as e:
            self.fail(f"planet_dynamics raised {type(e).__name__} unexpectedly: {e}")
