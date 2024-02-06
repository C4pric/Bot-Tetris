import cv2
from recognition import find_game_window, recognize_board_game

if __name__ == '__main__':
    # Recherche de la fenêtre du jeu
    game_hwnd = find_game_window()

    # Boucle principale du programme
    while True:
        try:
            # Reconnaissance et analyse du plateau de jeu
            board_array = recognize_board_game(game_hwnd)
        except:
            # Fermeture des fenêtres OpenCV et affichage d'un message si l'application du jeu est fermée ou s'est effondrée
            cv2.destroyAllWindows()
            print('L\'application a été fermée ou s\'est effondrée')
            break

    # Fermeture de toutes les fenêtres OpenCV à la fin du programme
    cv2.destroyAllWindows()

# Attente d'une entrée de l'utilisateur pour terminer le programme
input("Le programme est terminé, appuyez sur ENTRER")
