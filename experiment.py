import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


# Receiver locations, we will divise the room into a grid, and place the recievers at the following coordinates
receivers = [
    {'center': (2, 2)},   # Receiver A
    {'center': (5, 8)},  # Receiver B
    {'center': (8, 2)}   # Receiver C
]

# Dummy values for the distances, we will use the RSSI values to calculate the distances
# The distances are the distance from the receiver to the point
# In format [distance from A, distance from B, distance from C]
distances = [
    [2.5, 9.3, 8.1],
    [2.3, 8.5, 8.2],
    [1, 6.8, 6]
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

    for i, receiver in enumerate(receivers):
        center_x, center_y = receiver['center']
        plt.scatter(center_x, center_y, color='blue', label=f"Receiver ({center_x}, {center_y})", s=100)

        for j, distance_set in enumerate(distances):
            radius = distance_set[i]
            circle = plt.Circle((center_x, center_y), radius, color='blue', fill=False, linestyle='--', alpha=0.5,
                                label=f"Distance {radius} for Point {j+1}" if i == 0 else "")  # Avoid duplicate legend entries
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