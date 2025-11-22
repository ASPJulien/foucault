import csv
import matplotlib.pyplot as plt
import numpy as np  # Pour arctan2, unwrap, etc.

# Nom du fichier CSV (change si besoin)
csv_filename = 'simsim.csv'

# Listes pour stocker les données
frames = []
xs = []
ys = []
rayons = []  # Gardé au cas où, mais pas utilisé dans les plots demandés

# Lecture du CSV
try:
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Skip headers

        for row in reader:
            #print(row)
            if len(row) >= 2:  # Au minimum Frame, X, Y (rayon optionnel)
                frames.append(int(row[0]))
                xs.append(float(row[1]))  # Float pour plus de précision
                ys.append(float(row[2]))

    if not frames:
        print("Aucun données dans le CSV. Exécute le premier script d'abord !")
        exit()

except FileNotFoundError:
    print(f"Fichier '{csv_filename}' non trouvé. Vérifie le chemin !")
    exit()
except Exception as e:
    print(f"Erreur de lecture CSV : {e}")
    exit()

# Infos basiques
print(f"{len(frames)} entrées lues du CSV.")

# Estimation du centre (point d'attache du pendule, vu du haut)
# Moyenne des positions (assume oscillation autour de ce point ; ajuste si tu connais les coords fixes, ex. x_center=320)
x_center = np.mean(xs)
y_center = np.mean(ys)
print(f"Point central estimé : ({x_center:.2f}, {y_center:.2f})")

# Calcul des angles pour le pendule de Foucault (vu du haut : angle polaire θ par rapport au centre)
# θ = arctan2(Δy, Δx) en radians, puis unwrap pour gérer les rotations continues (>360°)
# Converti en degrés pour le plot
angles_rad = [np.arctan2(y - y_center, x - x_center) for x, y in zip(xs, ys)]
angles_deg = np.degrees(np.unwrap(angles_rad))  # Unwrap pour voir la rotation cumulative (ex. pour l'effet Coriolis)
frames = np.array(frames)

# Plot 1 : Trajectoire du pendule (X vs Y), coloré par frame pour voir l'évolution
plt.figure(figsize=(8, 6))
sc = plt.scatter(xs, ys, c=frames, cmap='viridis', marker='o', s=50)  # Taille des points augmentée
plt.colorbar(sc, label='Numéro de Frame')  # Barre de couleur pour le temps
plt.title('Trajectoire du Pendule de Foucault (Vu du Haut)')
plt.xlabel('Position X (pixels)')
plt.ylabel('Position Y (pixels)')
plt.grid(True)
plt.axis('equal')  # Garde l'aspect ratio pour une vue "du haut" réaliste
plt.show()

cc, co =  np.polyfit(frames*30/3600,angles_deg,1)

# Plot 2 : Évolution de l'angle (rotation du plan d'oscillation vs Frame)
# Cela montre la précession due à la rotation de la Terre (lente rotation de l'angle)
plt.figure(figsize=(10, 6))
plt.plot(frames*30/3600, angles_deg, 'm-', marker='o')  # Ligne magenta
plt.plot(frames*30/3600, cc*frames*30/3600 + co, ":r")
plt.title('Évolution de l\'Angle du Pendule de Foucault au fil des Frames')
plt.xlabel('Frame')
plt.ylabel('Angle Cumulatif (degrés)')
plt.grid(True)
plt.show()
print(cc,co)