# Planet Dynamics Simulation

A Python-based N-body gravitational dynamics simulator that models the orbital mechanics and interactions of multiple celestial bodies in 3D space.

## Features

- **N-Body Simulation** - Simulate gravitational interactions between multiple planets simultaneously
- **Realistic Physics** - Uses Newton's law of universal gravitation to compute forces and accelerations
- **Real Constants** - Incorporates actual physical constants and measurements (Earth mass, solar mass, AU distances, etc.)
- **3D Visualization** - Interactive 3D trajectory plotting using matplotlib
- **Collision Detection** - Automatically handles planet collisions with momentum conservation
- **Flexible Configuration** - Easily define custom planets with arbitrary masses, positions, and velocities

## Physics

The simulator uses Newtonian mechanics to model gravitational interactions:

### Gravitational Force
$$F = G \frac{m_1 m_2}{d^2}$$

Where:
- $G = 6.674 \times 10^{-11}$ m³/(kg·s²) (gravitational constant)
- $m_1$, $m_2$ are the masses of two bodies
- $d$ is the distance between them

### Particle Integration
Positions and velocities are updated using forward Euler integration:

$$v(t + \Delta t) = v(t) + a(t) \Delta t$$
$$x(t + \Delta t) = x(t) + v(t) \Delta t$$

### Collision Handling
When two planets collide (distance < max radius), they merge into a single body with:
- Combined mass
- Weighted average position (weighted by mass)
- Momentum-conserved velocity
- Merged volume determines new radius

## Installation

### Requirements
- Python 3.7+
- NumPy
- Matplotlib
- Jupyter (optional, for notebook examples)

### Setup

```bash
git clone https://github.com/JordiBusquets/Planet-dynamics.git
cd Planet-dynamics
pip install numpy matplotlib jupyter
```

## Usage

### Quick Start

Run the default simulation (Sun + Earth over 5 years):

```bash
# Running as a module
python -m src.main
```

This will display a 3D animation of Earth's orbit around the Sun.

Alternatively, open `scripts/Planets.ipynb` in Jupyter for an interactive experience.

### Custom Simulations

```python
from src.main import planet_dynamics

# Run for 10 years with 1-day time steps, including visualization
x, y, z = planet_dynamics(horizon=10.0, step=1.0, make_plot=True)

# Run without visualization for faster computation
x, y, z = planet_dynamics(horizon=100.0, step=1.0, make_plot=False)
```

### Creating Custom Planetary Systems

```python
from src.models.planet import Planet, static_sun, static_earth
from src.physics.mechanics import compute_accelerations
from src.constants import D_earth_sun, V_earth, M_earth, R_sun

# Define planets with custom properties
planets = [
    static_sun("Sun"),
    Planet(
        name="Earth",
        radius=R_sun,           # Actual sun radius
        mass=M_earth,           # Actual earth mass
        x=D_earth_sun,          # Earth-Sun distance (1 AU)
        y=0.0, z=0.0,           # Position
        x_v=0.0,
        y_v=V_earth,            # Orbital velocity
        z_v=0.0
    )
]

# Run simulation loop
for step in range(1000):
    compute_accelerations(planets)
    delta_t = 86400  # 1 day in seconds
    
    for p in planets:
        p.update_velocity(delta_t)
        p.update_position(delta_t)
        p.report()  # Print position/velocity/acceleration
```

## Project Structure

```
Planet-dynamics/
├── src/                       # Source code package
│   ├── __init__.py
│   ├── main.py               # Entry point
│   ├── constants.py          # Physical constants
│   ├── models/
│   │   ├── __init__.py
│   │   └── planet.py         # Planet class and factory functions
│   ├── physics/
│   │   ├── __init__.py
│   │   └── mechanics.py      # Gravitational calculations
│   └── visualization/
│       ├── __init__.py
│       └── plots.py          # 3D trajectory plotting
├── scripts/                   # Example scripts and notebooks
│   └── Planets.ipynb         # Interactive Jupyter notebook
├── tests/                     # Unit tests
│   └── __init__.py
└── README.md                 # Project documentation
```

