import sys
import os
import random

ruta_raiz = os.path.dirname(os.path.abspath(__file__))

if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

import pygame

from config import FILAS, COLUMNAS, FPS, TAMANO_CELDA

# =========================================================
# DEV_2
# =========================================================

from DEV_2.gestor_graficos import (
    inicializar_pantalla,
    dibujar_laberinto,
    dibujar_jugador_completo,
    dibujar_hud,
    mostrar_pantalla_fin,
    actualizar_pantalla,
    establecer_personaje
)

from DEV_2.gestor_eventos import procesar_inputs
from DEV_2.camara import Camara
from DEV_2.gestor_menu import mostrar_menu
from DEV_2.selector_personajes import seleccionar_personaje
from DEV_2.lector_assets import inicializar_audio


# =========================================================
# DEV_1
# =========================================================

from DEV_1.jugador_logica import JugadorLogica
from DEV_1.generador_dfs import generar_laberinto
from DEV_1.trampas import (
    inyectar_obstaculos,
    inyectar_recargas
)

from DEV_1.incendio_logica import (
    iniciar_fuego_seguro,
    actualizar_fuego_por_turnos
)

from DEV_1.cronometro import Cronometro


# =========================================================
# PASILLOS ANCHOS
# =========================================================

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


# =========================================================
# MAIN
# =========================================================

