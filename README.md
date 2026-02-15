# Planet-dynamics

A Python-based N-body gravitational dynamics simulator for modeling the orbital and collision behavior of planets and celestial bodies.

## Overview

This project simulates the dynamics of multiple planets interacting under the influence of gravity. It implements Newton's laws of gravitation to compute forces, accelerations, and trajectories in 3D space. The simulator includes collision detection and realistic merging of colliding bodies, allowing you to explore complex multi-body gravitational systems.

## Features

- **N-Body Gravitational Simulation**: Accurate computation of gravitational forces and accelerations between multiple planets
- **3D Trajectory Visualization**: Real-time or post-simulation visualization of planetary orbits in 3D space
- **Collision Detection & Merging**: Automatically detects planet collisions and merges them conserving mass and momentum
- **Customizable Planets**: Define planets with arbitrary mass, radius, position, and velocity
- **Predefined Bodies**: Convenience functions for creating Earth and Sun with realistic parameters
- **Multiple Interface Options**: Use either pure Python scripts (faster) or Jupyter notebooks (interactive)
- **Real Physical Constants**: Built-in astronomical data for Earth, Sun, Moon, and gravitational constant

## How It Works

The simulation uses a time-stepping numerical integration approach:

1. **Force Calculation**: Computes gravitational force between each pair of planets using Newton's law of universal gravitation:
   - $F = G \frac{m_1 m_2}{r^2}$

2. **Acceleration Computation**: Converts forces to accelerations for each planet based on their mass

3. **Position/Velocity Updates**: Updates positions and velocities using the computed accelerations over discrete time steps

4. **Collision Handling**: Detects when planets collide and merges them, conserving total mass and momentum

5. **Visualization**: Tracks and displays the 3D trajectory of each planet throughout the simulation

## Project Structure

```
Planet-dynamics/
├── constants.py          # Physical constants (Earth/Sun parameters, G)
├── planet.py             # Planet class and helper functions
├── physics.py            # Gravitational physics calculations
├── plots.py              # 3D visualization utilities
├── init.py               # Main simulation loop and setup
├── Planets.ipynb         # Jupyter notebook interface
├── README.md             # This file
```

### Module Details

**`planet.py`**
- `planet` class: Represents a celestial body with position, velocity, acceleration, mass, and radius
- Utility functions for creating Earth/Sun planets (random or static)
- Collision detection and planet merging logic
- Position/velocity/acceleration update methods

**`physics.py`**
- `gravitational_force()`: Computes the gravitational force between two planets
- `gravitational_acceleration()`: Converts force to acceleration
- `compute_accelerations()`: Updates acceleration for all planets in the system
- `stable_circular_orbit_earth()`: Helper for calculating stable orbits

**`plots.py`**
- 3D visualization setup and updates
- Dynamic plot rendering with matplotlib
- Automatic axis scaling based on planet positions

**`init.py`**
- `planet_dynamics()`: Main simulation function
- Time stepping and integration loop
- Collision checking and planet merging

**`constants.py`**
- Physical constants in SI units:
  - Earth mass ($M_{\text{Earth}}$): $5.972 \times 10^{24}$ kg
  - Sun mass ($M_{\text{Sun}}$): $1.989 \times 10^{30}$ kg
  - Gravitational constant ($G$): $6.67408 \times 10^{-11}$ m³/(kg·s²)
  - And more...

## Usage

### Running Pure Python Version

The primary simulation is defined in `init.py`. To run a simulation:

```python
from init import planet_dynamics

# Run for 5 years with 0.5-day time steps, with visualization
planet_dynamics(horizon=5.0, step=0.5, make_plot=True)
```

### Creating Custom Planets

You can define custom planets in the `planet_dynamics()` function:

```python
from planet import planet
from constants import M_sun, R_sun, M_earth, R_earth, D_earth_sun, V_earth

# Create a custom planet
custom_planet = planet(
    name="Custom",
    radius=1e7,              # meters
    mass=1e25,               # kg
    x=1.5e11,                # meters (x position)
    y=0.0,                   # meters (y position)
    z=0.0,                   # meters (z position)
    x_v=0.0,                 # m/s (x velocity)
    y_v=25000.0,             # m/s (y velocity)
    z_v=0.0                  # m/s (z velocity)
)
```

### Using Jupyter Notebook

Open `Planets.ipynb` for an interactive version of the simulator. The notebook:
- Allows toggling between dynamic (live animation) and static (final plot only) modes
- Provides an interactive visualization environment
- Enables step-by-step exploration of the code

## Parameters

The `planet_dynamics()` function accepts:
- `horizon` (float): Simulation duration in years (default: 5.0)
- `step` (float): Time step in days (default: 0.5)
- `make_plot` (bool): Enable visualization (default: True)

Smaller time steps provide more accuracy but slower execution. Larger horizons show longer-term orbital evolution.

## Physical Constants Reference

All constants are in SI units (meters, kilograms, seconds):

| Constant | Value | Unit |
|----------|-------|------|
| Earth Mass | 5.972 × 10²⁴ | kg |
| Earth Radius | 6.371 × 10⁶ | m |
| Sun Mass | 1.989 × 10³⁰ | kg |
| Sun Radius | 6.9551 × 10⁸ | m |
| Earth-Sun Distance | 1.4714 × 10¹¹ | m |
| Earth-Moon Distance | 3.844 × 10⁸ | m |
| Earth Orbital Velocity | 30,000 | m/s |
| Gravitational Constant G | 6.67408 × 10⁻¹¹ | m³/(kg·s²) |

## Example Simulations

### Static Sun with Orbiting Earth
```python
from planet import planet, static_sun
from constants import M_earth, R_earth, D_earth_sun, V_earth
from init import planet_dynamics

# Configure in init.py:
planets = [
    static_sun("Sun"),
    planet("Earth", R_earth, M_earth, D_earth_sun, 0.0, 0.0, 0.0, V_earth, 0.0)
]
```

### Multiple Bodies with Collisions
The simulator automatically detects and processes collisions, merging bodies while conserving:
- Total mass (sum of colliding bodies' masses)
- Momentum (weighted by mass)
- Radius (computed from combined volume)

## Technical Notes

- **Numerical Integration**: Uses simple Euler integration with fixed time steps
- **Collision Detection**: Checks if distance between planet surfaces is less than the larger radius
- **Coordinate System**: Cartesian 3D coordinates (x, y, z)
- **Performance**: Pure Python version is faster; Jupyter notebook is interactive but slower due to rendering

## Requirements

- Python 3.6+
- matplotlib (for visualization)
- numpy (for numerical computations)
- jupyter (for notebook interface, optional)

## Installation

```bash
# Clone the repository
git clone https://github.com/JordiBusquets/Planet-dynamics.git
cd Planet-dynamics

# Install dependencies
pip install matplotlib numpy jupyter
```

## Future Enhancements

- Variable time-stepping for improved accuracy
- Different integration methods (RK4, Verlet, etc.)
- Performance optimization for larger N-body systems
- Relativistic gravity correction for high-velocity scenarios
- Export simulation results to file formats

## License

[Add your license here]

## Author

[Jordi] 
