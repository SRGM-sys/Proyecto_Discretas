# DEV_1/incendio_logica.py
import random

# Variable para llevar la cuenta de los pasos del jugador
turnos_para_fuego = 0

def iniciar_fuego_seguro(matriz, cantidad_focos, dist_minima=6):
    """Crea fuegos LEJOS del inicio (1, 1) usando distancia Manhattan"""
    filas = len(matriz)
    columnas = len(matriz[0])
    fuegos_colocados = 0
    
    while fuegos_colocados < cantidad_focos:
        f = random.randint(1, filas - 2)
        c = random.randint(1, columnas - 2)
        
        distancia_al_jugador = abs(f - 1) + abs(c - 1)
        
        if matriz[f][c] == 0 and distancia_al_jugador >= dist_minima:
            matriz[f][c] = 5
            fuegos_colocados += 1
            
    return matriz

def propagar_incendio(matriz, probabilidad=0.10):
    """Lógica base que expande el fuego a las casillas adyacentes."""
    filas = len(matriz)
    columnas = len(matriz[0])
    nuevos_fuegos = [] 
    
    for f in range(filas):
        for c in range(columnas):
            if matriz[f][c] == 5:
                direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for df, dc in direcciones:
                    nf, nc = f + df, c + dc
                    if 0 <= nf < filas and 0 <= nc < columnas:
                        if matriz[nf][nc] in [0, 2, 4]: # Quema caminos, inicio y obstáculos
                            if random.random() < probabilidad:
                                nuevos_fuegos.append((nf, nc))
                                
    for f, c in nuevos_fuegos:
        matriz[f][c] = 5
        
    return matriz

def actualizar_fuego_por_turnos(matriz, frecuencia=3):
    """
    Se llama cada vez que el jugador se mueve. 
    Solo propaga el incendio si han pasado 'frecuencia' cantidad de turnos.
    """
    global turnos_para_fuego
    turnos_para_fuego += 1
    
    if turnos_para_fuego >= frecuencia:
        matriz = propagar_incendio(matriz, probabilidad=0.20)
        turnos_para_fuego = 0 # Reiniciar el contador
        
    return matriz