import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Receiver locations
receivers = [
    {'center': (1, 1)},   # Receiver A
    {'center': (10, 1)},  # Receiver B
    {'center': (5, 10)}   # Receiver C
]

# Array of distances for multiple points
distances = [
    [6, 10, 3.5],
    [5,9,4.5],
    [4,8,5.5],
    [5, 7, 5],
    [6, 6, 4.5],
    [7, 5, 5]
]

# Error function for optimization
def error_function(point, receivers, distances):
    x, y = point
    total_error = 0
    for i, receiver in enumerate(receivers):
        center_x, center_y = receiver['center']
        expected_distance = distances[i]
        actual_distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        total_error += (actual_distance - expected_distance)**2
    return total_error

def calculate_points(distances, receivers):
    points = []
    for distance_set in distances:
        initial_guess = (5, 5)  # Some midpoint in the graph
        result = minimize(error_function, initial_guess, args=(receivers, distance_set), method='L-BFGS-B')
        points.append(result.x)
    return points

calculated_points = calculate_points(distances, receivers)

def plot_points(receivers, distances, calculated_points):
    fig, ax = plt.subplots()

    # Plot receivers and their distance circles
    for i, receiver in enumerate(receivers):
        center_x, center_y = receiver['center']
        plt.scatter(center_x, center_y, color='blue', label=f"Receiver ({center_x}, {center_y})", s=100)
        
        # Plot circles for each distance
        for j, distance_set in enumerate(distances):
            radius = distance_set[i]
            circle = plt.Circle((center_x, center_y), radius, color='blue', fill=False, linestyle='--', alpha=0.5,
                                label=f"Distance {radius} for Point {j+1}" if i == 0 else "")  # Avoid duplicate legend entries
            ax.add_artist(circle)

    # Plot calculated points
    for i, point in enumerate(calculated_points):
        plt.scatter(point[0], point[1], color='red', label=f"Point {i+1} ({point[0]:.2f}, {point[1]:.2f})", s=150)

    # Customize the plot
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.title("Triangulated Points with Receiver Circles")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Legend outside
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# Plot results
plot_points(receivers, distances, calculated_points)
