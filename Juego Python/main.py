# main.py
import sys
import os

ruta_raiz = os.path.dirname(os.path.abspath(__file__))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

import pygame
from config import FILAS, COLUMNAS, FPS 

# Importes de DEV_2 (Tu trabajo gráfico)
from DEV_2.gestor_graficos import inicializar_pantalla, dibujar_laberinto, dibujar_jugador_completo, actualizar_pantalla
from DEV_2.gestor_eventos import procesar_inputs

# Importes de DEV_1 (Llamamos a sus funciones buenas, ignoramos el manager roto)
from DEV_1.jugador_logica import JugadorLogica
from DEV_1.generador_dfs import generar_laberinto
from DEV_1.trampas import inyectar_obstaculos, inyectar_recargas
from DEV_1.incendio_logica import iniciar_fuego_seguro, actualizar_fuego_por_turnos

def main():
    pantalla = inicializar_pantalla()
    reloj = pygame.time.Clock()

    # --- 1. INICIALIZAR LÓGICA (Bypass de Dev 1) ---
    # Creamos el mapa paso a paso con las funciones que SÍ le funcionan a tu pana
    matriz_actual = generar_laberinto(FILAS, COLUMNAS)
    matriz_actual = inyectar_obstaculos(matriz_actual, 5)
    matriz_actual = inyectar_recargas(matriz_actual, 2)
    matriz_actual = iniciar_fuego_seguro(matriz_actual, 2)
    
    jugador = JugadorLogica(1, 1) # Empieza en la celda 1,1

    # --- 2. VARIABLES DE ANIMACIÓN (DEV 2) ---
    indice_frame = 0
    temporizador_animacion = 0
    velocidad_animacion = 150 # ms por frame
    estado_animacion = 1 # 1 = Top-Down normal (Fila 2)
    cooldown_mov = 0 

    corriendo = True
    while corriendo:
        dt = reloj.tick(FPS)

        # --- 3. CAPTURAR TECLAS ---
        mov_x, mov_y, salir = procesar_inputs()
        if salir:
            corriendo = False

        # --- 4. MOVER AL JUGADOR ---
        if cooldown_mov <= 0:
            if mov_x != 0 or mov_y != 0:
                se_movio = jugador.intentar_moverse(mov_y, mov_x, matriz_actual)
                
                if se_movio:
                    cooldown_mov = 150 
                    if mov_x != 0: estado_animacion = 0 # Lateral
                    if mov_y != 0: estado_animacion = 1 # Top-Down
                    
                    # Hacemos que el fuego crezca al moverse (lógica de Dev 1)
                    matriz_actual = actualizar_fuego_por_turnos(matriz_actual, frecuencia=3)
        else:
            cooldown_mov -= dt

        # --- 5. TUS DESASTRES SOBRENATURALES MANUALES ---
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_1]: estado_animacion = 1 # Normal
        elif teclas[pygame.K_2]: estado_animacion = 2 # Incendio! (Fila 3)
        elif teclas[pygame.K_3]: estado_animacion = 3 # Inundación! (Fila 4)

        # --- 6. AVANZAR LA ANIMACIÓN ---
        temporizador_animacion += dt
        if temporizador_animacion >= velocidad_animacion:
            indice_frame = (indice_frame + 1) % 4
            temporizador_animacion = 0

        # --- 7. DIBUJAR TODO ---
        dibujar_laberinto(pantalla, matriz_actual)
        dibujar_jugador_completo(pantalla, jugador.columna, jugador.fila, indice_frame, estado_animacion)
        
        actualizar_pantalla()

    pygame.quit()

if __name__ == "__main__":
    main()