import numpy as np

# Positions de départ des tétriminos {rotation: position}
START_POS_TETROMINOES = {
    'i': {0: 4, 1: 5, 2: 4, 3: 6},
    't': {0: 4, 1: 4, 2: 4, 3: 5},
    'o': {0: 5, 1: 5, 2: 5, 3: 5},
    'l': {0: 4, 1: 4, 2: 4, 3: 5},
    'j': {0: 4, 1: 4, 2: 4, 3: 5},
    's': {0: 4, 1: 4, 2: 4, 3: 5},
    'z': {0: 4, 1: 4, 2: 4, 3: 5},
}

# Valeurs des couleurs pour chaque tétrimino
TETROMINOES_BRG = {'i': [209, 206, 0],
                   'o': [0, 255, 255],
                   't': [139, 0, 139],
                   'j': [174, 65, 3],
                   'l': [28, 151, 255],
                   's': [59, 203, 114],
                   'z': [19, 50, 255]}

# Formes des tétriminos représentées par des tableaux numpy
TETROMINOES_SHAPES = {
    'i': np.array([
        [1, 1, 1, 1]
    ]),

    't': np.array([
        [0, 1, 0],
        [1, 1, 1]
    ]),

    'o': np.array([
        [1, 1],
        [1, 1]
    ]),

    'j': np.array([
        [1, 0, 0],
        [1, 1, 1]
    ]),

    'l': np.array([
        [0, 0, 1],
        [1, 1, 1]
    ]),

    's': np.array([
        [0, 1, 1],
        [1, 1, 0]
    ]),

    'z': np.array([
        [1, 1, 0],
        [0, 1, 1]
    ]),
}

