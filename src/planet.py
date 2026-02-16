"""Planet model for dynamics simulation."""
import math
from typing import List
from src.constants import R_earth, R_sun, M_earth, M_sun, D_earth_sun, V_earth
import numpy as np


class Planet(object):
    """Represents a celestial body with position, velocity, and acceleration."""
    
    def __init__(self,
                 name: str,
                 radius: float = 1.0,
                 mass: float = 1.0,
                 x: float = 0., y: float = 0., z: float = 0.,
                 x_v: float = 0., y_v: float = 0., z_v: float = 0.,
                 x_a: float = 0., y_a: float = 0., z_a: float = 0.) -> None:
        self.name = name
        self.radius = radius
        self.mass = mass
        self.x = x
        self.y = y
        self.z = z
        self.x_v = x_v
        self.y_v = y_v
        self.z_v = z_v
        self.x_a = x_a
        self.y_a = y_a
        self.z_a = z_a

    def volume(self) -> float:
        """Calculate the volume of the planet."""
        return (4.0 / 3.0) * math.pi * (self.radius ** 3.0)

    def density(self) -> float:
        """Calculate the density of the planet."""
        return self.mass / self.volume()

    def update_position(self, delta_t: float) -> None:
        """Update position based on velocity and time step."""
        self.x += self.x_v * delta_t
        self.y += self.y_v * delta_t
        self.z += self.z_v * delta_t

    def update_velocity(self, delta_t: float) -> None:
        """Update velocity based on acceleration and time step."""
        self.x_v += self.x_a * delta_t
        self.y_v += self.y_a * delta_t
        self.z_v += self.z_a * delta_t

    def clear_acceleration(self) -> object:
        """Reset acceleration to zero."""
        self.x_a = 0.0
        self.y_a = 0.0
        self.z_a = 0.0

    def append_acceleration(self, dx_a: float, dy_a: float, dz_a: float) -> None:
        """Add acceleration components."""
        self.x_a += dx_a
        self.y_a += dy_a
        self.z_a += dz_a


def set_up_positions(x: list[list[float]], y: list[list[float]], z: list[list[float]], n: int) -> None:
    """Initialize position tracking lists."""
    i = 0
    while i < n:
        x.append([])
        y.append([])
        z.append([])
        i += 1


def append_positions(x: list[list[float]], y: list[list[float]], z: list[list[float]], planets: List[Planet]) -> None:
    """Record current positions of all planets."""
    n = len(planets)
    i = 0
    while i < n:
        p = planets[i]
        x[i].append(p.x)
        y[i].append(p.y)
        z[i].append(p.z)
        i += 1


def distance_between_planets(p_lhs: Planet, p_rhs: Planet) -> float:
    """Calculate the Euclidean distance between two planets."""
    return math.sqrt((p_lhs.x - p_rhs.x) ** 2.0 +
                     (p_lhs.y - p_rhs.y) ** 2.0 +
                     (p_lhs.z - p_rhs.z) ** 2.0)


def combine_planets(p_lhs: Planet, p_rhs: Planet) -> Planet:
    """Combine two planets into a new planet (collision)."""
    # new name
    new_name = p_lhs.name + p_rhs.name

    # new mass
    new_mass = p_lhs.mass + p_rhs.mass
    w_lhs = p_lhs.mass / new_mass
    w_rhs = 1.0 - w_lhs

    # new density and radius
    new_volume = p_lhs.volume() + p_rhs.volume()
    new_radius = (new_volume * (3.0 / 4.0) / math.pi) ** (1.0 / 3.0)

    # new position: we pick a point between the two centers,
    # giving more weight to bigger objects
    new_x = p_lhs.x * w_lhs + p_rhs.x * w_rhs
    new_y = p_lhs.y * w_lhs + p_rhs.y * w_rhs
    new_z = p_lhs.z * w_lhs + p_rhs.z * w_rhs

    # new velocity: conservation of momentum
    new_x_v = p_lhs.x_v * w_lhs + p_rhs.x_v * w_rhs
    new_y_v = p_lhs.y_v * w_lhs + p_rhs.y_v * w_rhs
    new_z_v = p_lhs.z_v * w_lhs + p_rhs.z_v * w_rhs

    # new acceleration: set it to zero, it will be computed in next iteration
    new_x_a = 0.0
    new_y_a = 0.0
    new_z_a = 0.0

    return Planet(new_name, new_radius, new_mass,
                  new_x, new_y, new_z,
                  new_x_v, new_y_v, new_z_v,
                  new_x_a, new_y_a, new_z_a)


