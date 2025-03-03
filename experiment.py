import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Receiver locations, we will divide the room into a grid, and place the receivers at the following coordinates
receivers = [
    {'center': (2, 2)},  # Receiver A
    {'center': (5, 8)},  # Receiver B
    {'center': (8, 2)}   # Receiver C
]

# The distances are the distance from the receiver to the point
# In format [distance from A, distance from B, distance from C] for a single point
distances = [
    [53, 59, 56],  # Distances from Point 1 to Receiver A, B, C
]

# Error function for optimization
def error_function(point, receivers, distances):
    x, y = point
    total_error = 0
    for i, receiver in enumerate(receivers):
        center_x, center_y = receiver['center']
        expected_distance = distances[i]  # Extract the expected distance for this receiver
        actual_distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        total_error += (actual_distance - expected_distance) ** 2
    return total_error

def calculate_points(distances, receivers):
    points = []
    for i in range(len(distances)):  # Loop through each point's distances (in this case, one point)
        initial_guess = (5, 5)  # Initial midpoint guess
        array = distances[i]  # Get distances for this point
        result = minimize(error_function, initial_guess, args=(receivers, array), method='L-BFGS-B')
        points.append(result.x)
    return points

calculated_points = calculate_points(distances, receivers)

def plot_points(receivers, distances, calculated_points):
    fig, ax = plt.subplots()

    for i, receiver in enumerate(receivers):
        center_x, center_y = receiver['center']
        plt.scatter(center_x, center_y, color='blue', label=f"Receiver ({center_x}, {center_y})", s=100)

        for j, distance_set in enumerate(distances):
            radius = distance_set[i]
            circle = plt.Circle((center_x, center_y), radius, color='blue', fill=False, linestyle='--', alpha=0.5,
                                label=f"Distance {radius:.2f} for Point {j+1}" if i == 0 else "")  # Avoid duplicate legend entries
            ax.add_artist(circle)

    for i, point in enumerate(calculated_points):
        plt.scatter(point[0], point[1], color='red', 
                    label=f"Point {i+1} ({point[0]:.2f}, {point[1]:.2f})", s=150)

    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
    plt.title("Triangulated Points with Receiver Circles")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.axis('equal')

    # Ensure the minimum axis values are 0
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.show()

plot_points(receivers, distances, calculated_points)
