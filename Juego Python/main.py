import sys
import os

ruta_raiz = os.path.dirname(os.path.abspath(__file__))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

import pygame
from config import FILAS, COLUMNAS, FPS, TAMANO_CELDA

# Importes tuyos (DEV_2)
from DEV_2.gestor_graficos import inicializar_pantalla, dibujar_laberinto, dibujar_jugador_completo, dibujar_hud, mostrar_pantalla_fin, actualizar_pantalla
from DEV_2.gestor_eventos import procesar_inputs
from DEV_2.camara import Camara
from DEV_2.gestor_menu import mostrar_menu
from DEV_2.lector_assets import inicializar_audio

# Importes de tu pana (DEV_1)
from DEV_1.jugador_logica import JugadorLogica
from DEV_1.generador_dfs import generar_laberinto
from DEV_1.trampas import inyectar_obstaculos, inyectar_recargas
from DEV_1.incendio_logica import iniciar_fuego_seguro, actualizar_fuego_por_turnos
from DEV_1.cronometro import Cronometro


# Bypass para hacer los pasillos anchos sin tocar DEV_1
def hacer_pasillos_anchos(matriz_original):
    matriz_ancha = []
    for fila in matriz_original:
        fila_doble = []
        for celda in fila:
            fila_doble.extend([celda, celda]) 
        matriz_ancha.append(fila_doble)
        matriz_ancha.append(list(fila_doble)) 
    return matriz_ancha

def main():
    pantalla = inicializar_pantalla()
    reloj = pygame.time.Clock()
    inicializar_audio()
    
    # Menú principal inicial
    quiere_jugar = mostrar_menu(pantalla)
    if not quiere_jugar:
        pygame.quit()
        sys.exit()

    jugando_partida = True
    while jugando_partida: # Ciclo general que mantiene vivo el programa al reiniciar
        camara = Camara()
        cronometro = Cronometro()
        cronometro.iniciar()

        # Generar mapa
        matriz_actual = generar_laberinto(FILAS, COLUMNAS)
        matriz_actual = hacer_pasillos_anchos(matriz_actual)
        matriz_actual = inyectar_obstaculos(matriz_actual, 5)
        matriz_actual = inyectar_recargas(matriz_actual, 2)
        matriz_actual = iniciar_fuego_seguro(matriz_actual, 2)
        
        jugador = JugadorLogica(2, 2) 

        indice_frame = 0
        temporizador_animacion = 0
        velocidad_animacion = 150 
        estado_animacion = 1 
        cooldown_mov = 0 
        mirando_izquierda = False
        tiempo_en_fuego = 0

        corriendo = True
        while corriendo:
            dt = reloj.tick(FPS)

            mov_x, mov_y, salir = procesar_inputs()
            if salir:
                pygame.quit()
                sys.exit()

            # Movimiento y lógica...
            if cooldown_mov <= 0:
                if mov_x != 0 or mov_y != 0:
                    se_movio = jugador.intentar_moverse(mov_y, mov_x, matriz_actual)
                    if se_movio:
                        cooldown_mov = 150 
                        if mov_x != 0: 
                            estado_animacion = 0 
                            mirando_izquierda = (mov_x < 0)
                        if mov_y != 0: 
                            estado_animacion = 1 
                        matriz_actual = actualizar_fuego_por_turnos(matriz_actual, frecuencia=3)
            else:
                cooldown_mov -= dt

            # Verificación de fin de partida
            if not jugador.esta_vivo or jugador.ha_ganado:
                dibujar_laberinto(pantalla, matriz_actual, camara)
                dibujar_jugador_completo(pantalla, jugador.columna, jugador.fila, indice_frame, estado_animacion, camara, mirando_izquierda)
                actualizar_pantalla()
                
                # Captura la decisión de la pantalla de fin
                quiere_reintentar = mostrar_pantalla_fin(pantalla, jugador.ha_ganado)
                
                corriendo = False # Rompe el bucle de la partida actual
                if not quiere_reintentar:
                    jugando_partida = False # Si dio ESC, rompe el ciclo general y cierra
                break

            
            # --- ANIMACIÓN GENERAL ---
            temporizador_animacion += dt
            if temporizador_animacion >= velocidad_animacion:
                indice_frame = (indice_frame + 1) % 4
                temporizador_animacion = 0

            # --- VERIFICAR TIEMPO EN EL FUEGO ---
            estado_render = estado_animacion
            frame_render = indice_frame
            
            # Revisamos si la chica está parada sobre una casilla de fuego (5)
            if matriz_actual[jugador.fila][jugador.columna] == 5:
                tiempo_en_fuego += dt # Sumamos el tiempo (dt está en milisegundos)
                
                if tiempo_en_fuego >= 2000: # Si pasan 2 segundos (2000 ms)
                    estado_render = 2 # Cambiamos a la Fila 3 de chica_pro.jpg (quemándose)
                    
                    # Con módulo 2 forzamos a que solo alterne entre los frames 0 y 1
                    frame_render = indice_frame % 2 
            else:
                tiempo_en_fuego = 0 # Si sale del fuego, se reinicia el contador al instante
            
            
            # Desastres manuales y renderizado normal...
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_1]: estado_animacion = 1 
            elif teclas[pygame.K_2]: estado_animacion = 2 
            elif teclas[pygame.K_3]: estado_animacion = 3 

            temporizador_animacion += dt
            if temporizador_animacion >= velocidad_animacion:
                indice_frame = (indice_frame + 1) % 4
                temporizador_animacion = 0

            jugador_px = jugador.columna * TAMANO_CELDA
            jugador_py = jugador.fila * TAMANO_CELDA
            camara.actualizar(jugador_px, jugador_py)

            dibujar_laberinto(pantalla, matriz_actual, camara, indice_frame)
            dibujar_jugador_completo(pantalla, jugador.columna, jugador.fila, frame_render, estado_render, camara, mirando_izquierda)
            dibujar_hud(pantalla, jugador, cronometro)
            
            actualizar_pantalla()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()