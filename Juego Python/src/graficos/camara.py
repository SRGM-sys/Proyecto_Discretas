# DEV_2/camara.py
from config import ANCHO_PANTALLA, ALTO_PANTALLA

class Camara:
    def __init__(self):
        self.desplazamiento_x = 0
        self.desplazamiento_y = 0

    def actualizar(self, jugador_x_pixel, jugador_y_pixel):
        # Calcula el centro de la pantalla
        centro_x = ANCHO_PANTALLA // 2
        centro_y = ALTO_PANTALLA // 2
        
        # Mueve la cámara en dirección contraria al jugador
        self.desplazamiento_x = centro_x - jugador_x_pixel
        self.desplazamiento_y = centro_y - jugador_y_pixel