import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Receiver locations and their estimated distances 
receivers = [
    {'center': (1, 1), 'radius': 5},  # Receiver A
    {'center': (10, 1), 'radius': 7},  # Receiver B
    {'center': (5, 10), 'radius': 5}   # Receiver C
]

def error_function(point, receivers):
    """Calculate the total error between the point and all receivers."""
    x, y = point
    total_error = 0
    for receiver in receivers:
        center_x, center_y = receiver['center']
        radius = receiver['radius']
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        total_error += (distance - radius)**2
    return total_error

# Initial guess for the point
initial_guess = (2, 2)

# Minimize the error function to find the best-fit point
result = minimize(error_function, initial_guess, args=(receivers,), method='L-BFGS-B')
best_fit_point = result.x

print(f"Best-fit point (x, y): {best_fit_point}")

# Plottting
def plot_approximation(receivers, best_fit_point):
    fig, ax = plt.subplots()
    for receiver in receivers:
        center_x, center_y = receiver['center']
        radius = receiver['radius']
        circle = plt.Circle((center_x, center_y), radius, fill=False, label=f"Receiver at ({center_x}, {center_y})")
        ax.add_artist(circle)
        plt.scatter(center_x, center_y, label=f"Center ({center_x}, {center_y})", s=100)
    
    # Mark the best-fit point
    plt.scatter(*best_fit_point, color='red', label=f"Best-Fit Point {tuple(best_fit_point)}", s=150)
    ax.set_xlim(-10, 20)
    ax.set_ylim(-10, 20)
    # Plot settings
    ax.set_aspect('equal', adjustable='datalim')
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')

    plt.title("Bluetooth Triangulation with Approximation")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()

plot_approximation(receivers, best_fit_point)
