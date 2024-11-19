import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

image_path = 'thumbnail_plantilla_CapturaDraw.png' 
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# pre detekciu tvarov 
_, threshold = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

# Detekcia kontúr
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Najdenie najvacsej kontury-spiraly
spiral_contour = max(contours, key=cv2.contourArea)

x, y, w, h = cv2.boundingRect(spiral_contour)


spiral_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.rectangle(spiral_image, (x, y), (x + w, y + h), (255, 255, 255), 2)

plt.imshow(spiral_image)
plt.title("Detekovaná špirála")
plt.show()

center_x, center_y = x + w // 2, y + h // 2
print(f"Stred špirály: ({center_x}, {center_y})")
print(f"Rozmery špirály: šírka = {w}, výška = {h}")


data_path = 'data.csv' 
data = pd.read_csv(data_path)

points = data[['X', 'Y']].to_numpy()

points[:, 1] = image.shape[0] - points[:, 1]  

def spiral_function(theta, a, b):
    return a + b * theta

# Parametry spirály (přizpůsobte podle analýzy obrázku)
a = 20  # Počáteční vzdálenost od středu
b = 10  # Rozestup mezi závity

# Kontrola bodů
for point in points:
    px, py = point
    dx, dy = px - center_x, py - center_y
    r = np.sqrt(dx**2 + dy**2)
    theta = np.arctan2(dy, dx)

    # Ověření, či bod odpovídá špirále
    expected_r = spiral_function(theta, a, b)
    deviation = abs(r - expected_r)

    print(f"Bod: ({px}, {py}), Odchylka: {deviation:.2f}")
