import sys
import os
import random

ruta_raiz = os.path.dirname(os.path.abspath(__file__))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

import pygame
from config import FILAS, COLUMNAS, FPS, TAMANO_CELDA

# =========================================================
# GRAFICOS Y SISTEMA
# =========================================================
from src.graficos.gestor_graficos import (
    inicializar_pantalla,
    dibujar_laberinto,
    dibujar_jugador_completo,
    dibujar_hud,
    mostrar_pantalla_fin,
    actualizar_pantalla,
    establecer_personaje
)
from src.graficos.camara import Camara
from src.sistema.gestor_eventos import procesar_inputs
from src.sistema.gestor_menu import mostrar_menu
from src.sistema.selector_personajes import seleccionar_personaje
from src.sistema.lector_assets import inicializar_audio

# =========================================================
# CORE Y MAPA
# =========================================================
from src.core.jugador_logica import JugadorLogica
from src.core.cronometro import Cronometro
from src.mapa.generador_dfs import generar_laberinto, hacer_pasillos_anchos
from src.mapa.trampas import inyectar_obstaculos, inyectar_recargas
from src.mapa.incendio_logica import iniciar_fuego_seguro, actualizar_fuego_por_turnos

# =========================================================
# MAIN
# =========================================================
def main():
    pantalla = inicializar_pantalla()
    reloj = pygame.time.Clock()
    inicializar_audio()

    quiere_jugar = mostrar_menu(pantalla)
    if not quiere_jugar:
        pygame.quit()
        sys.exit()

    personaje_seleccionado = seleccionar_personaje(pantalla)
    if personaje_seleccionado is None:
        pygame.quit()
        sys.exit()

    establecer_personaje(personaje_seleccionado)
    print("Personaje elegido:", personaje_seleccionado["nombre"])

    jugando_partida = True
    while jugando_partida:
        camara = Camara()
        cronometro = Cronometro()
        cronometro.iniciar()

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

        temporizador_terremoto = 0
        tiempo_entre_terremotos = 12000
        terremoto_activo = False
        duracion_terremoto = 1500
        tiempo_actual_terremoto = 0
        
        # SISTEMA DE PARTÍCULAS DEL EXTINTOR
        particulas_extintor = []
        cooldown_extintor = 0

        corriendo = True
        while corriendo:
            dt = reloj.tick(FPS)
            
            # Ahora capturamos la 'accion' desde los inputs
            mov_x, mov_y, accion, salir = procesar_inputs()
            
            if salir:
                pygame.quit()
                sys.exit()

            # =============================================
            # LÓGICA DE MOVIMIENTO
            # =============================================
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
                
            # =============================================
            # LÓGICA DEL EXTINTOR (ESPACIO)
            # =============================================
            if cooldown_extintor > 0:
                cooldown_extintor -= dt
                
            if accion and cooldown_extintor <= 0 and jugador.carga_extintor > 0:
                celdas_afectadas = jugador.usar_extintor(matriz_actual)
                cooldown_extintor = 500 # Medio segundo entre disparos
                
                # Generar partículas en cada celda del área 3x2
                for f, c in celdas_afectadas:
                    px = c * TAMANO_CELDA + TAMANO_CELDA // 2
                    py = f * TAMANO_CELDA + TAMANO_CELDA // 2
                    for _ in range(8): # 8 burbujas por celda afectada
                        particulas_extintor.append({
                            "x": px + random.randint(-20, 20),
                            "y": py + random.randint(-20, 20),
                            "vx": random.uniform(-2, 2),
                            "vy": random.uniform(-2, 2),
                            "vida": 255 # Controla el canal Alpha (Transparencia)
                        })

            # =============================================
            # FIN DE PARTIDA
            # =============================================
            if not jugador.esta_vivo or jugador.ha_ganado:
                dibujar_laberinto(pantalla, matriz_actual, camara)
                dibujar_jugador_completo(pantalla, jugador.columna, jugador.fila, indice_frame, estado_animacion, camara, mirando_izquierda)
                actualizar_pantalla()
                quiere_reintentar = mostrar_pantalla_fin(pantalla, jugador.ha_ganado)
                corriendo = False
                if not quiere_reintentar:
                    jugando_partida = False
                break

            # =============================================
            # ANIMACIÓN Y ESTADOS
            # =============================================
            temporizador_animacion += dt
            if temporizador_animacion >= velocidad_animacion:
                indice_frame = (indice_frame + 1) % 4
                temporizador_animacion = 0

            estado_render = estado_animacion
            frame_render = indice_frame

            if matriz_actual[jugador.fila][jugador.columna] == 5:
                tiempo_en_fuego += dt
                if tiempo_en_fuego >= 2000:
                    estado_render = 2
                    frame_render = (indice_frame % 4)
            else:
                tiempo_en_fuego = 0

            if not terremoto_activo:
                temporizador_terremoto += dt
                if temporizador_terremoto >= tiempo_entre_terremotos:
                    terremoto_activo = True
                    temporizador_terremoto = 0
                    tiempo_actual_terremoto = 0
            else:
                tiempo_actual_terremoto += dt
                if tiempo_actual_terremoto >= duracion_terremoto:
                    terremoto_activo = False

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_1]: estado_animacion = 1
            elif teclas[pygame.K_2]: estado_animacion = 2
            elif teclas[pygame.K_3]: estado_animacion = 3

            jugador_px = jugador.columna * TAMANO_CELDA
            jugador_py = jugador.fila * TAMANO_CELDA
            camara.actualizar(jugador_px, jugador_py)

            if terremoto_activo:
                intensidad = 8
                camara.desplazamiento_x += random.randint(-intensidad, intensidad)
                camara.desplazamiento_y += random.randint(-intensidad, intensidad)

            # =============================================
            # RENDERIZADO PRINCIPAL
            # =============================================
            dibujar_laberinto(pantalla, matriz_actual, camara, indice_frame)
            dibujar_jugador_completo(pantalla, jugador.columna, jugador.fila, frame_render, estado_render, camara, mirando_izquierda)
            
            # Dibujar partículas del extintor
            for p in particulas_extintor[:]:
                p["x"] += p["vx"] * dt * 0.1
                p["y"] += p["vy"] * dt * 0.1
                p["vida"] -= dt * 0.6 # Velocidad de evaporación
                
                if p["vida"] <= 0:
                    particulas_extintor.remove(p)
                else:
                    x_render = int(p["x"] + camara.desplazamiento_x)
                    y_render = int(p["y"] + camara.desplazamiento_y)
                    
                    # Dibujar espuma cian con transparencia
                    superficie_p = pygame.Surface((16, 16), pygame.SRCALPHA)
                    alpha = max(0, min(255, int(p["vida"])))
                    pygame.draw.circle(superficie_p, (115, 246, 255, alpha), (8, 8), random.randint(4, 8))
                    pantalla.blit(superficie_p, (x_render - 8, y_render - 8))

            dibujar_hud(pantalla, jugador, cronometro)
            actualizar_pantalla()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()