## Physical Constants Used

| Constant | Value | Unit |
|----------|-------|------|
| Earth Mass | 5.972 × 10²⁴ | kg |
| Sun Mass | 1.989 × 10³⁰ | kg |
| Earth Radius | 6.371 × 10⁶ | m |
| Sun Radius | 6.9551 × 10⁸ | m |
| Earth-Sun Distance (1 AU) | 1.4714 × 10¹¹ | m |
| Earth-Moon Distance | 3.844 × 10⁸ | m |
| Earth Orbital Velocity | 30,000 | m/s |
| Gravitational Constant (G) | 6.67408 × 10⁻¹¹ | m³/(kg·s²) |

## Example Scenarios

### Stable Earth Orbit
```python
from main import planet_dynamics

# Simulate Earth orbiting the Sun for 5 years
x, y, z = planet_dynamics(horizon=5.0, step=0.5, make_plot=True)
```

### Multi-Body System
```python
from models import Planet, static_sun, static_earth, random_earth

planets = [
    static_sun("Sun"),
    static_earth("Earth"),
    random_earth("Rogue Planet")  # Random position/velocity
]

# Simulate interactions between all three
```

## Visualization

The simulator produces 3D trajectory plots showing:
- **Green lines** - First planet's path
- **Red lines** - Second planet's path  
- **Blue lines** - Additional planets
- **Dynamic scaling** - Axes adjust automatically as planets move

The plot updates in real-time during simulation with current time displayed.

## Testing

The project includes comprehensive unit and functional tests for all major components. Tests are organized into:
- **Unit Tests** (`tests/unit/`) - Test individual classes and functions
- **Functional Tests** (`tests/functional/`) - Integration and end-to-end tests

### Installation

Install pytest and related tools:

```bash
pip install pytest pytest-cov
```

### Running Tests

#### Using pytest (recommended):

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run only functional tests
pytest tests/functional/

# Run specific test file
pytest tests/unit/test_constants.py

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src tests/

# Run with detailed coverage report
pytest --cov=src --cov-report=html tests/
```

#### Using unittest directly:

```bash
# Run all tests
python3 -m unittest discover tests

# Run specific test module
python3 -m unittest tests.unit.test_constants

# Run with verbose output
python3 -m unittest discover tests -v
```

### Test Structure

```
tests/
├── unit/                      # Unit tests
│   ├── test_constants.py      # Tests for physical constants
│   ├── models/
│   │   └── test_planet.py     # Tests for Planet class
│   ├── physics/
│   │   └── test_mechanics.py  # Tests for physics calculations
│   └── visualization/
│       └── test_plots.py      # Tests for plotting functions
└── functional/                # Functional/integration tests
    └── test_main.py           # Tests for main simulation function
```

## Limitations & Improvements

- **Euler Integration** - Forward Euler method has limited stability. Consider RK4 for higher accuracy
- **N-Body Performance** - O(n²) complexity; slow for >100 bodies
- **Relativistic Effects** - Ignores general relativity (fine for solar system scales)
- **Collision Handling** - Perfect inelastic collisions only

## Future Enhancements

- Implement higher-order integration schemes (RK4, Verlet)
- Add performance optimizations (spatial partitioning, GPU acceleration)
- Include asteroid belts and ring systems
- Add orbital parameter calculations (eccentricity, inclination)
- Web-based interactive visualization
- Support for barycenters and binary star systems

## License

MIT License

## Author

Jordi Busquets

## References

- Newton's Law of Universal Gravitation: _Principia Mathematica_ (Isaac Newton, 1687)
- N-Body Simulation Techniques: Aarseth, S. J. (2003). _Gravitational N-Body Simulations_
- Numerical Integration Methods: Press, W. H., et al. (2007). _Numerical Recipes_
