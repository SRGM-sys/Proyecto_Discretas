# DEV_1/trampas.py
import random

def inyectar_obstaculos(matriz, cantidad):
    """Genera escombros (valor 4) en el mapa que hacen daño al pisarlos"""
    filas = len(matriz)
    columnas = len(matriz[0])
    obstaculos_colocados = 0
    
    while obstaculos_colocados < cantidad:
        f = random.randint(1, filas - 2)
        c = random.randint(1, columnas - 2)
        
        # Solo poner obstáculos en caminos libres (0)
        if matriz[f][c] == 0:
            matriz[f][c] = 4
            obstaculos_colocados += 1
            
    return matriz