def main():

    # -----------------------------------------------------
    # INICIALIZACIÓN
    # -----------------------------------------------------

    pantalla = inicializar_pantalla()

    reloj = pygame.time.Clock()

    inicializar_audio()


    # =====================================================
    # MENÚ PRINCIPAL
    # =====================================================

    quiere_jugar = mostrar_menu(
        pantalla
    )

    if not quiere_jugar:

        pygame.quit()
        sys.exit()


    # =====================================================
    # SELECCIÓN DE PERSONAJE
    # =====================================================

    personaje_seleccionado = seleccionar_personaje(
        pantalla
    )

    if personaje_seleccionado is None:

        pygame.quit()
        sys.exit()


    # Cargar el sprite completo seleccionado
    establecer_personaje(
        personaje_seleccionado
    )

    print(
        "Personaje elegido:",
        personaje_seleccionado["nombre"]
    )


    # =====================================================
    # CICLO GENERAL
    # =====================================================

    jugando_partida = True

    while jugando_partida:

        # -------------------------------------------------
        # CÁMARA Y CRONÓMETRO
        # -------------------------------------------------

        camara = Camara()

        cronometro = Cronometro()

        cronometro.iniciar()


        # =================================================
        # GENERAR LABERINTO
        # =================================================

        matriz_actual = generar_laberinto(
            FILAS,
            COLUMNAS
        )

        matriz_actual = hacer_pasillos_anchos(
            matriz_actual
        )

        matriz_actual = inyectar_obstaculos(
            matriz_actual,
            5
        )

        matriz_actual = inyectar_recargas(
            matriz_actual,
            2
        )

        matriz_actual = iniciar_fuego_seguro(
            matriz_actual,
            2
        )


        # =================================================
        # JUGADOR
        # =================================================

        jugador = JugadorLogica(
            2,
            2
        )


        # =================================================
        # VARIABLES DE ANIMACIÓN
        # =================================================

        indice_frame = 0

        temporizador_animacion = 0

        velocidad_animacion = 150

        # 0 = lateral
        # 1 = frontal
        # 2 = fuego
        # 3 = agua
        estado_animacion = 1

        cooldown_mov = 0

        mirando_izquierda = False

        tiempo_en_fuego = 0


        # =================================================
        # TERREMOTO
        # =================================================

        temporizador_terremoto = 0

        tiempo_entre_terremotos = 12000

        terremoto_activo = False

        duracion_terremoto = 1500

        tiempo_actual_terremoto = 0


        # =================================================
        # BUCLE DE PARTIDA
        # =================================================

        corriendo = True

        while corriendo:

            dt = reloj.tick(
                FPS
            )


            # =============================================
            # INPUT
            # =============================================

            mov_x, mov_y, salir = procesar_inputs()

            if salir:

                pygame.quit()
                sys.exit()


            # =============================================
            # MOVIMIENTO
            # =============================================

            if cooldown_mov <= 0:

                if mov_x != 0 or mov_y != 0:

                    se_movio = jugador.intentar_moverse(
                        mov_y,
                        mov_x,
                        matriz_actual
                    )

                    if se_movio:

                        cooldown_mov = 150


                        # ---------------------------------
                        # MOVIMIENTO HORIZONTAL
                        # ---------------------------------

                        if mov_x != 0:

                            estado_animacion = 0

                            mirando_izquierda = (
                                mov_x < 0
                            )


                        # ---------------------------------
                        # MOVIMIENTO VERTICAL
                        # ---------------------------------

                        if mov_y != 0:

                            estado_animacion = 1


                        # ---------------------------------
                        # ACTUALIZAR INCENDIO
                        # ---------------------------------

                        matriz_actual = (
                            actualizar_fuego_por_turnos(
                                matriz_actual,
                                frecuencia=3
                            )
                        )

            else:

                cooldown_mov -= dt


            # =============================================
            # FIN DE PARTIDA
            # =============================================

            if (
                not jugador.esta_vivo
                or jugador.ha_ganado
            ):

                dibujar_laberinto(
                    pantalla,
                    matriz_actual,
                    camara
                )

                dibujar_jugador_completo(
                    pantalla,
                    jugador.columna,
                    jugador.fila,
                    indice_frame,
                    estado_animacion,
                    camara,
                    mirando_izquierda
                )

                actualizar_pantalla()


                quiere_reintentar = mostrar_pantalla_fin(
                    pantalla,
                    jugador.ha_ganado
                )

                corriendo = False


                # Si presiona ESC
                if not quiere_reintentar:

                    jugando_partida = False

                # Si presiona R:
                # vuelve a generar el laberinto
                # con EL MISMO personaje.

                break


            # =============================================
            # ANIMACIÓN
            # =============================================

            temporizador_animacion += dt

            if (
                temporizador_animacion
                >= velocidad_animacion
            ):

                indice_frame = (
                    indice_frame + 1
                ) % 4

                temporizador_animacion = 0


            # =============================================
            # ESTADO VISUAL
            # =============================================

            estado_render = estado_animacion

            frame_render = indice_frame


            # =============================================
            # PERSONAJE SOBRE EL FUEGO
            # =============================================

            if (
                matriz_actual[
                    jugador.fila
                ][
                    jugador.columna
                ]
                == 5
            ):

                tiempo_en_fuego += dt


                # Después de 2 segundos
                if tiempo_en_fuego >= 2000:

                    # Fila de fuego
                    estado_render = 2

                    frame_render = (
                        indice_frame % 4
                    )

            else:

                tiempo_en_fuego = 0


            # =============================================
            # TERREMOTO
            # =============================================

            if not terremoto_activo:

                temporizador_terremoto += dt

                if (
                    temporizador_terremoto
                    >= tiempo_entre_terremotos
                ):

                    terremoto_activo = True

                    temporizador_terremoto = 0

                    tiempo_actual_terremoto = 0

            else:

                tiempo_actual_terremoto += dt

                if (
                    tiempo_actual_terremoto
                    >= duracion_terremoto
                ):

                    terremoto_activo = False


            # =============================================
            # PRUEBAS MANUALES DE ANIMACIÓN
            # =============================================

            teclas = pygame.key.get_pressed()


            # Tecla 1 = animación frontal
            if teclas[pygame.K_1]:

                estado_animacion = 1


            # Tecla 2 = animación fuego
            elif teclas[pygame.K_2]:

                estado_animacion = 2


            # Tecla 3 = animación agua
            elif teclas[pygame.K_3]:

                estado_animacion = 3


            # =============================================
            # CÁMARA
            # =============================================

            jugador_px = (
                jugador.columna
                * TAMANO_CELDA
            )

            jugador_py = (
                jugador.fila
                * TAMANO_CELDA
            )

            camara.actualizar(
                jugador_px,
                jugador_py
            )


            # =============================================
            # SCREEN SHAKE
            # =============================================

            if terremoto_activo:

                intensidad = 8

                camara.desplazamiento_x += (
                    random.randint(
                        -intensidad,
                        intensidad
                    )
                )

                camara.desplazamiento_y += (
                    random.randint(
                        -intensidad,
                        intensidad
                    )
                )


            # =============================================
            # DIBUJAR
            # =============================================

            dibujar_laberinto(
                pantalla,
                matriz_actual,
                camara,
                indice_frame
            )

            dibujar_jugador_completo(
                pantalla,
                jugador.columna,
                jugador.fila,
                frame_render,
                estado_render,
                camara,
                mirando_izquierda
            )

            dibujar_hud(
                pantalla,
                jugador,
                cronometro
            )

            actualizar_pantalla()


    # =====================================================
    # CERRAR
    # =====================================================

    pygame.quit()

    sys.exit()


# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":
    main()