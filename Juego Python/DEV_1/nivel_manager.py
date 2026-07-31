# DEV_1/nivel_manager.py
from DEV_1.generador_dfs import generar_laberinto
from DEV_1.trampas import inyectar_obstaculos, inyectar_recargas
from DEV_1.incendio_logica import iniciar_fuego_seguro

# 1. Dev 1 pega la función aquí arriba (fuera de la clase)
def hacer_pasillos_anchos(matriz_original):
    """Convierte un mapa normal en uno donde todo mide 2x2 bloques"""
    matriz_ancha = []
    for fila in matriz_original:
        fila_doble = []
        for celda in fila:
            fila_doble.extend([celda, celda]) # Duplica en ancho
        matriz_ancha.append(fila_doble)
        matriz_ancha.append(list(fila_doble)) # Duplica en alto
    return matriz_ancha

class NivelManager:
    def __init__(self, filas_iniciales, col_iniciales):
        self.filas = filas_iniciales
        self.columnas = col_iniciales
        self.nivel_actual = 1
        self.cantidad_trampas = 5

    def generar_nuevo_nivel(self):
        # 2. Genera el mapa matemático base
        matriz = generar_laberinto(self.filas, self.columnas)
        
        # 3. ¡LA MAGIA OCURRE AQUÍ! Ensancha los pasillos
        matriz = hacer_pasillos_anchos(matriz)
        
        # 4. Inyecta todo lo demás. ¡Como el pasillo es ancho, los obstáculos se podrán esquivar!
        matriz = inyectar_obstaculos(matriz, self.cantidad_trampas)
        matriz = inyectar_recargas(matriz, 2)
        matriz = iniciar_fuego_seguro(matriz, 2)
        
        return matriz

    def subir_dificultad(self):
        self.nivel_actual += 1
        self.filas += 2     
        self.columnas += 2  
        self.cantidad_trampas += 3