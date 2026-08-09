import pygame

from config import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA
)

from DEV_2.personajes import PERSONAJES

from DEV_2.ui_estilo import (
    NARANJA,
    CIAN,
    CIAN_CLARO,
    BLANCO,
    crear_fondo_atmosferico,
    cargar_logos,
    dibujar_panel,
    dibujar_esquinas_hud,
    crear_particulas,
    actualizar_particulas
)


# =========================================================
# DETECTAR FILAS VISUALES
# =========================================================

def detectar_bandas_visuales(
    imagen,
    tolerancia=4,
    margen=5
):

    ancho, alto = imagen.get_size()

    filas_visibles = []

    for y in range(alto):

        franja = imagen.subsurface(
            (
                0,
                y,
                ancho,
                1
            )
        )

        if franja.get_bounding_rect(
            min_alpha=1
        ).width > 0:

            filas_visibles.append(y)


    if not filas_visibles:

        return []


    grupos = []

    inicio = filas_visibles[0]
    anterior = filas_visibles[0]


    for y in filas_visibles[1:]:

        if y <= anterior + tolerancia:

            anterior = y

        else:

            grupos.append(
                (
                    inicio,
                    anterior
                )
            )

            inicio = y
            anterior = y


    grupos.append(
        (
            inicio,
            anterior
        )
    )


    resultado = []

    for inicio, final in grupos:

        resultado.append(
            (
                max(
                    0,
                    inicio - margen
                ),

                min(
                    alto,
                    final + margen + 1
                )
            )
        )


    return resultado


# =========================================================
# OBTENER PREVIA DEL PERSONAJE
# =========================================================

def obtener_frame_previa(
    personaje
):

    try:

        hoja = pygame.image.load(
            personaje["sprite"]
        ).convert_alpha()


        columnas = personaje[
            "columnas"
        ]


        modo = personaje.get(
            "modo_corte",
            "rejilla"
        )


        # Usamos una pose frontal
        fila = 1
        columna = 0


        # =================================================
        # POU / PEPPA
        # =================================================

        if modo == "visual":

            bandas = detectar_bandas_visuales(
                hoja
            )


            if not bandas:

                raise ValueError(
                    "No se detectaron filas visuales"
                )


            if fila >= len(
                bandas
            ):

                fila = 0


            y0, y1 = bandas[
                fila
            ]


            ancho_columna = (
                hoja.get_width()
                // columnas
            )


            rect = pygame.Rect(
                columna * ancho_columna,
                y0,
                ancho_columna,
                y1 - y0
            )


        # =================================================
        # MINION / PRINCIPAL
        # =================================================

        else:

            filas = personaje[
                "filas"
            ]


            ancho_frame = (
                hoja.get_width()
                // columnas
            )


            alto_frame = (
                hoja.get_height()
                // filas
            )


            rect = pygame.Rect(
                columna * ancho_frame,
                fila * alto_frame,
                ancho_frame,
                alto_frame
            )


        # =================================================
        # EXTRAER FRAME
        # =================================================

        frame = hoja.subsurface(
            rect
        ).copy()


        visible = frame.get_bounding_rect(
            min_alpha=1
        )


        if (
            visible.width > 0
            and visible.height > 0
        ):

            frame = frame.subsurface(
                visible
            ).copy()


        # =================================================
        # ESCALAR SIN DEFORMAR
        # =================================================

        max_ancho = 120
        max_alto = 128


        ancho, alto = frame.get_size()


        escala = min(
            max_ancho / ancho,
            max_alto / alto
        )


        nuevo_ancho = max(
            1,
            int(
                ancho * escala
            )
        )


        nuevo_alto = max(
            1,
            int(
                alto * escala
            )
        )


        frame = pygame.transform.smoothscale(
            frame,
            (
                nuevo_ancho,
                nuevo_alto
            )
        )


        return frame


    except Exception as error:

        print(
            f"Error cargando previa de "
            f"{personaje['nombre']}: "
            f"{error}"
        )


        error_img = pygame.Surface(
            (
                100,
                120
            ),
            pygame.SRCALPHA
        )


        pygame.draw.rect(
            error_img,
            (
                70,
                75,
                90
            ),
            error_img.get_rect(),
            border_radius=12
        )


        fuente_error = pygame.font.SysFont(
            "Arial",
            50,
            bold=True
        )


        texto_error = fuente_error.render(
            "?",
            True,
            BLANCO
        )


        error_img.blit(
            texto_error,
            texto_error.get_rect(
                center=error_img.get_rect().center
            )
        )


        return error_img


