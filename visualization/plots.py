"""Visualization tools for planet dynamics simulation."""
import time
import matplotlib.pyplot as plt
from constants import R_earth

colors = ['g-', 'r-', 'b-', 'y-', 'g-', 'b-']


def compute_limit(planets, dim, current_lim_min=0.0, current_lim_plus=0.0):
    """Compute axis limits based on planet positions."""
    n = len(planets)
    i = 0
    lim_plus = current_lim_plus
    lim_min = current_lim_min
    while i < n:
        p = planets[i]
        if dim == 1:
            if p.x > 0.0:
                lim_plus = max(lim_plus, p.x)
            else:
                lim_min = min(lim_min, p.x)
        elif dim == 2:
            if p.y > 0.0:
                lim_plus = max(lim_plus, p.y)
            else:
                lim_min = min(lim_min, p.y)
        elif dim == 3:
            if p.z > 0.0:
                lim_plus = max(lim_plus, p.z)
            else:
                lim_min = min(lim_min, p.z)
        i += 1
    return (min(lim_min, -R_earth), max(lim_plus, R_earth))


def set_up_plot(lines, x, y, z, planets):
    """Initialize the 3D plot for planet trajectories."""
    n = len(planets)
    lim_x_min, lim_x_plus = compute_limit(planets, 1)
    lim_y_min, lim_y_plus = compute_limit(planets, 2)
    lim_z_min, lim_z_plus = compute_limit(planets, 3)

    fig = plt.figure()
    fig.add_subplot(1, 1, 1, projection='3d')
    plt.ion()
    plt.show()
    axes = plt.gca(projection='3d')
    axes.set_xlim(lim_x_min, lim_x_plus)
    axes.set_ylim(lim_y_min, lim_y_plus)
    axes.set_zlim(lim_z_min, lim_z_plus)

    plt.title("T=0 years")
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.set_zlabel("z")

    i = 0
    while i < n:
        line, = axes.plot(x[i], y[i], z[i], colors[i])
        lines.append(line)
        i += 1


def update_plot(lines, x, y, z, planets, t):
    """Update the plot with new planet positions."""
    n = len(lines)
    i = 0
    while i < len(planets):
        lines[i].set_xdata(x[i])
        lines[i].set_ydata(y[i])
        lines[i].set_3d_properties(z[i])
        i += 1

    axes = plt.gca(projection='3d')
    current_lim_x = axes.get_xlim()  # returns 2-tuple
    current_lim_y = axes.get_ylim()  # returns 2-tuple
    current_lim_z = axes.get_zlim()  # returns 2-tuple
    lim_x_min, lim_x_plus = compute_limit(planets, 1, current_lim_x[0], current_lim_x[1])
    lim_y_min, lim_y_plus = compute_limit(planets, 2, current_lim_y[0], current_lim_y[1])
    lim_z_min, lim_z_plus = compute_limit(planets, 3, current_lim_z[0], current_lim_z[1])
    axes.set_xlim(lim_x_min, lim_x_plus)
    axes.set_ylim(lim_y_min, lim_y_plus)
    axes.set_zlim(lim_z_min, lim_z_plus)

    new_title = "T=" + str("%.2f" % t) + " years"
    plt.title(new_title)

    plt.draw()
    plt.pause(1e-17)
    time.sleep(0.001)
