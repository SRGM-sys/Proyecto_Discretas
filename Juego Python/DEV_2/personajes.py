import os


# ---------------------------------------------------------
# RUTAS
# ---------------------------------------------------------

# Carpeta principal:
# Juego Python/
RUTA_RAIZ = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# assets/sprites/
CARPETA_SPRITES = os.path.join(
    RUTA_RAIZ,
    "assets",
    "sprites"
)

# assets/sprites/personajes/
CARPETA_PERSONAJES = os.path.join(
    CARPETA_SPRITES,
    "personajes"
)


# ---------------------------------------------------------
# PERSONAJES DISPONIBLES
# ---------------------------------------------------------

PERSONAJES = [
    {
        "nombre": "Minion",

        "sprite": os.path.join(
            CARPETA_PERSONAJES,
            "spriteMINION.png"
        ),

        # Su hoja tiene 4 filas y 4 columnas.
        "filas": 4,
        "columnas": 4,

        # Filas que utiliza el juego:
        # 0 = caminar lateral
        # 1 = caminar de frente
        # 2 = fuego
        # 3 = agua
        "filas_usadas": [0, 1, 2, 3]
    },

    {
        "nombre": "Pou",

        "sprite": os.path.join(
            CARPETA_PERSONAJES,
            "spritePOU.png"
        ),

        # Pou tiene 5 filas.
        "filas": 5,
        "columnas": 4,

        # El juego utilizará solamente las primeras 4.
        "filas_usadas": [0, 1, 2, 3]
    },

    {
        "nombre": "Peppa Pig",

        "sprite": os.path.join(
            CARPETA_PERSONAJES,
            "spritePEPA.png"
        ),

        "filas": 4,
        "columnas": 4,

        "filas_usadas": [0, 1, 2, 3]
    },

    {
        "nombre": "Principal",

        "sprite": os.path.join(
            CARPETA_SPRITES,
            "chica_pro.png"
        ),

        "filas": 4,
        "columnas": 4,

        "filas_usadas": [0, 1, 2, 3]
    }
]