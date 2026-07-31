# DEV_1/validacion.py
def es_posicion_valida(fila, columna, matriz):
    filas_max = len(matriz)
    col_max = len(matriz[0])
    
    if 0 <= fila < filas_max and 0 <= columna < col_max:
        # Puede caminar sobre camino(0), inicio(2), meta(3), escombro(4) y fuego(5)
        return matriz[fila][columna] != 1
    return False