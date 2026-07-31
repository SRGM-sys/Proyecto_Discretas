# config.py
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# config.py
FILAS = 11
COLUMNAS = 15

# Magia pro: calculamos el tamaño de la celda para que quepa exacto en pantalla
TAMANO_CELDA_X = ANCHO_PANTALLA // COLUMNAS
TAMANO_CELDA_Y = ALTO_PANTALLA // FILAS
TAMANO_CELDA = min(TAMANO_CELDA_X, TAMANO_CELDA_Y) # Usamos el menor para que sean cuadrados perfectos

FPS = 60

# Colores rápidos (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_PARED = (100, 100, 100)
VERDE_JUGADOR = (0, 255, 0)
ROJO_FUEGO = (220, 50, 50)
AZUL_AGUA = (50, 50, 220)