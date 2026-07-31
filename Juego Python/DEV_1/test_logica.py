# DEV_1/test_bombero.py
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DEV_1.generador_dfs import generar_laberinto
from DEV_1.trampas import inyectar_obstaculos
from DEV_1.incendio_logica import iniciar_fuego, actualizar_fuego_por_turnos
from DEV_1.jugador_logica import JugadorLogica

FILAS, COLUMNAS = 15, 15

def dibujar(matriz, jugador):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"--- VIDA DEL JUGADOR: {jugador.vida} HP ---")
    for f in range(FILAS):
        fila_str = ""
        for c in range(COLUMNAS):
            if jugador.fila == f and jugador.columna == c:
                fila_str += "P "
            elif matriz[f][c] == 1: fila_str += "█ " # Pared
            elif matriz[f][c] == 0: fila_str += ". " # Camino
            elif matriz[f][c] == 3: fila_str += "M " # Meta
            elif matriz[f][c] == 4: fila_str += "O " # Obstáculo
            elif matriz[f][c] == 5: fila_str += "F " # FUEGO
            else: fila_str += "  "
        print(fila_str)

# Inicializar todo
matriz = generar_laberinto(FILAS, COLUMNAS)
matriz = inyectar_obstaculos(matriz, 5)
matriz = iniciar_fuego(matriz, 2) # Empezamos con 2 focos de incendio
jugador = JugadorLogica(1, 1)

while jugador.esta_vivo and not jugador.ha_ganado:
    dibujar(matriz, jugador)
    accion = input("\nMover (W/A/S/D), Esperar (E) o Salir (Q): ").upper()
    
    if accion == 'Q': break
    if accion == 'W': jugador.intentar_moverse(-1, 0, matriz)
    if accion == 'S': jugador.intentar_moverse(1, 0, matriz)
    if accion == 'A': jugador.intentar_moverse(0, -1, matriz)
    if accion == 'D': jugador.intentar_moverse(0, 1, matriz)
    
    # Reemplaza la línea vieja por esta nueva:
    matriz = actualizar_fuego_por_turnos(matriz, frecuencia=3)

if jugador.ha_ganado:
    print("\n¡Escapaste del edificio a tiempo!")
elif not jugador.esta_vivo:
    print("\n¡Moriste quemado! HP llegó a 0.")