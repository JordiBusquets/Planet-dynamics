from planet import planet, check_for_colliding_planets, append_positions, set_up_positions, \
    random_sun, random_earth, static_sun, static_earth, M_sun, R_sun, V_earth, D_earth_sun, M_earth
from physics import compute_accelerations, stable_circular_orbit_earth
from plots import set_up_plot, update_plot
from constants import D_earth_sun, D_earth_moon

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

time_horizon = 5.0  # in years
time_delta = 0.5  # in days
days_to_sec = 24.0 * 60.0 * 60.0
days_to_years = 1.0 / 365.25


# Horizon is on years, step is in days
def planet_dynamics(horizon, step, make_plot=True):
    delta_in_sec = step * days_to_sec

    # define your planets here
    planets = [static_sun("1"),
               planet("2", R_sun, M_earth, D_earth_sun, 0.0, 0.0, 0.0, V_earth, 0.0)]

    x, y, z = [[]], [[]], [[]]
    set_up_positions(x, y, z, len(planets))
    lines = []
    if make_plot:
        set_up_plot(lines, x, y, z, planets)

    total_time = 0  # in years
    while total_time <= horizon:

        print("Time (in y): ", total_time, " --- Number of planets: ", len(planets))

        for p in planets:
            p.report()
        append_positions(x, y, z, planets)
        if make_plot:
            update_plot(lines, x, y, z, planets, total_time)

        compute_accelerations(planets)
        for p in planets:
            p.update_velocity(delta_in_sec)
            p.update_position(delta_in_sec)

        # planets = check_for_colliding_planets(planets)

        total_time += step * days_to_years  # in years

    if make_plot:
        plt.show()
    return x, y, z


if __name__ == '__main__':
    planet_dynamics(time_horizon, time_delta)

