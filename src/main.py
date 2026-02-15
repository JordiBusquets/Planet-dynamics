"""Main entry point for planet dynamics simulation."""

from src.models.planet import Planet, set_up_positions, append_positions
from src.physics.mechanics import compute_accelerations
from src.visualization.plots import set_up_plot, update_plot

import matplotlib.pyplot as plt

# Simulation parameters
TIME_HORIZON = 5.0  # in years
TIME_DELTA = 0.5    # in days
DAYS_TO_SEC = 24.0 * 60.0 * 60.0
DAYS_TO_YEARS = 1.0 / 365.25
DAYS_TO_SECONDS = 24.0 * 60.0 * 60.0

def planet_dynamics(planets: list[Planet], time_horizon:float, time_step:float, make_plot: bool=True, plot_update_freq: int=10):
    """
    Simulate planet dynamics over a given time horizon.
    
    Args:
        planets: the planets, with their initial positions and velocities, to simiulate
        time_horizon: Simulation time horizon in years
        step: Time step in days
        make_plot: Whether to display the 3D trajectory plot
        plot_update_freq: Update plot every N timesteps (default: 10)
        
    Returns:
        Tuple of (x, y, z) position lists for all planets
    """
    delta_in_sec = time_step * DAYS_TO_SEC

    x, y, z = [[]], [[]], [[]]
    set_up_positions(x, y, z, len(planets))
    lines = []
    
    if make_plot:
        set_up_plot(lines, x, y, z, planets)

    total_time = 0  # in years
    iteration = 0
    while total_time <= time_horizon:

        append_positions(x, y, z, planets)
        
        if make_plot and iteration % plot_update_freq == 0:
            update_plot(lines, x, y, z, planets, total_time)

        compute_accelerations(planets)
        for p in planets:
            p.update_velocity(delta_in_sec)
            p.update_position(delta_in_sec)

        # Uncomment to enable collision detection
        # planets = check_for_colliding_planets(planets)

        total_time += time_step * DAYS_TO_YEARS  # in years
        iteration += 1
    
    return x, y, z
