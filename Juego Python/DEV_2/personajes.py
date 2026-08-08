import os


# Carpeta principal del proyecto: Juego Python
RUTA_RAIZ = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Carpeta general de sprites
CARPETA_SPRITES = os.path.join(
    RUTA_RAIZ,
    "assets",
    "sprites"
)

# Carpeta que contiene los rostros nuevos
CARPETA_PERSONAJES = os.path.join(
    CARPETA_SPRITES,
    "personajes"
)


PERSONAJES = [
    {
        "nombre": "Minion",
        "archivo": os.path.join(
            CARPETA_PERSONAJES,
            "minionRO.png"
        ),
        "usar_rostro": True
    },
    {
        "nombre": "Pou",
        "archivo": os.path.join(
            CARPETA_PERSONAJES,
            "pouRO.png"
        ),
        "usar_rostro": True
    },
    {
        "nombre": "Peppa Pig",
        "archivo": os.path.join(
            CARPETA_PERSONAJES,
            "pepaRO.png"
        ),
        "usar_rostro": True
    },
    {
        "nombre": "Winnie Pooh",
        "archivo": os.path.join(
            CARPETA_PERSONAJES,
            "winnieRO.png"
        ),
        "usar_rostro": True
    },
    {
        "nombre": "Pablo",
        "archivo": os.path.join(
            CARPETA_PERSONAJES,
            "pabloRO.png"
        ),
        "usar_rostro": True
    },
    {
        "nombre": "Niña original",
        "archivo": os.path.join(
            CARPETA_SPRITES,
            "chica_pro.png"
        ),
        "usar_rostro": False
    }
]