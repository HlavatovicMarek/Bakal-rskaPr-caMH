import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance
import cv2

def extract_spiral_coords(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f'ObrázOk {image_path} se nepodarilo načtat.')
        return None

    # Detekcia hran + bin
    _, threshold = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("Kontury neboli najdene.")
        return None

    spiral_contour = max(contours, key=cv2.contourArea)
    spiral_coords = spiral_contour.reshape(-1, 2)

    spiral_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(spiral_image, [spiral_contour], -1, (0, 255, 0), 2)

    plt.imshow(cv2.cvtColor(spiral_image, cv2.COLOR_BGR2RGB))
    plt.title("Detekovaná špirála")
    plt.axis('on')
    plt.show()

    return spiral_coords

def preprocess_dataset(selected_dir):
    resolution_x = 1920
    resolution_y = 1080
    size_x_mm = 344.16
    size_y_mm = 193.59

    scale_x = size_x_mm / resolution_x
    scale_y = size_y_mm / resolution_y

    db_path = r'C:\\Users\\hlava\\OneDrive\\Počítač\\BP\\PARAMETRE\\spiralTrim'
    iDir = os.path.join(db_path, selected_dir)

    if os.path.isdir(iDir):
        svc_file_path = os.path.join(iDir, "spiral.svc")

        if os.path.isfile(svc_file_path):
            data_spiral = pd.read_csv(svc_file_path, delimiter=' ', skiprows=1, header=None, names=['X', 'Y', 'timestamp', 'on_surface', 'ir1', 'ir2', 'ir3'])
            nd = data_spiral[data_spiral['on_surface'] == 1].copy()

            nd['X_mm'] = nd['X']
            nd['Y_mm'] = nd['Y']
            return nd[['X_mm', 'Y_mm']].values, nd
        else:
            print(f'Subor "spiral.svc" se nepodarilo najst v {selected_dir}.')
            return None, None
    else:
        print(f'Adresar {selected_dir} neexistuje.')
        return None, None

# Výpočet euklidovských vzdialeností
def calculate_euclidean_distances(spiral_coords_dataset, spiral_coords_template):
    distances = distance.cdist(spiral_coords_dataset, spiral_coords_template, metric='euclidean')
    min_distances = np.min(distances, axis=1)
    return min_distances

# MAIN
image_path = r"C:\\Users\\hlava\\OneDrive\\Dokumenty\\vybielenapredloha.png"
selected_dir = input("Zadejte ID (nápoveda: 2-198): ")

# Extrakcia suradnic z predlohy
spiral_coords_template = extract_spiral_coords(image_path)
if spiral_coords_template is not None:
    print(f"Suradnice z predlohy: {spiral_coords_template}")

    pixel_pitch = 0.17925  # vzdialenost medzi pixelmi v mm
    scaling_factor_X = 0.9926
    scaling_factor_Y = 0.9926       

    # Úprava a škálovanie súradníc
    spiral_coords_template[:, 0] = (spiral_coords_template[:, 0] + 5) / scaling_factor_X * (100 * pixel_pitch)
    spiral_coords_template[:, 1] = (spiral_coords_template[:, 1] + 10) / scaling_factor_Y * (100 * pixel_pitch)

    print(f"Suradnice z predlohy po úprave: {spiral_coords_template}")

    spiral_coords_dataset, nd = preprocess_dataset(selected_dir)

    if spiral_coords_dataset is not None:
        print(f"Suradnice z datasetu: {spiral_coords_dataset}")

        # Výpočet euklidovských vzdialeností
        distances = calculate_euclidean_distances(spiral_coords_dataset, spiral_coords_template)

        nd['DTT'] = distances  # Hodnoty DTT budú v mm

        output_dir = os.path.join(r'C:\\Users\\hlava\\OneDrive\\Počítač\\BP\\PARAMETRE\\spiralTrim', selected_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_file_path = os.path.join(output_dir, "vysledky2.xlsx")

        with pd.ExcelWriter(output_file_path) as writer:
            nd.to_excel(writer, sheet_name='Vypočítané data', index=False)
            pd.DataFrame(spiral_coords_template, columns=['X_template', 'Y_template']).to_excel(writer, sheet_name='Suradnice z preedlohy', index=False)

        print(f'Data boli ulozene do suboru: {output_file_path}')
    else:
        print("Nepodarilo se načítat suradnice z datasetu.")
else:
    print("Nepodarilo se extrahovat suradnice z obrázku.")
