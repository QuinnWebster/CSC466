import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.interpolate import CubicSpline


PATH_LOSS = 2.9  # Higher value for more noisy room


def rssi_to_distance(rssi, rssi_unit):
    rssi_ref = rssi_unit  # RSSI_UNIT
    path_loss = PATH_LOSS
    return 10 ** ((rssi_ref - rssi) / (10 * path_loss))


# Error function for optimization
def error_function(point, receivers, distances):
    x, y = point
    total_error = 0
    for i, receiver in enumerate(receivers):
        center_x, center_y = receiver["center"]
        expected_distance = distances[i]
        actual_distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        total_error += (actual_distance - expected_distance) ** 2
    return total_error


def error_function_L1(point, receivers, distances):
    x, y = point
    total_error = 0
    for i, receiver in enumerate(receivers):
        center_x, center_y = receiver["center"]
        expected_distance = distances[i]
        actual_distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        total_error += np.abs(actual_distance - expected_distance)
    return total_error


def error_function_huber(point, receivers, distances, delta=1.0):
    x, y = point
    total_error = 0
    for i, receiver in enumerate(receivers):
        center_x, center_y = receiver["center"]
        expected_distance = distances[i]
        actual_distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        error = np.abs(actual_distance - expected_distance)
        if error <= delta:
            total_error += 0.5 * error**2
        else:
            total_error += delta * (error - 0.5 * delta)
    return total_error


def calculate_points(distances, receivers):
    points = []
    for i in range(len(distances)):
        initial_guess = (5, 5)  # Initial midpoint guess
        array = distances[i]  # Get distances for this point
        result = minimize(
            error_function, initial_guess, args=(receivers, array), method="L-BFGS-B"
        )
        # result = minimize(error_function_huber, initial_guess, args=(receivers, array), method='L-BFGS-B')
        points.append(result.x)
    return points


# Adds more points to the path
def smooth_path(calculated_points, num_points=100):
    # Convert the list of calculated points to separate X and Y coordinates
    x_vals = [point[0] for point in calculated_points]
    y_vals = [point[1] for point in calculated_points]

    # Create a cubic spline interpolator
    spline_x = CubicSpline(range(len(calculated_points)), x_vals)
    spline_y = CubicSpline(range(len(calculated_points)), y_vals)

    # Generate new smooth points
    smooth_x = np.linspace(0, len(calculated_points) - 1, num_points)
    smooth_y = np.linspace(0, len(calculated_points) - 1, num_points)

    # Get the smooth coordinates from the spline functions
    smooth_x_vals = spline_x(smooth_x)
    smooth_y_vals = spline_y(smooth_y)

    return list(zip(smooth_x_vals, smooth_y_vals))


# Plotting the receivers and calculated points
def plot_receivers_and_points(receivers, calculated_points, expected_path):
    plt.figure(figsize=(8, 8))

    # Plot receivers as red points
    for receiver in receivers:
        plt.plot(receiver["center"][0], receiver["center"][1], "ro", label="Receiver")

    # Plot calculated points as blue 'x'
    for point in calculated_points:
        plt.plot(point[0], point[1], "bx", label="Calculated Point")

    # Plot the expected path as a red dashed line
    expected_x, expected_y = zip(
        *expected_path
    )  # Unzip the path into x and y coordinates
    plt.plot(expected_x, expected_y, "r--", label="Expected Path")

    # Labels and title
    plt.title("Receiver Locations, Calculated Points, and Expected Path")
    plt.xlabel("X Coordinates")
    plt.ylabel("Y Coordinates")

    # Display the grid and the legend
    plt.grid(True)

    plt.show()


def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))


# Compute the errors
def compute_errors(calculated_points, expected_path):
    if len(calculated_points) != len(expected_path):
        raise ValueError(
            "The number of calculated points and expected points must be the same."
        )

    squared_errors = []
    for c_point, e_point in zip(calculated_points, expected_path):
        squared_error = euclidean_distance(c_point, np.array(e_point)) ** 2
        squared_errors.append(squared_error)

    # Sum of squared errors
    sse = sum(squared_errors)

    # Root mean square error (RMSE)
    rmse = np.sqrt(sse / len(calculated_points))

    return sse, rmse


