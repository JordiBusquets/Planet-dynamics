"""Unit tests for Planet class and model functions."""
import unittest
import math
from src.models import (
    Planet, set_up_positions, append_positions, distance_between_planets,
    combine_planets, static_sun, static_earth, random_sun, random_earth
)
from src.constants import R_sun, M_sun, R_earth, M_earth, D_earth_sun


class TestPlanetClass(unittest.TestCase):
    """Test Planet class initialization and methods."""

    def setUp(self):
        """Create a test planet."""
        self.planet = Planet(
            name="TestPlanet",
            radius=1000.0,
            mass=1e24,
            x=0.0, y=0.0, z=0.0,
            x_v=1.0, y_v=2.0, z_v=3.0,
            x_a=0.1, y_a=0.2, z_a=0.3
        )

    def test_planet_initialization(self):
        """Test planet initializes with correct attributes."""
        self.assertEqual(self.planet.name, "TestPlanet")
        self.assertEqual(self.planet.radius, 1000.0)
        self.assertEqual(self.planet.mass, 1e24)
        self.assertEqual(self.planet.x, 0.0)

    def test_volume_calculation(self):
        """Test volume calculation."""
        volume = self.planet.volume()
        expected_volume = (4.0 / 3.0) * math.pi * (1000.0 ** 3.0)
        self.assertAlmostEqual(volume, expected_volume)

    def test_density_calculation(self):
        """Test density calculation."""
        density = self.planet.density()
        expected_density = self.planet.mass / self.planet.volume()
        self.assertAlmostEqual(density, expected_density)

    def test_update_position(self):
        """Test position update."""
        delta_t = 1.0
        self.planet.update_position(delta_t)
        
        # x = 0 + 1.0 * 1.0 = 1.0
        self.assertAlmostEqual(self.planet.x, 1.0)
        # y = 0 + 2.0 * 1.0 = 2.0
        self.assertAlmostEqual(self.planet.y, 2.0)
        # z = 0 + 3.0 * 1.0 = 3.0
        self.assertAlmostEqual(self.planet.z, 3.0)

    def test_update_velocity(self):
        """Test velocity update."""
        delta_t = 2.0
        self.planet.update_velocity(delta_t)
        
        # x_v = 1.0 + 0.1 * 2.0 = 1.2
        self.assertAlmostEqual(self.planet.x_v, 1.2)
        # y_v = 2.0 + 0.2 * 2.0 = 2.4
        self.assertAlmostEqual(self.planet.y_v, 2.4)
        # z_v = 3.0 + 0.3 * 2.0 = 3.6
        self.assertAlmostEqual(self.planet.z_v, 3.6)

    def test_clear_acceleration(self):
        """Test acceleration clearing."""
        self.planet.clear_acceleration()
        self.assertEqual(self.planet.x_a, 0.0)
        self.assertEqual(self.planet.y_a, 0.0)
        self.assertEqual(self.planet.z_a, 0.0)

    def test_append_acceleration(self):
        """Test appending acceleration."""
        self.planet.clear_acceleration()
        self.planet.append_acceleration(0.5, 1.0, 1.5)
        
        self.assertAlmostEqual(self.planet.x_a, 0.5)
        self.assertAlmostEqual(self.planet.y_a, 1.0)
        self.assertAlmostEqual(self.planet.z_a, 1.5)
        
        # Append again
        self.planet.append_acceleration(0.5, 1.0, 1.5)
        self.assertAlmostEqual(self.planet.x_a, 1.0)
        self.assertAlmostEqual(self.planet.y_a, 2.0)
        self.assertAlmostEqual(self.planet.z_a, 3.0)