def create_new_planet_list(i_lhs: int, i_rhs: int, new_planet: Planet, old_list: List[Planet]) -> List[Planet]:
    """Create a new planet list after a collision."""
    new_list = old_list
    if i_lhs < i_rhs:
        new_list.pop(i_rhs)
        new_list.pop(i_lhs)
    else:
        new_list.pop(i_lhs)
        new_list.pop(i_rhs)
    new_list.append(new_planet)
    return new_list


def check_for_colliding_planets(planets: List['Planet']) -> List['Planet']:
    """Check for colliding planets and combine them recursively."""
    n = len(planets)
    i_lhs = 0
    while i_lhs < n - 1:
        p_lhs = planets[i_lhs]
        i_rhs = i_lhs + 1
        while i_rhs < n:
            p_rhs = planets[i_rhs]
            larger_radius = max(p_lhs.radius, p_rhs.radius)
            distance = distance_between_planets(p_lhs, p_rhs)
            if distance < larger_radius:
                new_planet = combine_planets(p_lhs, p_rhs)
                new_planets = create_new_planet_list(i_lhs, i_rhs, new_planet, planets)
                return check_for_colliding_planets(new_planets)
            i_rhs += 1
        i_lhs += 1
    return planets


def report(planets: Planet, iteration: int, years: float) -> None:
    """Print current state of the planet."""
    print("After iteration ", iteration, " (", "%.6f" % years, " years):")
    for p in planets:
        print("   Planet ", p.name, ":")
        print("      * position:     ( %.2f, %.2f, %.2f)" % (p.x, p.y, p.z))
        print("      * velocity:     ( %.3f, %.3f, %.3f)" % (p.x_v, p.y_v, p.z_v))
        print("      * acceleration: ( %.4f, %.4f, %.4f)" % (p.x_a, p.y_a, p.z_a))


def ran() -> float:
    """Generate a random number between -1 and 1."""
    return -1.0 + 2.0 * np.random.random()


def random_sun(name: str) -> Planet:
    """Create a sun with random position and velocity."""
    return Planet(name,
                  R_sun,  # radius
                  M_sun,  # mass
                  ran() * D_earth_sun, ran() * D_earth_sun, ran() * D_earth_sun,  # position
                  ran() * V_earth, ran() * V_earth, ran() * V_earth)  # velocity


def static_sun(name: str) -> Planet:
    """Create a sun at the origin."""
    return Planet(name,
                  R_sun,  # radius
                  M_sun,  # mass
                  0.0, 0.0, 0.0,  # position
                  0.0, 0.0, 0.0)  # velocity


def real_earth(name: str) -> Planet:
    """Create a realistic Earth planet, at the current Sun-Earth distance,
    with realistic current tangential velocity."""
    return Planet(name, 
                  R_earth, # radius 
                  M_earth, # mass
                  D_earth_sun, 0.0, 0.0, # position 
                  0.0, V_earth, 0.0) # velocity


def random_earth(name: str) -> Planet:
    """Create an earth with random position and velocity."""
    return Planet(name,
                  R_earth,  # radius
                  M_earth,  # mass
                  ran() * D_earth_sun, ran() * D_earth_sun, ran() * D_earth_sun,  # position
                  ran() * V_earth, ran() * V_earth, ran() * V_earth)  # velocity


def static_earth(name: str) -> Planet:
    """Create an earth at the origin."""
    return Planet(name,
                  R_earth,  # radius
                  M_earth,  # mass
                  0.0, 0.0, 0.0,  # position
                  0.0, 0.0, 0.0)  # velocity
