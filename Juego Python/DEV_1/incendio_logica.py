# DEV_1/incendio_logica.py
import random

def iniciar_fuego(matriz, cantidad_focos):
    """Crea los primeros focos de incendio (valor 5) en el mapa"""
    filas = len(matriz)
    columnas = len(matriz[0])
    fuegos_colocados = 0
    
    while fuegos_colocados < cantidad_focos:
        f = random.randint(1, filas - 2)
        c = random.randint(1, columnas - 2)
        
        if matriz[f][c] == 0:
            matriz[f][c] = 5
            fuegos_colocados += 1
    return matriz

def propagar_incendio(matriz, probabilidad=0.10):
    """
    Expande el fuego a las casillas adyacentes.
    Debe llamarse periódicamente (ej. cada segundo o cada X frames).
    """
    filas = len(matriz)
    columnas = len(matriz[0])
    nuevos_fuegos = [] # Transformación temporal
    
    for f in range(filas):
        for c in range(columnas):
            if matriz[f][c] == 5: # Si la casilla actual está en llamas
                direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                
                for df, dc in direcciones:
                    nf, nc = f + df, c + dc
                    
                    if 0 <= nf < filas and 0 <= nc < columnas:
                        # El fuego consume caminos(0), inicio(2) y escombros(4)
                        if matriz[nf][nc] in [0, 2, 4]:
                            if random.random() < probabilidad:
                                nuevos_fuegos.append((nf, nc))
                                
    # Aplicar la matriz de transformación al estado real
    for f, c in nuevos_fuegos:
        matriz[f][c] = 5
        
    return matriz