class TestPlanetFunctions(unittest.TestCase):
    """Test planet-related functions."""

    def test_set_up_positions(self):
        """Test position list initialization."""
        x, y, z = [], [], []
        set_up_positions(x, y, z, 3)
        
        self.assertEqual(len(x), 3)
        self.assertEqual(len(y), 3)
        self.assertEqual(len(z), 3)
        self.assertEqual(x[0], [])
        self.assertEqual(y[0], [])
        self.assertEqual(z[0], [])

    def test_append_positions(self):
        """Test appending planet positions."""
        planets = [
            Planet("P1", x=1.0, y=2.0, z=3.0),
            Planet("P2", x=4.0, y=5.0, z=6.0),
        ]
        x, y, z = [[]], [[]]
        set_up_positions(x, y, z, 2)
        
        append_positions(x, y, z, planets)
        
        self.assertEqual(x[0][0], 1.0)
        self.assertEqual(y[0][0], 2.0)
        self.assertEqual(z[0][0], 3.0)
        self.assertEqual(x[1][0], 4.0)
        self.assertEqual(y[1][0], 5.0)
        self.assertEqual(z[1][0], 6.0)

    def test_distance_between_planets(self):
        """Test distance calculation between planets."""
        p1 = Planet("P1", x=0.0, y=0.0, z=0.0)
        p2 = Planet("P2", x=3.0, y=4.0, z=0.0)
        
        distance = distance_between_planets(p1, p2)
        self.assertAlmostEqual(distance, 5.0)  # 3-4-5 triangle

    def test_distance_same_position(self):
        """Test distance when planets are at same position."""
        p1 = Planet("P1", x=1.0, y=1.0, z=1.0)
        p2 = Planet("P2", x=1.0, y=1.0, z=1.0)
        
        distance = distance_between_planets(p1, p2)
        self.assertAlmostEqual(distance, 0.0)

    def test_combine_planets(self):
        """Test combining two planets."""
        p1 = Planet("P1", mass=1e24, radius=1e6, x=0.0, y=0.0, z=0.0)
        p2 = Planet("P2", mass=1e24, radius=1e6, x=2e6, y=0.0, z=0.0)
        
        combined = combine_planets(p1, p2)
        
        self.assertEqual(combined.mass, 2e24)
        # Center of mass should be at (1e6, 0, 0) since masses are equal
        self.assertAlmostEqual(combined.x, 1e6, delta=1e-5)
        self.assertAlmostEqual(combined.y, 0.0)
        self.assertAlmostEqual(combined.z, 0.0)

    def test_static_sun(self):
        """Test static sun factory function."""
        sun = static_sun("TestSun")
        
        self.assertEqual(sun.name, "TestSun")
        self.assertEqual(sun.mass, M_sun)
        self.assertEqual(sun.radius, R_sun)
        self.assertEqual(sun.x, 0.0)
        self.assertEqual(sun.y, 0.0)
        self.assertEqual(sun.z, 0.0)
        self.assertEqual(sun.x_v, 0.0)

    def test_static_earth(self):
        """Test static earth factory function."""
        earth = static_earth("TestEarth")
        
        self.assertEqual(earth.name, "TestEarth")
        self.assertEqual(earth.mass, M_earth)
        self.assertEqual(earth.radius, R_earth)
        self.assertEqual(earth.x, 0.0)
        self.assertEqual(earth.y, 0.0)
        self.assertEqual(earth.z, 0.0)

    def test_random_sun(self):
        """Test random sun factory function."""
        sun = random_sun("RandomSun")
        
        self.assertEqual(sun.name, "RandomSun")
        self.assertEqual(sun.mass, M_sun)
        self.assertEqual(sun.radius, R_sun)
        # Position and velocity should be non-zero and in reasonable range
        self.assertNotEqual(sun.x, 0.0)

    def test_random_earth(self):
        """Test random earth factory function."""
        earth = random_earth("RandomEarth")
        
        self.assertEqual(earth.name, "RandomEarth")
        self.assertEqual(earth.mass, M_earth)
        self.assertEqual(earth.radius, R_earth)


if __name__ == '__main__':
    unittest.main()
