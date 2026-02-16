"""Unit tests for Planet class and model functions."""
import unittest
import math
from src.planet import (
    Planet, set_up_positions, append_positions, distance_between_planets,
    combine_planets, static_sun, static_earth, random_sun, random_earth
)
from src.constants import R_sun, M_sun, R_earth, M_earth, D_earth_sun
from src.main import planet_dynamics, DAYS_IN_YEAR


def test_planet_dynamics() -> None:
    """Test main simulation function."""
    # Create two planets with known initial conditions
    planets = [Planet("1", mass=1e9, x=-1000.0), Planet("2", mass=1e9, x=1000.0)]
    
    # Run the simulation for a short time horizon
    time_horizon = 1.0 / 24.0 / DAYS_IN_YEAR  # one hour, in years
    time_step = 1.0 / 24.0 / 60.0  # one minute, in days
    
    x, y, z = planet_dynamics(planets, time_horizon, time_step, make_plot=False)
    
    # Check that positions were recorded
    assert len(x) == len(y) == len(z) == 2
    assert len(x[0]) == len(y[0]) == len(z[0]) == 62
    assert len(x[1]) == len(y[1]) == len(z[1]) == 62
    assert all(i == 0.0 for i in y[0])
    assert all(i == 0.0 for i in y[1])
    assert all(i == 0.0 for i in z[0])
    assert all(i == 0.0 for i in z[1])

    assert math.isclose(x[0][0], -1000.0, abs_tol=1e-2)
    assert math.isclose(x[1][0], 1000.0, abs_tol=1e-2)
    assert math.isclose(x[0][1], -999.53, abs_tol=1e-2)
    assert math.isclose(x[1][1], 999.53, abs_tol=1e-2)
    assert math.isclose(x[0][10], -974.32, abs_tol=1e-2)
    assert math.isclose(x[1][10], 974.32, abs_tol=1e-2)
    assert math.isclose(x[0][57], -39.48, abs_tol=1e-2)
    assert math.isclose(x[1][57], 39.48, abs_tol=1e-2)
    
