"""Unit tests for physics mechanics module."""
import unittest
from src.physics.mechanics import compute_accelerations, gravitational_force, gravitational_acceleration

from src.models.planet import Planet, static_sun, static_earth
from src.constants import G, M_sun, M_earth


class TestGravitationalForce(unittest.TestCase):
    """Test gravitational force calculation."""

    def test_gravitational_force_positive(self):
        """Test gravitational force is positive."""
        p1 = Planet("P1", mass=1e24)
        p2 = Planet("P2", mass=1e24, x=1e10, y=0.0, z=0.0)
        
        force = gravitational_force(p1, p2)
        self.assertGreater(force, 0)

    def test_gravitational_force_symmetry(self):
        """Test Newton's third law: F12 = F21."""
        p1 = Planet("P1", mass=1e24, x=0.0, y=0.0, z=0.0)
        p2 = Planet("P2", mass=2e24, x=1e10, y=0.0, z=0.0)
        
        force_12 = gravitational_force(p1, p2)
        force_21 = gravitational_force(p2, p1)
        
        self.assertAlmostEqual(force_12, force_21)

    def test_gravitational_force_inverse_square(self):
        """Test that force follows inverse square law."""
        p1 = Planet("P1", mass=1e24)
        
        # At distance d
        p2_near = Planet("P2", mass=1e24, x=1e10, y=0.0, z=0.0)
        force_near = gravitational_force(p1, p2_near)
        
        # At distance 2d
        p2_far = Planet("P2", mass=1e24, x=2e10, y=0.0, z=0.0)
        force_far = gravitational_force(p1, p2_far)
        
        # Force should be 1/4 at 2x distance
        ratio = force_near / force_far
        self.assertAlmostEqual(ratio, 4.0, places=5)

    def test_gravitational_force_formula(self):
        """Test against known gravitational force formula."""
        m1, m2 = 1e24, 1e24
        d = 1e10
        
        p1 = Planet("P1", mass=m1)
        p2 = Planet("P2", mass=m2, x=d, y=0.0, z=0.0)
        
        force = gravitational_force(p1, p2)
        expected = G * m1 * m2 / (d * d)
        
        self.assertAlmostEqual(force, expected, delta=expected * 1e-10)


class TestGravitationalAcceleration(unittest.TestCase):
    """Test gravitational acceleration calculation."""

    def test_acceleration_positive(self):
        """Test acceleration is positive."""
        force = 1e20
        planet = Planet("P", mass=1e24)
        
        acceleration = gravitational_acceleration(force, planet)
        self.assertGreater(acceleration, 0)

    def test_acceleration_formula(self):
        """Test acceleration calculation."""
        force = 1e20
        mass = 1e24
        planet = Planet("P", mass=mass)
        
        acceleration = gravitational_acceleration(force, planet)
        expected = (force / mass) ** 0.5
        
        self.assertAlmostEqual(acceleration, expected)


class TestComputeAccelerations(unittest.TestCase):
    """Test acceleration computation for planet systems."""

    def test_single_planet_no_acceleration(self):
        """Test single planet has no acceleration (no other bodies)."""
        planet = Planet("P", x=0.0, y=0.0, z=0.0)
        planets = [planet]
        
        compute_accelerations(planets)
        
        self.assertEqual(planet.x_a, 0.0)
        self.assertEqual(planet.y_a, 0.0)
        self.assertEqual(planet.z_a, 0.0)

    def test_two_planets_acceleration_nonzero(self):
        """Test two planets experience acceleration."""
        p1 = Planet("P1", mass=1e24, x=0.0, y=0.0, z=0.0)
        p2 = Planet("P2", mass=1e24, x=1e10, y=0.0, z=0.0)
        planets = [p1, p2]
        
        compute_accelerations(planets)
        
        # Both planets should have non-zero acceleration
        self.assertNotEqual(p1.x_a, 0.0)
        self.assertNotEqual(p2.x_a, 0.0)

    def test_acceleration_clears_before_compute(self):
        """Test that accelerations are cleared before computation."""
        planet = Planet("P", mass=1e24, x=0.0, y=0.0, z=0.0, x_a=100.0)
        planets = [planet]
        
        compute_accelerations(planets)
        
        # Should be cleared since it's the only planet
        self.assertEqual(planet.x_a, 0.0)

    def test_newtons_third_law_system(self):
        """Test Newton's third law in multi-body system."""
        p1 = Planet("P1", mass=1e24, x=0.0, y=0.0, z=0.0)
        p2 = Planet("P2", mass=1e24, x=1e10, y=0.0, z=0.0)
        planets = [p1, p2]
        
        compute_accelerations(planets)
        
        # For equal masses, accelerations should be opposite
        # a1 = -a2 in x direction
        self.assertAlmostEqual(p1.x_a, -p2.x_a, places=5)
