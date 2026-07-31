# main.py
import sys
import os

# Magia para que Python no se pierda con las carpetas
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

import pygame
from config import FILAS, COLUMNAS, FPS # Usamos tu config2

# Importes de DEV_2 (Tu trabajo gráfico)
from DEV_2.gestor_graficos import inicializar_pantalla, dibujar_laberinto, dibujar_jugador_completo, actualizar_pantalla
from DEV_2.gestor_eventos import procesar_inputs

# Importes de DEV_1 (El trabajo de tu compañero)
from DEV_1.nivel_manager import NivelManager
from DEV_1.jugador_logica import JugadorLogica

def main():
    pantalla = inicializar_pantalla()
    reloj = pygame.time.Clock()

    # --- 1. INICIALIZAR LÓGICA (DEV 1) ---
    nivel = NivelManager(FILAS, COLUMNAS)
    matriz_actual = nivel.generar_nuevo_nivel()
    jugador = JugadorLogica(1, 1) # Empieza en la celda 1,1

    # --- 2. VARIABLES DE ANIMACIÓN (DEV 2) ---
    indice_frame = 0
    temporizador_animacion = 0
    velocidad_animacion = 150 # ms por frame (bájalo si quieres que corra más rápido)
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
                # Dev 1 usa (fila, columna), así que pasamos (Y, X)
                se_movio = jugador.intentar_moverse(mov_y, mov_x, matriz_actual)
                
                if se_movio:
                    cooldown_mov = 150 # Espera 150ms antes del siguiente paso
                    # Cambiamos la animación si camina a los lados o arriba/abajo
                    if mov_x != 0: estado_animacion = 0 # Fila 1 (Lateral)
                    if mov_y != 0: estado_animacion = 1 # Fila 2 (Top-Down)
        else:
            cooldown_mov -= dt

        # --- 5. TUS DESASTRES SOBRENATURALES ---
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
        
        # Le pasamos la columna (X) y la fila (Y) al gestor de gráficos
        dibujar_jugador_completo(pantalla, jugador.columna, jugador.fila, indice_frame, estado_animacion)
        
        actualizar_pantalla()

    pygame.quit()

if __name__ == "__main__":
    main()