# Bot-Tetris
Ce programme utilise la vision d'opencv pour jouer le meilleur coup disponible automatiquement
Il se décompose en 5 fichiers ayant chacun leurs utilité au sein du programme :
- tetrominoes.py --> donne des informations sur la forme, la couleur et les rotations des différentes formes du jeu
- criteria.py -->  calcul l'espace entre chaque bloc, compte les potentiels trous et gère les différentes interractions entre les blocs
- recognition.py --> Ce fichier récupère toute les données nécessaires au bon fonctionnement du jeu et permet l'interraction entre l'ia et Tetris
- position.py --> Il forme le coeur de l'IA et trouve la meilleure combinaison possible en testant toutes les rotations et les positions, c'est ce programme qui gère le système de récompense

# Computer Vision

How it works? 
When bot started he tries to find game aplication and wait until game is started. When game is started bot detectes the board, the tetrominoes in the game using Opencv. Grabs the images in realtime and transfroms board to bollean matrix (0 - empty cell , 1 - occupied cell) and identify current tetromino...

- Run `bot.exe`
- Start new Game
- Enjoy:)
