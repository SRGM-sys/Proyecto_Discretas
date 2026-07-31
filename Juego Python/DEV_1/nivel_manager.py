# DEV_1/nivel_manager.py
from DEV_1.generador_dfs import generar_laberinto
from DEV_1.trampas import inyectar_trampas

class NivelManager:
    def __init__(self, filas_iniciales, col_iniciales):
        self.filas = filas_iniciales
        self.columnas = col_iniciales
        self.nivel_actual = 1
        self.cantidad_trampas = 5

    def generar_nuevo_nivel(self):
        """Crea el mapa con la dificultad actual"""
        matriz = generar_laberinto(self.filas, self.columnas)
        matriz = inyectar_trampas(matriz, self.cantidad_trampas)
        return matriz

    def subir_dificultad(self):
        """Aumenta el tamaño del mapa y las trampas para el siguiente nivel"""
        self.nivel_actual += 1
        self.filas += 2     # Sumamos 2 para que siempre siga siendo un número impar
        self.columnas += 2  # Sumamos 2 para que siempre siga siendo un número impar
        self.cantidad_trampas += 3