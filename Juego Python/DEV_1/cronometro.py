# DEV_1/cronometro.py
import time

class Cronometro:
    def __init__(self):
        self.tiempo_inicio = 0
        self.corriendo = False

    def iniciar(self):
        self.tiempo_inicio = time.time()
        self.corriendo = True

    def detener(self):
        self.corriendo = False

    def obtener_segundos(self):
        """DEV 2 llamará a esto en cada frame para dibujar el tiempo"""
        if not self.corriendo:
            return 0
        return int(time.time() - self.tiempo_inicio)