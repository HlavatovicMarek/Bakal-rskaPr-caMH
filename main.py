import numpy as np

def calculate_trajectory_deviation(points):
    """
    Vypočíta odchýlku trajektórie od priamky.
    points: Zoznam dvojíc reprezentujúcich (x, y) súradnice bodov v trajektórii.
    """
    # Prispôsobí priamku bodom
    x_coords, y_coords = zip(*points)
    coefficients = np.polyfit(x_coords, y_coords, 1)
    polynomial = np.poly1d(coefficients)
    
    # Vypočíta odchýlku od prispôsobenej priamky
    deviations = [abs(polynomial(x) - y) for x, y in points]
    
    return deviations

def calculate_speed_changes(points, times):
    """
    Vypočíta zmeny rýchlosti na začiatku, v strede a na konci trajektórie.
    points: Zoznam dvojíc reprezentujúcich (x, y) súradnice bodov v trajektórii.
    times: Zoznam časových značiek zodpovedajúcich každému bodu v trajektórii.
    """
    speeds = []
    
    for i in range(1, len(points)):
        distance = np.linalg.norm(np.array(points[i]) - np.array(points[i-1]))
        time_diff = times[i] - times[i-1]
        speed = distance / time_diff
        speeds.append(speed)
    
    # Vypočíta zmeny rýchlosti na začiatku, v strede a na konci tuto musím konkrétne zadať ako chvem ú
    speed_changes = {
        "beginning": speeds[1] - speeds[0],
        "middle": speeds[len(speeds)//2 + 1] - speeds[len(speeds)//2],
        "end": speeds[-1] - speeds[-2]
    }
    
    return speed_changes

# Príklad použitia
trajectory_points = [(0, 0), (1, 2), (2, 4), (3, 6), (4, 8)]
time_stamps = [0, 1, 2, 3, 4]

trajectory_deviation = calculate_trajectory_deviation(trajectory_points)
speed_changes = calculate_speed_changes(trajectory_points, time_stamps)

print("Odchýlka trajektórie:", trajectory_deviation)
print("Zmeny rýchlosti:", speed_changes)