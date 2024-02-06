
import time
import cv2
import numpy as np
from ctypes import windll
import win32com.client
from PIL import ImageGrab
import win32gui
from position import get_all_variations, get_best_pos, move
from tetrominoes import TETROMINOES_BRG

# Nom de l'application Tetris
APP_NAME = 'TETRIS'
windows_list = []

# Fonction pour corriger les problèmes de dpi
def configure_win32():
    user32 = windll.user32
    user32.SetProcessDPIAware()

# Fonction pour énumérer les fenêtres Windows
def enum_win(hwnd, result):
    # Récupérer le texte de la fenêtre
    win_text = win32gui.GetWindowText(hwnd)
    # Ajouter la fenêtre à la liste des fenêtres
    windows_list.append((hwnd, win_text))

# Fonction pour obtenir toutes les fenêtres
def get_all_windows():
    top_list = []
    # Enumérer toutes les fenêtres et les ajouter à la liste
    win32gui.EnumWindows(enum_win, top_list)

# Fonction pour mettre la fenêtre en premier plan
def set_foreground(hwnd):
    # Créer une instance de l'objet Shell pour envoyer des touches
    shell = win32com.client.Dispatch("WScript.Shell")
    # Envoyer la touche ALT pour mettre la fenêtre en premier plan
    shell.SendKeys('%')
    # Définir la fenêtre spécifiée en premier plan
    win32gui.SetForegroundWindow(hwnd)

