# DEV_1/generador_dfs.py
import random
import sys

sys.setrecursionlimit(5000)

def generar_laberinto(filas, columnas):
    matriz = [[1 for _ in range(columnas)] for _ in range(filas)]
    
    def dfs(f, c):
        matriz[f][c] = 0 
        direcciones = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcciones)
        
        for df, dc in direcciones:
            nf, nc = f + df, c + dc
            if 0 < nf < filas - 1 and 0 < nc < columnas - 1 and matriz[nf][nc] == 1:
                matriz[f + df//2][c + dc//2] = 0
                dfs(nf, nc)

    dfs(1, 1)
    
    # --- NUEVA LÓGICA DE INICIO Y META DINÁMICOS ---
    caminos = []
    # Recopilar todos los caminos (0) generados
    for f in range(1, filas - 1):
        for c in range(1, columnas - 1):
            if matriz[f][c] == 0:
                caminos.append((f, c))
                
    # Ordenamos los caminos por la suma de sus coordenadas.
    # Los más cercanos a la esquina superior izquierda quedan al principio.
    caminos.sort(key=lambda pos: pos[0] + pos[1])
    
    # Inicio (2): Elegimos uno aleatorio del primer 20% de los caminos
    rango_inicio = max(1, len(caminos) // 5)
    f_inicio, c_inicio = random.choice(caminos[:rango_inicio])
    matriz[f_inicio][c_inicio] = 2
    
    # Meta (3): Elegimos uno aleatorio del último 20% de los caminos
    rango_meta = max(1, len(caminos) // 5)
    f_meta, c_meta = random.choice(caminos[-rango_meta:])
    matriz[f_meta][c_meta] = 3
    
    return matriz