# =========================================================
# SELECTOR DE PERSONAJES
# =========================================================

def seleccionar_personaje(
    pantalla
):

    reloj = pygame.time.Clock()


    # =====================================================
    # FONDO
    # =====================================================

    fondo = crear_fondo_atmosferico(
        semilla=19
    )


    # =====================================================
    # LOGOS
    # =====================================================

    logo_feria, logo_espol = cargar_logos()


    # =====================================================
    # PARTÍCULAS
    # =====================================================

    particulas = crear_particulas(
        28
    )


    # =====================================================
    # FUENTES
    # =====================================================

    fuente_titulo = pygame.font.SysFont(
        "Bahnschrift",
        39,
        bold=True
    )


    fuente_nombre = pygame.font.SysFont(
        "Bahnschrift",
        20,
        bold=True
    )


    fuente_chip = pygame.font.SysFont(
        "Bahnschrift",
        14,
        bold=True
    )


    fuente_instruccion = pygame.font.SysFont(
        "Bahnschrift",
        18
    )


    fuente_enter = pygame.font.SysFont(
        "Bahnschrift",
        20,
        bold=True
    )


    fuente_seleccion = pygame.font.SysFont(
        "Bahnschrift",
        16,
        bold=True
    )


    # =====================================================
    # PREVISUALIZACIONES
    # =====================================================

    imagenes = []

    for personaje in PERSONAJES:

        imagenes.append(
            obtener_frame_previa(
                personaje
            )
        )


    # Primer personaje seleccionado
    indice = 0


    # =====================================================
    # LOOP
    # =====================================================

    while True:

        dt = reloj.tick(
            60
        )


        # =================================================
        # EVENTOS
        # =================================================

        for evento in pygame.event.get():


            if evento.type == pygame.QUIT:

                return None


            if evento.type == pygame.KEYDOWN:


                # -----------------------------------------
                # IZQUIERDA
                # -----------------------------------------

                if evento.key in (
                    pygame.K_LEFT,
                    pygame.K_a
                ):

                    indice = (
                        indice - 1
                    ) % len(
                        PERSONAJES
                    )


                # -----------------------------------------
                # DERECHA
                # -----------------------------------------

                elif evento.key in (
                    pygame.K_RIGHT,
                    pygame.K_d
                ):

                    indice = (
                        indice + 1
                    ) % len(
                        PERSONAJES
                    )


                # -----------------------------------------
                # ENTER = CONFIRMAR
                # -----------------------------------------

                elif (
                    evento.key
                    == pygame.K_RETURN
                ):

                    return PERSONAJES[
                        indice
                    ]


                # -----------------------------------------
                # ESC = SALIR
                # -----------------------------------------

                elif (
                    evento.key
                    == pygame.K_ESCAPE
                ):

                    return None


        # =================================================
        # FONDO
        # =================================================

        pantalla.blit(
            fondo,
            (
                0,
                0
            )
        )


        # =================================================
        # PARTÍCULAS
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
            (
                0,
                0
            )
        )


        # =================================================
        # LOGO FERIA
        # =================================================

        if logo_feria:

            ancho_logo = 150


            alto_logo = int(
                logo_feria.get_height()
                * ancho_logo
                / logo_feria.get_width()
            )


            mini_feria = pygame.transform.smoothscale(
                logo_feria,
                (
                    ancho_logo,
                    alto_logo
                )
            )


            pantalla.blit(
                mini_feria,
                (
                    24,
                    18
                )
            )


        # =================================================
        # LOGO ESPOL
        # =================================================

        if logo_espol:

            ancho_logo = 112


            alto_logo = int(
                logo_espol.get_height()
                * ancho_logo
                / logo_espol.get_width()
            )


            mini_espol = pygame.transform.smoothscale(
                logo_espol,
                (
                    ancho_logo,
                    alto_logo
                )
            )


            rect_espol = mini_espol.get_rect(
                topright=(
                    ANCHO_PANTALLA - 24,
                    22
                )
            )


            pantalla.blit(
                mini_espol,
                rect_espol
            )


        # =================================================
        # TÍTULO
        # =================================================

        titulo_sombra = fuente_titulo.render(
            "SELECCIONA TU PERSONAJE",
            True,
            (
                75,
                33,
                20
            )
        )


        titulo = fuente_titulo.render(
            "SELECCIONA TU PERSONAJE",
            True,
            (
                238,
                209,
                180
            )
        )


        rect_titulo = titulo.get_rect(
            center=(
                ANCHO_PANTALLA // 2,
                105
            )
        )


        pantalla.blit(
            titulo_sombra,
            (
                rect_titulo.x + 3,
                rect_titulo.y + 3
            )
        )


        pantalla.blit(
            titulo,
            rect_titulo
        )


        # =================================================
        # LÍNEA DECORATIVA
        # =================================================

        pygame.draw.line(
            pantalla,
            CIAN,
            (
                220,
                136
            ),
            (
                580,
                136
            ),
            2
        )


        pygame.draw.circle(
            pantalla,
            NARANJA,
            (
                ANCHO_PANTALLA // 2,
                136
            ),
            6,
            2
        )


        # =================================================
        # CONFIGURACIÓN DE TARJETAS
        # =================================================

        ancho_tarjeta = 170
        alto_tarjeta = 282

        separacion = 18


        total = (
            len(PERSONAJES)
            * ancho_tarjeta
            +
            (
                len(PERSONAJES)
                - 1
            )
            * separacion
        )


        inicio_x = (
            ANCHO_PANTALLA
            - total
        ) // 2


        y_tarjeta = 160


        # =================================================
        # DIBUJAR PERSONAJES
        # =================================================

        for i, personaje in enumerate(
            PERSONAJES
        ):


            x = (
                inicio_x
                + i
                * (
                    ancho_tarjeta
                    + separacion
                )
            )


            rect = pygame.Rect(
                x,
                y_tarjeta,
                ancho_tarjeta,
                alto_tarjeta
            )


            seleccionado = (
                i == indice
            )


            # =============================================
            # COLORES DE LA TARJETA
            # =============================================

            if seleccionado:

                borde = NARANJA

                relleno = (
                    27,
                    20,
                    22,
                    230
                )

            else:

                borde = (
                    55,
                    145,
                    166
                )

                relleno = (
                    12,
                    23,
                    35,
                    220
                )


            # =============================================
            # PANEL
            # =============================================

            dibujar_panel(
                pantalla,
                rect,
                borde=borde,
                relleno=relleno,
                grosor=(
                    3
                    if seleccionado
                    else 1
                ),
                glow=seleccionado
            )


            # =============================================
            # RADAR DECORATIVO
            # =============================================

            centro = (
                rect.centerx,
                rect.y + 104
            )


            pygame.draw.circle(
                pantalla,
                borde,
                centro,
                60,
                1
            )


            pygame.draw.circle(
                pantalla,
                borde,
                centro,
                45,
                1
            )


            pygame.draw.line(
                pantalla,
                borde,
                (
                    centro[0] - 62,
                    centro[1]
                ),
                (
                    centro[0] + 62,
                    centro[1]
                ),
                1
            )


            pygame.draw.line(
                pantalla,
                borde,
                (
                    centro[0],
                    centro[1] - 62
                ),
                (
                    centro[0],
                    centro[1] + 62
                ),
                1
            )


            # =============================================
            # IMAGEN DEL PERSONAJE
            # =============================================

            imagen = imagenes[
                i
            ]


            pantalla.blit(
                imagen,
                imagen.get_rect(
                    center=centro
                )
            )


            # =============================================
            # NOMBRE
            # =============================================

            nombre = fuente_nombre.render(
                personaje[
                    "nombre"
                ],
                True,
                BLANCO
            )


            pantalla.blit(
                nombre,
                nombre.get_rect(
                    center=(
                        rect.centerx,
                        rect.y + 205
                    )
                )
            )


            # =============================================
            # BOTÓN ELEGIR / ELEGIDO
            # =============================================

            boton_estado = pygame.Rect(
                rect.x + 28,
                rect.y + 235,
                rect.width - 56,
                34
            )


            if seleccionado:

                color_fondo_boton = NARANJA

                color_borde_boton = (
                    255,
                    190,
                    120
                )

                color_texto_boton = (
                    25,
                    15,
                    12
                )

                texto_estado = (
                    "ELEGIDO"
                )

            else:

                color_fondo_boton = (
                    15,
                    38,
                    51
                )

                color_borde_boton = (
                    64,
                    166,
                    190
                )

                color_texto_boton = CIAN_CLARO

                texto_estado = (
                    "ELEGIR"
                )


            pygame.draw.rect(
                pantalla,
                color_fondo_boton,
                boton_estado,
                border_radius=7
            )


            pygame.draw.rect(
                pantalla,
                color_borde_boton,
                boton_estado,
                1,
                border_radius=7
            )


            texto_boton = fuente_chip.render(
                texto_estado,
                True,
                color_texto_boton
            )


            pantalla.blit(
                texto_boton,
                texto_boton.get_rect(
                    center=boton_estado.center
                )
            )


        # =================================================
        # PANEL DE CONTROLES
        # =================================================

        controles = pygame.Rect(
            188,
            468,
            424,
            92
        )


        dibujar_panel(
            pantalla,
            controles,
            borde=(
                65,
                92,
                110
            ),
            relleno=(
                8,
                14,
                24,
                225
            ),
            grosor=1
        )


        # =================================================
        # INSTRUCCIÓN
        # =================================================

        linea1 = fuente_instruccion.render(
            "A / D o flechas para elegir",
            True,
            (
                211,
                219,
                227
            )
        )


        pantalla.blit(
            linea1,
            linea1.get_rect(
                center=(
                    ANCHO_PANTALLA // 2,
                    493
                )
            )
        )


        # =================================================
        # ENTER PARA CONFIRMAR
        # =================================================

        texto_enter = fuente_enter.render(
            "ENTER",
            True,
            CIAN
        )


        texto_confirmar = fuente_instruccion.render(
            "para confirmar",
            True,
            CIAN
        )


        ancho_total = (
            texto_enter.get_width()
            + 14
            + texto_confirmar.get_width()
        )


        x_inicio = (
            ANCHO_PANTALLA // 2
            - ancho_total // 2
        )


        pantalla.blit(
            texto_enter,
            (
                x_inicio,
                525
            )
        )


        pantalla.blit(
            texto_confirmar,
            (
                x_inicio
                + texto_enter.get_width()
                + 14,
                527
            )
        )


        # =================================================
        # SELECCIONADO
        # =================================================

        texto_seleccion = fuente_seleccion.render(
            (
                "Seleccionado: "
                + PERSONAJES[
                    indice
                ][
                    "nombre"
                ]
            ),
            True,
            NARANJA
        )


        pantalla.blit(
            texto_seleccion,
            texto_seleccion.get_rect(
                center=(
                    ANCHO_PANTALLA // 2,
                    578
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