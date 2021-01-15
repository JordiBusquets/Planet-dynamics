from planet import planet, distance_between_planets, static_earth
from typing import List
from constants import G


def gravitational_force(p1, p2):
    d = distance_between_planets(p1, p2)
    f = G * p1.mass * p2.mass / (d * d)
    return f


def gravitational_acceleration(f, p):
    return (f / p.mass) ** 0.5


def compute_accelerations(planets: List[planet]):
    n = len(planets)

    i = 0
    while i < n:
        planets[i].clear_acceleration()
        i += 1

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
            planets[i_lhs].append_acceleration(a_lhs * d_x / d, a_lhs * d_y / d, a_lhs * d_z / d)
            planets[i_rhs].append_acceleration(-a_rhs * d_x / d, -a_rhs * d_y / d, -a_rhs * d_z / d)
            i_rhs += 1
        i_lhs += 1
    return 0


def stable_circular_orbit_earth(p, x):
    earth = static_earth("earth")
    earth.x = x
    f = gravitational_force(p, earth)
    a = gravitational_acceleration(f, earth)
    earth.y_v = (a * x) ** 0.5
    return earth
