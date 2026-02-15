"""Unit tests for physics mechanics module."""
import unittest
from src.physics.mechanics import compute_accelerations, gravitational_force, gravitational_acceleration

from src.models.planet import Planet, static_sun, static_earth
from src.constants import G, M_sun, M_earth


class TestGravitationalForce(unittest.TestCase):
    """Test gravitational force calculation."""

    def test_gravitational_force_positive(self) -> None:
        """Test gravitational force is positive."""
        p1 = Planet("P1", mass=1e24)
        p2 = Planet("P2", mass=1e24, x=1e10, y=0.0, z=0.0)
        
        force = gravitational_force(p1, p2)
        self.assertGreater(force, 0)
        self.assertAlmostEqual(force, 6.674299999999999e+17, places=5)

    def test_gravitational_force_symmetry(self) -> None:
        """Test Newton's third law: F12 = F21."""
        p1 = Planet("P1", mass=1e24, x=0.0, y=0.0, z=0.0)
        p2 = Planet("P2", mass=2e24, x=1e10, y=0.0, z=0.0)
        
        force_12 = gravitational_force(p1, p2)
        force_21 = gravitational_force(p2, p1)
        
        self.assertAlmostEqual(force_12, force_21)

    def test_gravitational_force_inverse_square(self) -> None:
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

    def test_gravitational_force_formula(self) -> None:
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

    def test_acceleration_positive(self) -> None:
        """Test acceleration is positive."""
        force = 1e20
        planet = Planet("P", mass=1e24)
        
        acceleration = gravitational_acceleration(force, planet)
        self.assertGreater(acceleration, 0)

    def test_acceleration_formula(self) -> None:
        """Test acceleration calculation."""
        force = 1e20
        mass = 1e24
        planet = Planet("P", mass=mass)
        
        acceleration = gravitational_acceleration(force, planet)
        expected = (force / mass) ** 0.5
        
        self.assertAlmostEqual(acceleration, expected)


class TestComputeAccelerations(unittest.TestCase):
    """Test acceleration computation for planet systems."""

    def test_single_planet_no_acceleration(self) -> None:
        """Test single planet has no acceleration (no other bodies)."""
        planet = Planet("P", x=0.0, y=0.0, z=0.0)
        planets = [planet]
        
        compute_accelerations(planets)
        
        self.assertEqual(planet.x_a, 0.0)
        self.assertEqual(planet.y_a, 0.0)
        self.assertEqual(planet.z_a, 0.0)

    def test_acceleration_clears_before_compute(self):
        """Test that accelerations are cleared before computation."""
        planet = Planet("P", mass=1e24, x=0.0, y=0.0, z=0.0, x_a=100.0)
        planets = [planet]
        
        compute_accelerations(planets)
        
        # Should be cleared since it's the only planet
        self.assertEqual(planet.x_a, 0.0)

    def test_newtons_third_law_system_two_planets(self):
        """Test Newton's third law in multi-body system."""
        p1 = Planet("P1", mass=1e24, x=0.0, y=0.0, z=0.0, x_v=1.0, y_v=2.0, z_v=3.0)
        p2 = Planet("P2", mass=1e24, x=1e7, y=0.0, z=0.0, x_v=-4.0, y_v=-5.0, z_v=-6.0)
        planets = [p1, p2]
        
        compute_accelerations(planets)
        
        # For equal masses, accelerations should be opposite
        # a1 = -a2 in x direction.
        # P1 should accelerate towards P2 (positive x), P2 should accelerate towards P1 (negative x)
        self.assertAlmostEqual(p1.x_a, -p2.x_a, places=5)
        self.assertAlmostEqual(p1.x_a, 0.816963, places=5)
        self.assertAlmostEqual(p2.x_a, -0.816963, places=5)
        self.assertAlmostEqual(p1.y_a, 0.0, places=5)
        self.assertAlmostEqual(p2.y_a, 0.0, places=5)
        self.assertAlmostEqual(p1.z_a, 0.0, places=5)
        self.assertAlmostEqual(p2.z_a, 0.0, places=5)

        for p in planets:
            p.update_velocity(1.0)  # Update velocity for 1 second

        # Given the initial velocities, accelerations should
        # cause a change in velocity in the x direction for both planets
        self.assertAlmostEqual(p1.x_v, 1.0 + 0.816963, places=5)
        self.assertAlmostEqual(p2.x_v, -4.0 - 0.816963, places=5)
        self.assertAlmostEqual(p1.y_v, 2.0, places=5)
        self.assertAlmostEqual(p2.y_v, -5.0, places=5)
        self.assertAlmostEqual(p1.z_v, 3.0, places=5)
        self.assertAlmostEqual(p2.z_v, -6.0, places=5)

    def test_newtons_third_law_system_three_planets(self):
        """Test Newton's third law in multi-body system."""
        p1 = Planet("P1", mass=1e24, x=0.0, y=0.0, z=0.0, x_v=1.0, y_v=2.0, z_v=3.0)
        p2 = Planet("P2", mass=1e24, x=1e7, y=0.0, z=0.0, x_v=-4.0, y_v=-5.0, z_v=-6.0)
        p3 = Planet("P3", mass=1e24, x=0.5e7, y=1e7, z=0.0, x_v=7.0, y_v=8.0, z_v=9.0)
        planets = [p1, p2, p3]
        
        compute_accelerations(planets)
        
        # The planets form a triangle:
        # P1 at (0, 0), P2 at (1e7, 0), P3 at (0.5e7, 1e7)
        # Each planet should feel a net acceleration towards the other two.
        
        # On the x axis, P1 and P2 should have opposite accelerations, while P3 should have no acceleration
        self.assertAlmostEqual(p1.x_a, -p2.x_a, places=5)
        self.assertAlmostEqual(p1.x_a, 1.143749, places=5)
        self.assertAlmostEqual(p2.x_a, -1.143749, places=5)
        self.assertAlmostEqual(p3.x_a, 0.0, places=5)

        # On the y axis, P1 should accelerate towards P3, P2 should accelerate towards P3, and P3 should accelerate towards both P1 and P2
        self.assertAlmostEqual(p1.y_a, p2.y_a, places=5)
        self.assertAlmostEqual(p1.y_a, 0.65357, places=5)
        self.assertAlmostEqual(p2.y_a, 0.65357, places=5)
        self.assertAlmostEqual(p3.y_a, -1.307142, places=5)

        # On the z axis, there should be no acceleration for any planet
        self.assertAlmostEqual(p1.z_a, 0.0, places=5)
        self.assertAlmostEqual(p2.z_a, 0.0, places=5)
        self.assertAlmostEqual(p3.z_a, 0.0, places=5)

        for p in planets:
            p.update_velocity(1.0)  # Update velocity for 1 second

        # Given the initial velocities, accelerations should
        # cause a change in velocity in the x direction for both planets
        self.assertAlmostEqual(p1.x_v, 1.0+1.143749, places=5)
        self.assertAlmostEqual(p2.x_v, -4.0-1.143749, places=5)
        self.assertAlmostEqual(p3.x_v, 7.0, places=5)

        self.assertAlmostEqual(p1.y_v, 2.0+0.6535711, places=5)
        self.assertAlmostEqual(p2.y_v, -5.0+0.65357, places=5)
        self.assertAlmostEqual(p3.y_v, 8.0-1.307142, places=5)
        
        self.assertAlmostEqual(p1.z_v, 3.0, places=5)
        self.assertAlmostEqual(p2.z_v, -6.0, places=5)
        self.assertAlmostEqual(p3.z_v, 9.0, places=5)