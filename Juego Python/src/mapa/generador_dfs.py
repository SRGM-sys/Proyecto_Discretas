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
    
    # --- LÓGICA DE INICIO FIJO Y META EN EL NODO MÁS LEJANO (BFS) ---
    
    # 1. Fijar el inicio en la esquina superior izquierda
    f_inicio, c_inicio = 1, 1
    matriz[f_inicio][c_inicio] = 2
    
    # 2. Encontrar el nodo más lejano mediante Búsqueda en Anchura (BFS)
    cola = [(f_inicio, c_inicio, 0)]  # Tupla: (fila, columna, distancia_en_pasos)
    visitados = set()
    visitados.add((f_inicio, c_inicio))
    
    nodo_mas_lejano = (f_inicio, c_inicio)
    max_distancia = 0
    
    while cola:
        f, c, dist = cola.pop(0)
        
        # Si esta celda requiere más pasos, la guardamos como la nueva candidata a meta
        if dist > max_distancia:
            max_distancia = dist
            nodo_mas_lejano = (f, c)
            
        # Explorar los 4 vecinos posibles
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for df, dc in direcciones:
            nf, nc = f + df, c + dc
            # Verificar límites y que sea un camino válido ('0')
            if 0 < nf < filas - 1 and 0 < nc < columnas - 1:
                if matriz[nf][nc] == 0 and (nf, nc) not in visitados:
                    visitados.add((nf, nc))
                    cola.append((nf, nc, dist + 1))
                    
    # 3. Colocar el portal de meta en el nodo que registró la mayor distancia
    f_meta, c_meta = nodo_mas_lejano
    matriz[f_meta][c_meta] = 3
    
    return matriz

def hacer_pasillos_anchos(matriz_original):

    matriz_ancha = []

    for fila in matriz_original:

        fila_doble = []

        for celda in fila:
            fila_doble.extend(
                [celda, celda]
            )

        matriz_ancha.append(
            fila_doble
        )

        matriz_ancha.append(
            list(fila_doble)
        )

    return matriz_ancha