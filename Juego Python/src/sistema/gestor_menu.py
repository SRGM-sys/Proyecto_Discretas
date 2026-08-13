import pygame

from config import ANCHO_PANTALLA, ALTO_PANTALLA

from src.graficos.ui_estilo import (
    NARANJA,
    CIAN,
    BLANCO,
    GRIS,
    crear_fondo_atmosferico,
    cargar_logos,
    dibujar_panel,
    dibujar_esquinas_hud,
    crear_particulas,
    actualizar_particulas
)


def mostrar_menu(pantalla):

    reloj = pygame.time.Clock()

    fondo = crear_fondo_atmosferico()

    logo_feria, logo_espol = cargar_logos()

    particulas = crear_particulas(40)

    # =====================================================
    # FUENTES
    # =====================================================

    fuente_titulo = pygame.font.SysFont(
        "Bahnschrift",
        64,
        bold=True
    )

    fuente_subtitulo = pygame.font.SysFont(
        "Bahnschrift",
        39,
        bold=True
    )

    fuente_desafio = pygame.font.SysFont(
        "Bahnschrift",
        18,
        bold=True
    )

    fuente_boton = pygame.font.SysFont(
        "Bahnschrift",
        27,
        bold=True
    )

    fuente_texto = pygame.font.SysFont(
        "Bahnschrift",
        18
    )

    fuente_pequena = pygame.font.SysFont(
        "Bahnschrift",
        15
    )

    # =====================================================
    # BUCLE DEL MENÚ
    # =====================================================

    while True:

        dt = reloj.tick(60)

        # =================================================
        # EVENTOS
        # =================================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:
                    return True

                if evento.key == pygame.K_ESCAPE:
                    return False

        # =================================================
        # FONDO
        # =================================================

        pantalla.blit(
            fondo,
            (0, 0)
        )

        # =================================================
        # PARTÍCULAS / BRASAS
        # =================================================

        capa_particulas = pygame.Surface(
            (
                ANCHO_PANTALLA,
                ALTO_PANTALLA
            ),
            pygame.SRCALPHA
        )

        actualizar_particulas(
            capa_particulas,
            particulas,
            dt
        )

        pantalla.blit(
            capa_particulas,
            (0, 0)
        )

        # =================================================
        # LOGO FERIA DE CIENCIAS
        # =================================================

        if logo_feria:

            rect_feria = logo_feria.get_rect(
                center=(
                    ANCHO_PANTALLA // 2 - 115,
                    60
                )
            )

            pantalla.blit(
                logo_feria,
                rect_feria
            )

        # =================================================
        # LOGO ESPOL
        # Ya llega blanco desde ui_estilo.py
        # =================================================

        if logo_espol:

            rect_espol = logo_espol.get_rect(
                center=(
                    ANCHO_PANTALLA // 2 + 130,
                    60
                )
            )

            pantalla.blit(
                logo_espol,
                rect_espol
            )

        # =================================================
        # DIVISOR ENTRE LOGOS
        # =================================================

        pygame.draw.line(
            pantalla,
            (185, 193, 205),
            (
                ANCHO_PANTALLA // 2 + 10,
                32
            ),
            (
                ANCHO_PANTALLA // 2 + 10,
                90
            ),
            1
        )

        # =================================================
        # TÍTULO (CÓDIGO)
        # =================================================
        titulo_sombra = fuente_titulo.render(
            "CÓDIGO",
            True,
            (82, 32, 16)
        )
        titulo = fuente_titulo.render(
            "CÓDIGO",
            True,
            (238, 218, 190)
        )
        rect_titulo = titulo.get_rect(
            center=(
                ANCHO_PANTALLA // 2,
                175
            )
        )
        pantalla.blit(
            titulo_sombra,
            (
                rect_titulo.x + 4,
                rect_titulo.y + 5
            )
        )
        pantalla.blit(
            titulo,
            rect_titulo
        )

        # =================================================
        # SUBTÍTULO (DE ESCAPE)
        # =================================================
        subtitulo = fuente_subtitulo.render(
            "DE ESCAPE",
            True,
            CIAN
        )
        pantalla.blit(
            subtitulo,
            subtitulo.get_rect(
                center=(
                    ANCHO_PANTALLA // 2,
                    226
                )
            )
        )

        # =================================================
        # LÍNEAS DECORATIVAS
        # =================================================

        pygame.draw.line(
            pantalla,
            CIAN,
            (120, 260),
            (310, 260),
            2
        )

        pygame.draw.line(
            pantalla,
            NARANJA,
            (490, 260),
            (680, 260),
            2
        )

        pygame.draw.circle(
            pantalla,
            NARANJA,
            (
                ANCHO_PANTALLA // 2,
                260
            ),
            10,
            2
        )

        pygame.draw.circle(
            pantalla,
            CIAN,
            (
                ANCHO_PANTALLA // 2,
                260
            ),
            4
        )

        # =================================================
        # DESAFÍO DFS
        # =================================================

        rect_desafio = pygame.Rect(
            ANCHO_PANTALLA // 2 - 95,
            276,
            190,
            34
        )

        dibujar_panel(
            pantalla,
            rect_desafio,
            borde=NARANJA,
            relleno=(20, 16, 18, 220),
            grosor=1
        )

        texto_desafio = fuente_desafio.render(
            "DESAFÍO DFS",
            True,
            NARANJA
        )

        pantalla.blit(
            texto_desafio,
            texto_desafio.get_rect(
                center=rect_desafio.center
            )
        )

        # =================================================
        # BOTÓN INICIAR
        # =================================================

        rect_iniciar = pygame.Rect(
            ANCHO_PANTALLA // 2 - 170,
            330,
            340,
            75
        )

        dibujar_panel(
            pantalla,
            rect_iniciar,
            borde=NARANJA,
            relleno=(21, 18, 20, 225),
            grosor=2,
            glow=True
        )

        # Triángulo PLAY
        pygame.draw.polygon(
            pantalla,
            NARANJA,
            [
                (
                    rect_iniciar.x + 40,
                    rect_iniciar.centery - 15
                ),
                (
                    rect_iniciar.x + 40,
                    rect_iniciar.centery + 15
                ),
                (
                    rect_iniciar.x + 65,
                    rect_iniciar.centery
                )
            ]
        )

        texto_iniciar = fuente_boton.render(
            "INICIAR",
            True,
            BLANCO
        )

        pantalla.blit(
            texto_iniciar,
            texto_iniciar.get_rect(
                center=(
                    rect_iniciar.centerx + 25,
                    rect_iniciar.centery
                )
            )
        )

        # =================================================
        # PERSONAJES DISPONIBLES
        # =================================================

        rect_info = pygame.Rect(
            ANCHO_PANTALLA // 2 - 140,
            425,
            280,
            48
        )

        dibujar_panel(
            pantalla,
            rect_info,
            borde=CIAN,
            relleno=(13, 22, 34, 210),
            grosor=1
        )

        texto_info = fuente_pequena.render(
            "4 PERSONAJES DISPONIBLES",
            True,
            CIAN
        )

        pantalla.blit(
            texto_info,
            texto_info.get_rect(
                center=rect_info.center
            )
        )

        # =================================================
        # ENTER
        # =================================================

        texto_enter = fuente_texto.render(
            "ENTER  para comenzar",
            True,
            CIAN
        )

        pantalla.blit(
            texto_enter,
            texto_enter.get_rect(
                center=(
                    ANCHO_PANTALLA // 2,
                    510
                )
            )
        )

        # =================================================
        # ESC
        # =================================================

        texto_esc = fuente_texto.render(
            "ESC  para salir",
            True,
            GRIS
        )

        pantalla.blit(
            texto_esc,
            texto_esc.get_rect(
                center=(
                    ANCHO_PANTALLA // 2,
                    540
                )
            )
        )

        # =================================================
        # TEXTO INFERIOR IZQUIERDO
        # =================================================

        texto_izq = fuente_pequena.render(
            "Ciencia, ingenio y valentía.",
            True,
            (105, 198, 255)
        )

        pantalla.blit(
            texto_izq,
            (
                30,
                ALTO_PANTALLA - 32
            )
        )

        # =================================================
        # TEXTO INFERIOR DERECHO
        # =================================================

        texto_der = fuente_pequena.render(
            "Cada decisión cuenta.",
            True,
            (255, 153, 78)
        )

        pantalla.blit(
            texto_der,
            texto_der.get_rect(
                topright=(
                    ANCHO_PANTALLA - 30,
                    ALTO_PANTALLA - 32
                )
            )
        )

        # =================================================
        # ESQUINAS
        # =================================================

        dibujar_esquinas_hud(
            pantalla
        )

        # =================================================
        # ACTUALIZAR
        # =================================================

        pygame.display.flip()