import numpy as np

# Coefficients utilisés pour calculer le score final
HEIGHT_COEFFICIENT = 0
LINES_COEFFICIENT = 0.760666
HOLES_COEFFICIENT = 0.35663
BUMPINESS_COEFFICIENT = 0.184483
WEIGHT_COEFFICIENT = 0.510066

# Fonction pour obtenir les sommets (hauteurs) de chaque colonne du plateau
def get_peaks(board):
    peaks = np.array([])

    for j in range(board.shape[1]):
        if 1 in board[:, j]:  # Vérifie si la colonne contient des blocs
            value = board.shape[0] - np.argmax(board[:, j])  # Trouve la hauteur du sommet
        else:
            value = 0
        peaks = np.append(peaks, value)

    return peaks

# Fonction pour calculer le poids agrégé (somme des hauteurs des sommets)
def get_aggregate_weight(peaks):
    return np.sum(peaks)

# Fonction pour calculer le nombre de trous dans le plateau
def get_holes(board, peaks):
    holes_count = np.array([])

    for i in range(board.shape[1]):
        if peaks[i] == 0:  # Si la colonne est vide, il n'y a pas de trou
            holes_count = np.append(holes_count, 0)
        else:
            # Calcul du nombre de trous en dessous du sommet de la colonne
            holes_count = np.append(holes_count, peaks[i] - np.sum(board[int(-peaks[i]):, i]))

    return sum(holes_count)

# Fonction pour calculer la rugosité du plateau
def get_bumpiness(peaks):
    bumpiness = 0
    for i in range(len(peaks) - 1):
        # Calcul de la différence de hauteur absolue entre les colonnes adjacentes
        bumpiness += abs(peaks[i] - peaks[i + 1])

    return bumpiness

# Fonction pour calculer le nombre de lignes complètes sur le plateau
def get_lines(board):
    lines_count = 0
    for i in range(board.shape[0]):
        if 0 not in board[i, :]:  # Vérifie si la ligne est complète (aucune case vide)
            lines_count += 1

    return lines_count

# Fonction pour obtenir la hauteur maximale du plateau
def get_height(board):
    return np.max(get_peaks(board))

# Fonction pour calculer le nombre de sommets non nuls (colonnes contenant des blocs)
def get_peaks_number(peaks):
    peaks_count = 0
    for i in range(len(peaks)):
        if peaks[i] != 0:
            peaks_count += 1
    return peaks_count
