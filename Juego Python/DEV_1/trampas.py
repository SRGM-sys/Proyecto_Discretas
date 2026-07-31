import random

def inyectar_trampas(matriz, cantidad):
    filas = len(matriz)
    columnas = len(matriz[0])
    trampas_colocadas = 0
    
    while trampas_colocadas < cantidad:
        f = random.randint(1, filas - 2)
        c = random.randint(1, columnas - 2)
        
        # Solo poner trampa si es un camino normal (0)
        # Para no sobreescribir paredes, el inicio o la meta
        if matriz[f][c] == 0:
            matriz[f][c] = 4
            trampas_colocadas += 1
            
    return matriz