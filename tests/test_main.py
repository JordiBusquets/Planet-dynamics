"""Unit tests for Planet class and model functions."""
import unittest
import math
from src.planet import (
    Planet, set_up_positions, append_positions, distance_between_planets,
    combine_planets, static_sun, static_earth, random_sun, random_earth
)
from src.constants import R_sun, M_sun, R_earth, M_earth, D_earth_sun
from src.main import planet_dynamics, DAYS_IN_YEAR


def test_main() -> None:
    """Test main simulation function."""
    # Create two planets with known initial conditions
    planets = [Planet("1", mass=M_earth, x=0.0), Planet("2", mass=M_earth, x=1000.0)]
    
    # Run the simulation for a short time horizon
    time_horizon = 100.0 / DAYS_IN_YEAR  # in years
    time_step = 1.0  # in days
    
    x, y, z = planet_dynamics(planets, time_horizon, time_step, make_plot=False)
    
    # Check that positions were recorded
    assert len(x) == len(y) == len(z) == 2
    assert len(x[0]) == len(y[0]) == len(z[0]) == 101
    assert len(x[1]) == len(y[1]) == len(z[1]) == 101
    
