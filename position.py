import time
import win32api
import win32con
import numpy as np
from tetrominoes import START_POS_TETROMINOES, TETROMINOES_SHAPES
import criteria
import recognition

# Délai pour simuler l'appui sur une touche
KEY_DOWN_DELAY = 0.05

class PredictedBoard:

    def __init__(self, board=None, pos=-100):
        # Initialise une instance de PredictedBoard avec un plateau de jeu et une position par défaut
        self.board = board
        self.pos = pos

    def is_empty(self):
        # Vérifie si la prédiction est vide (c'est-à-dire si aucune position valide n'a été trouvée)
        return self.pos == -100

def try_put(board, board_col, board_row, tetromino, tetromino_name, rotation):
    # Essaye de placer un tétrimino sur le plateau de jeu à une position spécifique

    # Copie le plateau de jeu actuel pour ne pas le modifier directement
    new_board = board.copy()

    # Parcours chaque cellule du tétrimino pour vérifier s'il peut être placé sur le plateau
    for tetromino_col in range(tetromino.shape[1]):
        for tetromino_row in range(tetromino.shape[0]):
            # Vérifie si la position est valide pour placer le tétrimino
            if board_row == board.shape[0] - tetromino.shape[0] + 1 or new_board[
                board_row + tetromino_row, board_col + tetromino_col] + tetromino[tetromino_row, tetromino_col] > 1:
                # Retourne un objet PredictedBoard vide si la position est invalide
                return PredictedBoard()
            else:
                # Met à jour le plateau de jeu avec le tétrimino
                new_board[board_row + tetromino_row, board_col + tetromino_col] += tetromino[
                    tetromino_row, tetromino_col]

    # Calcul la position finale du tétrimino sur le plateau de jeu
    return PredictedBoard(new_board, board_col - START_POS_TETROMINOES[tetromino_name][rotation] + 1)

def get_all_variations(board, tetromino_name):
    # Génère toutes les variations possibles d'un tétrimino sur le plateau de jeu

    # Récupère la forme du tétrimino à partir de son nom
    tetromino = TETROMINOES_SHAPES[tetromino_name]
    variations = []
    pre_ans = None

    # Parcours les 4 rotations possibles du tétrimino
    for rotation in range(4):
        variations.append([])
        # Parcours chaque colonne du plateau de jeu pour essayer de placer le tétrimino
        for board_col in range(board.shape[1] - tetromino.shape[1] + 1):
            # Parcours chaque ligne du plateau de jeu pour essayer de placer le tétrimino
            for board_row in range(board.shape[0] - tetromino.shape[0] + 2):
                # Essaie de placer le tétrimino à cette position spécifique
                answer = try_put(board, board_col, board_row, tetromino, tetromino_name, rotation)
                # Si la position est invalide et qu'une position valide a été trouvée précédemment, ajoute-la aux variations
                if answer.is_empty() and pre_ans is not None and not pre_ans.is_empty():
                    variations[rotation].append(pre_ans)
                    break
                pre_ans = answer

        # Fait pivoter le tétrimino pour tester d'autres rotations
        tetromino = np.rot90(tetromino)

    return variations

def fitness_func(board, peaks):
    # Fonction d'évaluation de la qualité du plateau de jeu

    return criteria.HEIGHT_COEFFICIENT * criteria.get_height(board) - \
           criteria.LINES_COEFFICIENT * criteria.get_lines(board) + \
           criteria.HOLES_COEFFICIENT * criteria.get_holes(board, peaks) + \
           criteria.BUMPINESS_COEFFICIENT * criteria.get_bumpiness(peaks) + \
           criteria.WEIGHT_COEFFICIENT * criteria.get_aggregate_weight(peaks)

def get_best_pos(var):
    # Trouve la meilleure position pour placer un tétrimino sur le plateau de jeu

    score = 10000000
    rotation = -10
    position = -10
    board = None

    # Parcours les variations de chaque rotation du tétrimino
    for i in range(len(var)):
        current_rotation = i
        for variant in var[i]:
            current_pos = variant.pos
            # Calcule les pics du plateau de jeu après avoir placé le tétrimino
            peaks = criteria.get_peaks(variant.board)
            # Évalue la qualité du plateau de jeu avec le tétrimino placé
            current_score = fitness_func(variant.board, peaks)

            # Met à jour la meilleure position si le score actuel est meilleur que le meilleur score précédent
            if current_score < score:
                score = current_score
                rotation = current_rotation
                position = current_pos
                board = variant.board

    # Affiche les informations sur la meilleure position trouvée
    print("position", position, 'rotation', rotation, 'score', score)
    return position, rotation

def move(game_hwnd, position, rotation):
    # Déplace un tétrimino dans la fenêtre du jeu

    # Effectue la rotation nécessaire
    for _ in range(rotation):
        win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, ord('A'))
        win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, ord('A'))
        time.sleep(KEY_DOWN_DELAY)

    # Déplace le tétrimino horizontalement vers la gauche ou la droite
    for _ in range(abs(position)):
        if position < 0:
            win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT)
            win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_LEFT)
        else:
            win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT)
            win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT)
        time.sleep(KEY_DOWN_DELAY)

    # Fait tomber le tétrimino en appuyant sur la touche d'espace
    win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_SPACE)
    win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_SPACE)
    time.sleep(KEY_DOWN_DELAY)