# Fonction pour trouver la fenêtre du jeu
def find_game_window():
    # Configurer Win32 pour gérer les DPI
    configure_win32()
    while True:
        # Obtenir toutes les fenêtres ouvertes
        get_all_windows()
        # Parcourir toutes les fenêtres pour trouver celle avec le nom spécifié
        for (hwnd, win_text) in windows_list:
            if win_text == APP_NAME:
                # Mettre la fenêtre en premier plan
                set_foreground(hwnd)
                return hwnd

        # Attendre une seconde avant de réessayer
        time.sleep(1)
        # Afficher un message pour indiquer qu'il faut ouvrir l'application si elle n'est pas trouvée
        print('Veuillez ouvrir l'application', end='\r')

# Fonction pour prendre une capture d'écran
def take_screenshot(position):
    # Prendre une capture d'écran de la région spécifiée
    screenshot = ImageGrab.grab(position)
    # Convertir la capture d'écran en tableau numpy
    screenshot = np.array(screenshot)
    # Convertir le format de couleur de la capture d'écran de RGB à BGR (utilisé par OpenCV)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

# Fonction pour détecter le plateau de jeu
def detect_the_board(screenshot):
    # Définir les couleurs de la zone du plateau de jeu
    board_color = (np.array([12, 12, 12]), np.array([18, 18, 18]))
    # Créer un masque pour extraire la zone du plateau de jeu de la capture d'écran
    board_mask = cv2.inRange(screenshot, board_color[0], board_color[1])
    # Trouver les contours dans le masque
    contours, _ = cv2.findContours(board_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Trier les contours par aire, du plus grand au plus petit
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    # Retourner le contour avec la plus grande aire (c'est-à-dire le contour du plateau de jeu) et le masque
    return contours[0], board_mask

# Fonction pour définir la position sur le plateau de jeu
def set_position_on_the_board(board_arr, x, y, board_x, board_y, board_w, block_width, block_height):
    # Vérifier si les coordonnées sont à l'intérieur du plateau de jeu
    if x < board_x or x > board_x + board_w:
        return

    # Calculer les indices de la position sur le plateau de jeu et la marquer comme occupée dans le tableau
    board_arr[int((y - board_y) / block_height), int((x - board_x) / block_width)] = 1

# Fonction pour créer les cellules du plateau de jeu
def create_cells(board, board_x, board_y, block_width, block_height):
    # Parcourir chaque cellule du plateau de jeu et dessiner un rectangle autour de celle-ci
    for row in range(20):
        for col in range(10):
            block_x = block_width * col
            block_y = block_height * row

            cv2.rectangle(board, (board_x + block_x, board_y + block_y),
                          (board_x + block_x + block_width, board_y + block_y + block_height),
                          (255, 255, 255), 1)

# Fonction pour vérifier les 2 premières lignes du plateau
def check_first_2_lines(x, y, board_x, board_y, board_w, block_width, block_height):
    # Vérifier si les coordonnées sont dans les 2 premières lignes du plateau
    if board_x + block_height * 3 <= x <= board_x + board_w - block_width * 3 \
            and board_y <= y <= board_y + block_height * 3:
        return True

    return False

# Fonction pour afficher du texte sur l'écran
def show_text(frame_name, board=None, txt=None):
    # Créer une image noire pour afficher le texte
    img = np.zeros((400, 400, 1), np.uint8)
    # Parcourir chaque ligne du tableau et dessiner le texte
    for i in range(board.shape[0]):
        cv2.putText(img, str(board[i, :]),
                    (100, 16 * i + 50),
                    cv2.FONT_HERSHEY_TRIPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                    1)
    # Dessiner le texte en bas de l'image
    cv2.putText(img, txt, (20, 336 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1, 1)
    # Afficher l'image
    cv2.imshow(frame_name, img)

# Fonction pour visualiser les captures d'écran
def visualize(frames: list, board_x, board_y, block_width, block_height):
    # Redimensionner chaque capture d'écran pour l'affichage
    frames_resized = []
    for frame in frames:
        # Redimensionner la capture d'écran à 400x400 pixels
        frames_resized.append(cv2.resize(frame, (400, 400)))

    # Afficher les captures d'écran redimensionnées
    cv2.imshow('Écran', frames_resized[0])
    cv2.imshow('Plateau virtuel', frames_resized[1])
    cv2.imshow("Masque", frames_resized[2])
    cv2.waitKey(25)

# Fonction pour reconnaître le jeu de plateau
def recognize_board_game(game_hwnd):
    # Obtenir la position de la fenêtre du jeu
    position = win32gui.GetWindowRect(game_hwnd)
    # Prendre une capture d'écran de la région spécifiée
    screenshot = take_screenshot(position)
    rows, cols, _ = screenshot.shape

    # Détecter le contour du plateau de jeu dans la capture d'écran
    cnt, board_mask = detect_the_board(screenshot)
    (board_x, board_y, board_w, board_h) = cv2.boundingRect(cnt)
    cv2.drawContours(screenshot, [cnt], -1, (0, 255, 0), 3)

    # Vérifier si le plateau de jeu a la bonne proportion (2:1)
    if board_h / board_w != 2:
        # Afficher un message indiquant d'attendre si le plateau n'a pas la bonne proportion
        print('En attente du jeu...', end='\r')
        time.sleep(1)
        return

    # Calculer la taille d'un bloc sur le plateau de jeu
    block_width = int(board_w / 10)
    block_height = int(board_h / 20)

    # Créer un tableau numpy pour représenter le plateau de jeu
    board_array = np.zeros((20, 10), dtype=int)
    current_tetromino = ''

    # Parcourir les couleurs des tétriminos pour les détecter sur le plateau de jeu
    for key in TETROMINOES_BRG:
        bgr_color = TETROMINOES_BRG[key]
        bgr_color = np.array(bgr_color)
        mask = cv2.inRange(screenshot, bgr_color, bgr_color)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            # Vérifier si le tétrimino se trouve dans les 2 premières lignes du plateau de jeu
            if check_first_2_lines(x, y, board_x, board_y, board_w, block_width, block_height):
                current_tetromino = key

            # Marquer la position du tétrimino sur le plateau de jeu
            set_position_on_the_board(board_array, x, y, board_x, board_y, board_w, block_width, block_height)

    # Vérifier si aucun tétrimino n'a été détecté sur le plateau de jeu
    if current_tetromino == '':
        return

    # Générer toutes les variations possibles du tétrimino sur le plateau de jeu
    var = get_all_variations(board_array[3:, :], current_tetromino)

    # Trouver la meilleure position et rotation pour placer le tétrimino
    position, rotation = get_best_pos(var)
    # Déplacer le tétrimino dans la fenêtre du jeu
    move(game_hwnd, position, rotation)

    # Retourner le tableau représentant le plateau de jeu après avoir placé le tétrimino
    return board_array

