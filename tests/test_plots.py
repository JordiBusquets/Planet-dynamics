"""Unit tests for visualization module."""
import unittest
from unittest.mock import patch, MagicMock
from src.plots import compute_limit
from src.planet import Planet
from src.constants import R_earth


class TestComputeLimit(unittest.TestCase):
    """Test plot limit calculation."""

    def test_single_planet_single_axis(self) -> None:
        """Test limit calculation for single planet on x-axis."""
        planet = Planet("P", x=1e11, y=0.0, z=0.0)
        planets = [planet]
        
        lim_min, lim_max = compute_limit(planets, 1)
        
        # Min should be -R_earth, max should be at least 1e11
        self.assertLess(lim_min, 0)
        self.assertGreaterEqual(lim_max, 1e11)

    def test_limit_includes_planet_radius(self) -> None:
        """Test that limits account for planet radius."""
        planet = Planet("P", radius=R_earth, x=0.0, y=0.0, z=0.0)
        planets = [planet]
        
        lim_min, lim_max = compute_limit(planets, 1)
        
        # Should include at least R_earth margin
        self.assertLessEqual(lim_min, -R_earth)
        self.assertGreaterEqual(lim_max, R_earth)

    def test_multiple_planets_y_axis(self) -> None:
        """Test limit calculation for multiple planets on y-axis."""
        p1 = Planet("P1", x=0.0, y=1e11, z=0.0)
        p2 = Planet("P2", x=0.0, y=-5e10, z=0.0)
        planets = [p1, p2]
        
        lim_min, lim_max = compute_limit(planets, 2)
        
        self.assertLessEqual(lim_min, -5e10)
        self.assertGreaterEqual(lim_max, 1e11)

    def test_negative_coordinates(self) -> None:
        """Test with negative planet positions."""
        planet = Planet("P", x=-1e11, y=0.0, z=0.0)
        planets = [planet]
        
        lim_min, lim_max = compute_limit(planets, 1)
        
        self.assertLessEqual(lim_min, -1e11)

    def test_current_limits_respected(self) -> None:
        """Test that current limits are considered."""
        planet = Planet("P", x=5e10, y=0.0, z=0.0)
        planets = [planet]
        
        # Provide larger initial limits
        lim_min, lim_max = compute_limit(planets, 1, current_lim_min=-1e11, current_lim_plus=1e11)
        
        # Should respect or expand the provided limits
        self.assertLessEqual(lim_min, -1e11)
        self.assertGreaterEqual(lim_max, 1e11)

    def test_z_axis_computation(self) -> None:
        """Test limit computation for z-axis."""
        planet = Planet("P", x=0.0, y=0.0, z=2e10)
        planets = [planet]
        
        lim_min, lim_max = compute_limit(planets, 3)
        
        self.assertLess(lim_min, 0)
        self.assertGreaterEqual(lim_max, 2e10)

    def test_zero_position_planet(self) -> None:
        """Test limit calculation for planet at origin."""
        planet = Planet("P", x=0.0, y=0.0, z=0.0, radius=R_earth)
        planets = [planet]
        
        lim_min, lim_max = compute_limit(planets, 1)
        
        # Limits should be symmetric around origin with R_earth margin
        self.assertAlmostEqual(lim_min, -R_earth)
        self.assertAlmostEqual(lim_max, R_earth)

    def test_dimension_parameter(self) -> None:
        """Test that dimension parameter correctly selects axis."""
        p1 = Planet("P1", x=1e11, y=2e11, z=3e11)
        planets = [p1]
        
        lim_min_x, lim_max_x = compute_limit(planets, 1)
        lim_min_y, lim_max_y = compute_limit(planets, 2)
        lim_min_z, lim_max_z = compute_limit(planets, 3)
        
        # Max for each dimension should be greater than respective coordinate
        self.assertGreaterEqual(lim_max_x, 1e11)
        self.assertGreaterEqual(lim_max_y, 2e11)
        self.assertGreaterEqual(lim_max_z, 3e11)


if __name__ == '__main__':
    unittest.main()
