import numpy as np
from scipy.optimize import curve_fit

def spiral_model(t, a, b):
    return a * t * np.cos(t), a * t * np.sin(t)

def calculate_trajectory_deviation(points):
    """
    Vypočíta odchýlku trajektórie od špirály.
    points: Zoznam dvojíc reprezentujúcich (x, y) súradnice bodov v trajektórii.
    """
    x_coords, y_coords = zip(*points)
    t_coords = np.linspace(0, 4 * np.pi, len(points))  # Predpokladáme, že body tvoria špirálu

    # Prispôsobí špirálový model bodom
    def wrapped_spiral_model(t, a, b):
        x, y = spiral_model(t, a, b)
        return np.concatenate((x, y))

    params, _ = curve_fit(wrapped_spiral_model, t_coords, np.concatenate((x_coords, y_coords)))
    a, b = params

    # Vypočíta odchýlku od prispôsobenej špirály
    fitted_x, fitted_y = spiral_model(t_coords, a, b)
    deviations = [np.sqrt((x - fx)**2 + (y - fy)**2) for (x, y), (fx, fy) in zip(points, zip(fitted_x, fitted_y))]

    return deviations

def calculate_speed_changes(points, times):
    #
     #Vypočíta zmeny rýchlosti na začiatku, v strede a na konci trajektórie. points: Zoznam dvojíc reprezentujúcich (x, y) súradnice bodov v trajektórii. times: Zoznam časových značiek zodpovedajúcich každému bodu v trajektórii.

    speeds = []
    
    for i in range(1, len(points)):
        distance = np.linalg.norm(np.array(points[i]) - np.array(points[i-1]))
        time_diff = times[i] - times[i-1]
        speed = distance / time_diff
        speeds.append(speed)
    
    # Vypočíta zmeny rýchlosti na začiatku, v strede a na konci
    speed_changes = {
        "začiatok": speeds[1] - speeds[0],
        "stred": speeds[len(speeds)//2 + 1] - speeds[len(speeds)//2],
        "koniec": speeds[-1] - speeds[-2]
    }
    
    return speed_changes

# Príklad použitia
trajectory_points = [(0, 0), (1, 2), (2, 4), (3, 6), (4, 8)]
time_stamps = [0, 1, 2, 3, 4]

trajectory_deviation = calculate_trajectory_deviation(trajectory_points)
speed_changes = calculate_speed_changes(trajectory_points, time_stamps)

print("Odchýlka trajektórie:", trajectory_deviation)
print("Zmeny rýchlosti:", speed_changes)