def main():
    # Receiver locations, we will divide the room into a grid, and place the receivers at the following coordinates
    receivers = [
        {"center": (6, 9)},  # Receiver A
        {"center": (0, 0)},  # Receiver B
        {"center": (12, 0)},  # Receiver C
    ]

    # In format [distance from A, distance from B, distance from C] for a single point
    # distances = [
    #     [53, 59, 56],  # Distances from Point 1 to Receiver A, B, C
    #     [50, 56, 53],  # Distances from Point 2 to Receiver A, B, C
    # ]

    UNIT_RSSI_A = -58  # Tune this value to rssi value at one unit distance
    UNIT_RSSI_B = -58
    UNIT_RSSI_C = -58

    # Distances from the receivers to the tracked points
    # truman
    distances_a = [
        -84.0,
        -82.0,
        -88.0,
        -79.0,
        -77.0,
        -76,
        -75.0,
        -77,
        -78.0,
        -87.0,
        -80.5,
        -75.25,
        -84.5,
        -83.0,
        -81,
        -80.66666666666667,
        -84.0,
        -86,
        -88.0,
        -87.5,
        -82.0,
        -86.0,
        -83.5,
        -77.5,
        -82.5,
        -87.0,
        -84.0,
        -81.5,
        -78.0,
        -82.66666666666667,
        -87.0,
        -89.5,
        -92,
        -95.0,
        -93.0,
        -96.0,
        -96.0,
        -96.0,
        -96.0,
        -96.0,
    ]
    # jack
    distances_b = [
        -77.6,
        -79.0,
        -71.0,
        -70.0,
        -75.0,
        -80.33333333333333,
        -79.0,
        -75.75,
        -75.0,
        -75.0,
        -76.6,
        -77.0,
        -80.0,
        -82.0,
        -88.5,
        -85.5,
        -90.0,
        -92.0,
        -89.33333333333333,
        -95.0,
        -95.0,
        -91.0,
        -91.0,
        -92.5,
        -93.0,
        -92.5,
        -92.0,
        -92.0,
        -97.0,
        -97.0,
        -97.0,
        -97.0,
        -90.0,
        -85.5,
        -84.0,
        -91.33333333333333,
        -84.0,
        -81.0,
        -85,
        -88.0,
    ]
    # quinn
    distances_c = [
        -90.0,
        -93.5,
        -91,
        -90.5,
        -81.66666666666667,
        -89.33333333333333,
        -75.66666666666667,
        -77.25,
        -78.5,
        -78.33333333333333,
        -81.0,
        -82.5,
        -83.4,
        -82.5,
        -78.66666666666667,
        -79.8,
        -84.0,
        -88.0,
        -85.0,
        -85.0,
        -83.0,
        -88.0,
        -93.0,
        -89.0,
        -93.66666666666667,
        -87.66666666666667,
        -85.0,
        -87.25,
        -85.0,
        -85.33333333333333,
        -85.0,
        -88.33333333333333,
        -92.4,
        -94.5,
        -92,
        -90.5,
        -91.33333333333333,
        -93.33333333333333,
        -92,
        -91.0,
    ]
    # expected_path = [ (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,6.5), (5,7), (4.5,7), (4,7), (3,7), (2,7), (1, 7), (0,7) ]

    expected_path = [
        (5, 0),
        (5, 0.5),
        (5, 1),
        (5, 1.5),
        (5, 2),
        (5, 2.5),
        (5, 3),
        (5, 3.5),
        (5, 4),
        (5, 4.5),
        (5, 5),
        (5, 5.5),
        (5, 6),
        (5, 7),
        (4.5, 7),
        (4, 7),
        (3, 7),
        (2, 7),
        (1, 7),
        (0, 7),
    ]

    if len(distances_a) != len(distances_b) or len(distances_a) != len(distances_c):
        raise ValueError("The number of distances for each receiver must be the same.")

    # list of three distance points. i.e. [[a1, b1, c1], [a2, b2, c2], ...]

    distances_a = [rssi_to_distance(distance, UNIT_RSSI_A) for distance in distances_a]

    distances_b = [rssi_to_distance(distance, UNIT_RSSI_B) for distance in distances_b]

    distances_c = [rssi_to_distance(distance, UNIT_RSSI_C) for distance in distances_c]

    triangulation_points = [
        list(values) for values in zip(distances_a, distances_b, distances_c)
    ]

    calculated_points = calculate_points(triangulation_points, receivers)

    # Smooth the path using cubic spline interpolation
    # smoothed_points = smooth_path(calculated_points)
    smoothed_points = calculated_points

    # Call the plotting function with calculated points
    plot_receivers_and_points(receivers, smoothed_points, expected_path)

    # Compute errors
    sse, rmse = compute_errors(calculated_points, expected_path)

    # Print the results
    print("Root Mean Square Error (RMSE):", rmse)


if __name__ == "__main__":
    main()
