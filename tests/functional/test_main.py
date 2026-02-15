"""Unit tests for main module."""
import unittest
from unittest.mock import patch
from src.main import planet_dynamics


class TestPlanetDynamics(unittest.TestCase):
    """Test planet_dynamics function."""

    @patch('src.main.set_up_plot')
    @patch('src.main.update_plot')
    @patch('src.main.plt.show')
    def test_planet_dynamics_without_plot(self, mock_show, mock_update, mock_setup):
        """Test planet_dynamics runs without plotting."""
        x, y, z = planet_dynamics(horizon=0.1, step=0.01, make_plot=False)
        
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        self.assertIsNotNone(z)
        # Verify plot functions were not called
        mock_setup.assert_not_called()
        mock_update.assert_not_called()
        mock_show.assert_not_called()

    @patch('src.main.plt.show')
    def test_planet_dynamics_returns_positions(self, mock_show):
        """Test planet_dynamics returns position arrays."""
        x, y, z = planet_dynamics(horizon=0.01, step=0.01, make_plot=False)
        
        # Should return three lists (one for each planet)
        self.assertIsInstance(x, list)
        self.assertIsInstance(y, list)
        self.assertIsInstance(z, list)
        
        # Should have data for at least 2 planets
        self.assertGreaterEqual(len(x), 2)
        self.assertGreaterEqual(len(y), 2)
        self.assertGreaterEqual(len(z), 2)

    def test_planet_dynamics_short_simulation(self):
        """Test a very short simulation completes."""
        try:
            x, y, z = planet_dynamics(horizon=0.001, step=0.001, make_plot=False)
            self.assertIsNotNone(x)
            self.assertIsNotNone(y)
            self.assertIsNotNone(z)
        except Exception as e:
            self.fail(f"planet_dynamics raised {type(e).__name__} unexpectedly: {e}")


if __name__ == '__main__':
    unittest.main()
