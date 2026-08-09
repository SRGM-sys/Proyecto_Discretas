# DEV_1/test_logica.py
import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DEV_1.generador_dfs import generar_laberinto
from DEV_1.trampas import inyectar_obstaculos, inyectar_recargas
from DEV_1.incendio_logica import iniciar_fuego_seguro, actualizar_fuego_por_turnos
from DEV_1.jugador_logica import JugadorLogica

FILAS, COLUMNAS = 15, 15

# Inicializar todo
matriz = generar_laberinto(FILAS, COLUMNAS)
matriz = inyectar_obstaculos(matriz, 5)
matriz = inyectar_recargas(matriz, 3)
matriz = iniciar_fuego_seguro(matriz, 2) 

# Buscar el punto de inicio aleatorio que definió el DFS
f_inicio, c_inicio = 1, 1
for f in range(FILAS):
    for c in range(COLUMNAS):
        if matriz[f][c] == 2:
            f_inicio, c_inicio = f, c
            break

# Aparecemos al jugador en las coordenadas dinámicas
jugador = JugadorLogica(f_inicio, c_inicio)

def dibujar(matriz, jugador):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"--- VIDA: {jugador.vida} HP | EXTINTOR: {'█ ' * jugador.carga_extintor}{'░ ' * (jugador.carga_maxima - jugador.carga_extintor)}---")
    for f in range(FILAS):
        fila_str = ""
        for c in range(COLUMNAS):
            if jugador.fila == f and jugador.columna == c:
                fila_str += "P "
            elif matriz[f][c] == 1: fila_str += "█ " # Pared
            elif matriz[f][c] == 0: fila_str += ". " # Camino
            elif matriz[f][c] == 3: fila_str += "M " # Meta
            elif matriz[f][c] == 4: fila_str += "O " # Obstáculo
            elif matriz[f][c] == 5: fila_str += "F " # Fuego
            elif matriz[f][c] == 6: fila_str += "+ " # Recarga Extintor
            else: fila_str += "  "
        print(fila_str)

# Inicializar todo
matriz = generar_laberinto(FILAS, COLUMNAS)
matriz = inyectar_obstaculos(matriz, 5)
matriz = inyectar_recargas(matriz, 3) # Colocamos 3 recargas en el mapa
matriz = iniciar_fuego_seguro(matriz, 2) 
jugador = JugadorLogica(1, 1)

while jugador.esta_vivo and not jugador.ha_ganado:
    dibujar(matriz, jugador)
    accion = input("\nMover (W/A/S/D), Esperar (E) o Salir (Q): ").upper()
    
    if accion == 'Q': break
    if accion == 'W': jugador.intentar_moverse(-1, 0, matriz)
    if accion == 'S': jugador.intentar_moverse(1, 0, matriz)
    if accion == 'A': jugador.intentar_moverse(0, -1, matriz)
    if accion == 'D': jugador.intentar_moverse(0, 1, matriz)
    
    matriz = actualizar_fuego_por_turnos(matriz, frecuencia=3)

if jugador.ha_ganado:
    print("\n¡Escapaste del edificio a tiempo!")
elif not jugador.esta_vivo:
    print("\n¡Moriste quemado! HP llegó a 0.")