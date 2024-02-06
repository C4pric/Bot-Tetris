# Bot-Tetris
Ce programme utilise la vision d'opencv pour jouer le meilleur coup disponible automatiquement
Il se décompose en 5 fichiers ayant chacun leurs utilité au sein du programme :
- tetrominoes.py --> donne des informations sur la forme, la couleur et les rotations des différentes formes du jeu
- criteria.py -->  calcul l'espace entre chaque bloc, compte les potentiels trous et gère les différentes interractions entre les blocs
- recognition.py --> Ce fichier récupère toute les données nécessaires au bon fonctionnement du jeu et permet l'interraction entre l'ia et Tetris
- position.py --> Il forme le coeur de l'IA et trouve la meilleure combinaison possible en testant toutes les rotations et les positions, c'est ce programme qui gère le système de récompense

# Computer Vision

Comment ça fonctionne?
Lorsque le bot démarre, il essaie de trouver une application de jeu et attend que le jeu démarre. Lorsque le jeu démarre, le bot détecte le plateau, les tétrominos du jeu en utilisant Opencv. Récupère les images en temps réel et transfère la carte en matrice bolléenne (0 - cellule vide, 1 - cellule occupée) et identifie le tétromino actuel...

- Run `bot.exe`
- Start new Game
- Enjoy:)
