# DEV_1/validacion.py

def es_posicion_valida(fila, columna, matriz):
    filas_max = len(matriz)
    col_max = len(matriz[0])
    
    # Comprobar límites del mapa
    if 0 <= fila < filas_max and 0 <= columna < col_max:
        # Es válido si NO es una pared (1)
        # O sea, puede pisar 0(camino), 2(inicio), 3(meta) y 4(trampa)
        return matriz[fila][columna] != 1
    return False