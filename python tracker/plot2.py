import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA  # Pour calculer l'angle principal

# Nom du fichier CSV
csv_filename = 'simsim.csv'

# Listes pour stocker les données
frames = []
xs = []
ys = []

# Lecture du CSV (version robuste, comme avant)
try:
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip headers

        for row_num, row in enumerate(reader, start=2):
            if len(row) < 3:
                print(f"Ligne {row_num} ignorée : pas assez de colonnes")
                continue
            try:
                frames.append(int(row[0]))
                xs.append(float(row[1]))
                ys.append(float(row[2]))
            except ValueError as ve:
                print(f"Erreur ligne {row_num} : {ve}")
                continue

    if not frames:
        print("Aucun données valides !")
        exit()

except FileNotFoundError:
    print(f"Fichier non trouvé !")
    exit()
except Exception as e:
    print(f"Erreur : {e}")
    exit()

print(f"{len(frames)} entrées lues.")

# Params pour l'analyse (ajuste selon ta vidéo)
fps = 30  # FPS de ta vidéo (récupère-le via cap.get(cv.CAP_PROP_FPS) dans le premier script, ou mets la vraie valeur)
window_size = 2500  # Nombre de frames par fenêtre pour PCA (ex. : 100 pour capturer plusieurs oscillations)
step_size = 50    # Pas entre fenêtres (pour overlapp, réduit pour plus de points)

# Estimation du centre
x_center = np.mean(xs)
y_center = np.mean(ys)
print(f"Centre estimé : ({x_center:.2f}, {y_center:.2f})")

# Calcul des angles de précession par fenêtres glissantes
window_frames = []  # Frame moyenne par fenêtre
precession_angles = []  # Angles en degrés

for start in range(0, len(xs) - window_size + 1, step_size):
    end = start + window_size
    window_x = np.array(xs[start:end]) - x_center
    window_y = np.array(ys[start:end]) - y_center
    points = np.column_stack((window_x, window_y))  # Matrice (N, 2)

    if len(points) < 2:
        continue  # Fenêtre trop petite

    pca = PCA(n_components=1)  # Axe principal
    pca.fit(points)
    angle_rad = np.arctan2(pca.components_[0][1], pca.components_[0][0])  # Angle de l'axe principal
    angle_deg = np.degrees(angle_rad)  # En degrés (-180 à 180)

    # Stocke
    window_frames.append(np.mean(frames[start:end]))  # Frame moyenne
    precession_angles.append(angle_deg)

# Calcul vitesse de précession moyenne (°/h)
if len(window_frames) > 1:
    total_time_hours = (max(window_frames) - min(window_frames)) / fps / 3600  # Frames -> secondes -> heures
    total_angle_change = precession_angles[-1] - precession_angles[0]
    precession_rate = total_angle_change / total_time_hours if total_time_hours > 0 else 0
    print(f"Vitesse de précession estimée : {precession_rate:.2f} °/h")
else:
    print("Pas assez de fenêtres pour calculer la précession.")

# Plot 1 : Trajectoire (X vs Y)
plt.figure(figsize=(8, 6))
plt.scatter(xs, ys, c=frames, cmap='viridis', marker='o', s=50)
plt.colorbar(label='Frame')
plt.title('Trajectoire du Pendule de Foucault (Vu du Haut)')
plt.xlabel('X (pixels)')
plt.ylabel('Y (pixels)')
plt.grid(True)
plt.axis('equal')
plt.show()

# Plot 2 : Évolution de l'angle de précession
plt.figure(figsize=(10, 6))
time_hours = np.array(window_frames) / fps / 3600  # Frames -> heures pour l'axe X
plt.plot(time_hours, precession_angles, 'm-', marker='o')
plt.title('Évolution de l\'Angle de Précession du Pendule de Foucault')
plt.xlabel('Temps (heures)')
plt.ylabel('Angle de Précession (degrés)')
plt.grid(True)
plt.show()