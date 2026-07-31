# DEV_1/generador_dfs.py
import random
import sys

# Aumentamos el límite de recursión por si hacen un mapa inmenso
sys.setrecursionlimit(5000)

def generar_laberinto(filas, columnas):
    # 1. Llenar todo de paredes (1)
    matriz = [[1 for _ in range(columnas)] for _ in range(filas)]
    
    def dfs(f, c):
        matriz[f][c] = 0 # Marcar como camino
        direcciones = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcciones) # Aleatorizar caminos
        
        for df, dc in direcciones:
            nf, nc = f + df, c + dc
            # Verificar límites y si es pared
            if 0 < nf < filas - 1 and 0 < nc < columnas - 1 and matriz[nf][nc] == 1:
                # Romper la pared intermedia
                matriz[f + df//2][c + dc//2] = 0
                dfs(nf, nc)
    
    # 2. Empezar a excavar desde la coordenada (1, 1)
    dfs(1, 1)
    
    # 3. Definir Inicio (2) y Meta (3)
    matriz[1][1] = 2
    matriz[filas - 2][columnas - 2] = 3
    
    return matriz