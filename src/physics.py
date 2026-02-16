"""Physics calculations for planet dynamics."""
import math
from typing import List
from src.constants import G
from src.planet import Planet, distance_between_planets, static_earth


def gravitational_force(p1: Planet, p2: Planet) -> float:
    """Calculate the gravitational force between two planets."""
    d = distance_between_planets(p1, p2)
    f = G * p1.mass * p2.mass / (d ** 2)
    return f


def gravitational_acceleration(force: float, p: Planet) -> float:
    """Calculate the gravitational acceleration from a force."""
    return math.sqrt(force / p.mass)


def compute_accelerations(planets: List[Planet]) -> None:
    """Compute gravitational accelerations for all planets due to mutual forces."""
    n = len(planets)

    # Clear existing accelerations
    i = 0
    while i < n:
        planets[i].clear_acceleration()
        i += 1

    # Compute pairwise gravitational interactions
    i_lhs = 0
    while i_lhs < n - 1:
        p_lhs = planets[i_lhs]
        i_rhs = i_lhs + 1
        while i_rhs < n:
            p_rhs = planets[i_rhs]
            f = gravitational_force(p_lhs, p_rhs)  # absolute force
            a_lhs = gravitational_acceleration(f, p_lhs)  # absolute acceleration on p_lhs
            a_rhs = gravitational_acceleration(f, p_rhs)  # absolute acceleration on p_rhs
            d = distance_between_planets(p_lhs, p_rhs)
            d_x = p_rhs.x - p_lhs.x
            d_y = p_rhs.y - p_lhs.y
            d_z = p_rhs.z - p_lhs.z
            planets[i_lhs].update_acceleration(a_lhs * d_x / d, a_lhs * d_y / d, a_lhs * d_z / d)
            planets[i_rhs].update_acceleration(-a_rhs * d_x / d, -a_rhs * d_y / d, -a_rhs * d_z / d)
            i_rhs += 1
        i_lhs += 1
