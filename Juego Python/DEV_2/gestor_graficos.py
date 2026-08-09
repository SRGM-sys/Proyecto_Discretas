import math
import os
import random
import pygame

from config import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    TAMANO_CELDA,
    VERDE_JUGADOR,
    GRIS_PARED,
    ROJO_FUEGO,
)

from DEV_2.ui_estilo import (
    NARANJA,
    NARANJA_CLARO,
    CIAN,
    CIAN_CLARO,
    BLANCO,
    GRIS,
    crear_fondo_atmosferico,
    cargar_logos,
    dibujar_panel,
    dibujar_esquinas_hud,
)


# =========================================================
# VARIABLES GLOBALES
# =========================================================

HOJA_JUGADOR_PRO = []
HOJA_FUEGO = []

IMAGEN_MURO = None
TILE_PISO = None
FONDO_JUEGO = None

GLOW_FUEGO = None
GLOW_CIAN = None
GLOW_META = None

NOMBRE_PERSONAJE_ACTUAL = "Principal"


# =========================================================
# RUTA PRINCIPAL
# =========================================================

def ruta_raiz():

    return os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )


# =========================================================
# CREAR RESPLANDOR
# =========================================================

def crear_glow(
    tamano,
    color
):

    superficie = pygame.Surface(
        (
            tamano,
            tamano
        ),
        pygame.SRCALPHA
    )

    centro = tamano // 2

    radio_max = tamano // 2


    for radio in range(
        radio_max,
        2,
        -4
    ):

        factor = (
            1
            - radio / radio_max
        )

        alpha = int(
            7
            + 28 * factor
        )


        pygame.draw.circle(
            superficie,
            (
                *color,
                alpha
            ),
            (
                centro,
                centro
            ),
            radio
        )


    return superficie


# =========================================================
# CREAR PISO
# =========================================================

def crear_tile_piso():

    tile = pygame.Surface(
        (
            TAMANO_CELDA,
            TAMANO_CELDA
        )
    ).convert()


    # Fondo oscuro
    tile.fill(
        (
            12,
            18,
            32
        )
    )


    # Borde de la placa
    pygame.draw.rect(
        tile,
        (
            17,
            25,
            42
        ),
        (
            0,
            0,
            TAMANO_CELDA,
            TAMANO_CELDA
        ),
        1
    )


    # Línea inferior
    pygame.draw.line(
        tile,
        (
            25,
            40,
            58
        ),
        (
            0,
            TAMANO_CELDA - 2
        ),
        (
            TAMANO_CELDA,
            TAMANO_CELDA - 2
        ),
        1
    )


    # Línea lateral
    pygame.draw.line(
        tile,
        (
            20,
            33,
            48
        ),
        (
            TAMANO_CELDA - 2,
            0
        ),
        (
            TAMANO_CELDA - 2,
            TAMANO_CELDA
        ),
        1
    )


    # Detalles pequeños
    rng = random.Random(
        8
    )


    for _ in range(
        9
    ):

        x = rng.randrange(
            5,
            TAMANO_CELDA - 5
        )

        y = rng.randrange(
            5,
            TAMANO_CELDA - 5
        )


        color = rng.choice(
            [
                (
                    30,
                    48,
                    66
                ),

                (
                    25,
                    35,
                    53
                ),

                (
                    27,
                    57,
                    70
                )
            ]
        )


        pygame.draw.circle(
            tile,
            color,
            (
                x,
                y
            ),
            1
        )


    return tile


# =========================================================
# INICIALIZAR PANTALLA
# =========================================================

def inicializar_pantalla():

    global HOJA_JUGADOR_PRO
    global HOJA_FUEGO
    global IMAGEN_MURO

    global TILE_PISO
    global FONDO_JUEGO

    global GLOW_FUEGO
    global GLOW_CIAN
    global GLOW_META


    pygame.init()


    pantalla = pygame.display.set_mode(
        (
            ANCHO_PANTALLA,
            ALTO_PANTALLA
        )
    )


    pygame.display.set_caption(
        "Laberinto Sobrenatural Pro"
    )


    # =====================================================
    # ELEMENTOS VISUALES
    # =====================================================

    TILE_PISO = crear_tile_piso()


    FONDO_JUEGO = crear_fondo_atmosferico(
        semilla=43
    )


    GLOW_FUEGO = crear_glow(
        110,
        (
            255,
            70,
            15
        )
    )


    GLOW_CIAN = crear_glow(
        100,
        CIAN
    )


    GLOW_META = crear_glow(
        120,
        (
            255,
            196,
            38
        )
    )


    raiz = ruta_raiz()


    # =====================================================
    # PRINCIPAL POR DEFECTO
    # =====================================================

    ruta_principal = os.path.join(
        raiz,
        "assets",
        "sprites",
        "chica_pro.png"
    )


    try:

        HOJA_JUGADOR_PRO = (
            cargar_personaje_rejilla(
                ruta_principal,
                4,
                4,
                [
                    0,
                    1,
                    2,
                    3
                ]
            )
        )

    except Exception as error:

        print(
            f"No se pudo cargar Principal: "
            f"{error}"
        )

        HOJA_JUGADOR_PRO = (
            crear_sprite_emergencia()
        )


    # =====================================================
    # MURO
    # =====================================================

    ruta_muro = os.path.join(
        raiz,
        "assets",
        "sprites",
        "muro.jpg"
    )


    try:

        muro = pygame.image.load(
            ruta_muro
        ).convert()


        muro = pygame.transform.smoothscale(
            muro,
            (
                TAMANO_CELDA,
                TAMANO_CELDA
            )
        )


        # Tinte azul/gris
        tinte = pygame.Surface(
            (
                TAMANO_CELDA,
                TAMANO_CELDA
            )
        ).convert()


        tinte.fill(
            (
                132,
                150,
                180
            )
        )


        muro.blit(
            tinte,
            (
                0,
                0
            ),
            special_flags=pygame.BLEND_MULT
        )


        IMAGEN_MURO = muro


    except Exception as error:

        print(
            f"No se pudo cargar muro: "
            f"{error}"
        )

        IMAGEN_MURO = None


    # =====================================================
    # FUEGO
    # =====================================================

    ruta_fuego = os.path.join(
        raiz,
        "assets",
        "sprites",
        "fuego.jpg"
    )


    try:

        HOJA_FUEGO = cargar_sprite_sheet(
            ruta_fuego,
            1,
            4
        )


    except Exception as error:

        print(
            f"No se pudo cargar fuego: "
            f"{error}"
        )


        cuadro = pygame.Surface(
            (
                TAMANO_CELDA,
                TAMANO_CELDA
            ),
            pygame.SRCALPHA
        )


        pygame.draw.circle(
            cuadro,
            ROJO_FUEGO,
            (
                TAMANO_CELDA // 2,
                TAMANO_CELDA // 2
            ),
            20
        )


        HOJA_FUEGO = [

            cuadro.copy()

            for _ in range(
                4
            )
        ]


    return pantalla


# =========================================================
# DETECTAR FILAS VISUALES
# =========================================================

def detectar_filas_visuales(
    imagen,
    tolerancia=4,
    margen=6
):

    ancho, alto = (
        imagen.get_size()
    )


    filas_visibles = []


    for y in range(
        alto
    ):

        franja = imagen.subsurface(
            (
                0,
                y,
                ancho,
                1
            )
        )


        if (
            franja.get_bounding_rect(
                min_alpha=1
            ).width > 0
        ):

            filas_visibles.append(
                y
            )


    if not filas_visibles:

        return []


    grupos = []


    inicio = (
        filas_visibles[0]
    )

    anterior = (
        filas_visibles[0]
    )


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


    return [

        (
            max(
                0,
                ini - margen
            ),

            min(
                alto,
                fin + margen + 1
            )
        )

        for ini, fin in grupos
    ]


# =========================================================
# ADAPTAR PERSONAJE A CELDA
# =========================================================

def adaptar_personaje_a_celda(
    frame
):

    tamano_canvas = (
        TAMANO_CELDA - 8
    )


    visible = frame.get_bounding_rect(
        min_alpha=1
    )


    if (
        visible.width == 0
        or visible.height == 0
    ):

        return pygame.Surface(
            (
                tamano_canvas,
                tamano_canvas
            ),
            pygame.SRCALPHA
        )


    personaje = frame.subsurface(
        visible
    ).copy()


    ancho, alto = (
        personaje.get_size()
    )


    escala = min(
        tamano_canvas / ancho,
        tamano_canvas / alto
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


    personaje = pygame.transform.smoothscale(
        personaje,
        (
            nuevo_ancho,
            nuevo_alto
        )
    )


    canvas = pygame.Surface(
        (
            tamano_canvas,
            tamano_canvas
        ),
        pygame.SRCALPHA
    )


    x = (
        tamano_canvas
        - nuevo_ancho
    ) // 2


    y = (
        tamano_canvas
        - nuevo_alto
    )


    canvas.blit(
        personaje,
        (
            x,
            y
        )
    )


    return canvas


# =========================================================
# CARGAR SPRITE EN REJILLA
# =========================================================

def cargar_personaje_rejilla(
    ruta_archivo,
    filas,
    columnas,
    filas_usadas
):

    hoja = pygame.image.load(
        ruta_archivo
    ).convert_alpha()


    ancho_frame = (
        hoja.get_width()
        // columnas
    )


    alto_frame = (
        hoja.get_height()
        // filas
    )


    frames = []


    for fila in filas_usadas:

        for columna in range(
            columnas
        ):

            rect = pygame.Rect(
                columna * ancho_frame,
                fila * alto_frame,
                ancho_frame,
                alto_frame
            )


            frame = pygame.Surface(
                (
                    ancho_frame,
                    alto_frame
                ),
                pygame.SRCALPHA
            )


            frame.blit(
                hoja,
                (
                    0,
                    0
                ),
                rect
            )


            frames.append(
                adaptar_personaje_a_celda(
                    frame
                )
            )


    return frames


# =========================================================
# CARGAR SPRITE VISUAL
# =========================================================

def cargar_personaje_visual(
    ruta_archivo,
    columnas,
    filas_usadas
):

    hoja = pygame.image.load(
        ruta_archivo
    ).convert_alpha()


    bandas = detectar_filas_visuales(
        hoja
    )


    ancho_columna = (
        hoja.get_width()
        // columnas
    )


    frames = []


    for fila in filas_usadas:

        if fila >= len(
            bandas
        ):

            raise ValueError(
                f"No existe la fila visual "
                f"{fila} en "
                f"{os.path.basename(ruta_archivo)}"
            )


        y0, y1 = bandas[
            fila
        ]


        alto_fila = (
            y1 - y0
        )


        for columna in range(
            columnas
        ):

            rect = pygame.Rect(
                columna * ancho_columna,
                y0,
                ancho_columna,
                alto_fila
            )


            frame = pygame.Surface(
                (
                    ancho_columna,
                    alto_fila
                ),
                pygame.SRCALPHA
            )


            frame.blit(
                hoja,
                (
                    0,
                    0
                ),
                rect
            )


            frames.append(
                adaptar_personaje_a_celda(
                    frame
                )
            )


    return frames


# =========================================================
# ESTABLECER PERSONAJE
# =========================================================

def establecer_personaje(
    personaje
):

    global HOJA_JUGADOR_PRO
    global NOMBRE_PERSONAJE_ACTUAL


    try:

        if (
            personaje.get(
                "modo_corte"
            )
            == "visual"
        ):

            frames = cargar_personaje_visual(
                personaje[
                    "sprite"
                ],

                personaje[
                    "columnas"
                ],

                personaje[
                    "filas_usadas"
                ]
            )


        else:

            frames = cargar_personaje_rejilla(
                personaje[
                    "sprite"
                ],

                personaje[
                    "filas"
                ],

                personaje[
                    "columnas"
                ],

                personaje[
                    "filas_usadas"
                ]
            )


        if len(frames) != 16:

            raise ValueError(
                f"Se esperaban 16 frames "
                f"y se obtuvieron "
                f"{len(frames)}"
            )


        HOJA_JUGADOR_PRO = frames


        NOMBRE_PERSONAJE_ACTUAL = (
            personaje[
                "nombre"
            ]
        )


        print(
            f"Personaje cargado: "
            f"{NOMBRE_PERSONAJE_ACTUAL}"
        )


    except Exception as error:

        print(
            f"Error cargando "
            f"{personaje['nombre']}: "
            f"{error}"
        )


        HOJA_JUGADOR_PRO = (
            crear_sprite_emergencia()
        )


        NOMBRE_PERSONAJE_ACTUAL = (
            personaje[
                "nombre"
            ]
        )


# =========================================================
# SPRITE EMERGENCIA
# =========================================================

def crear_sprite_emergencia():

    tam = (
        TAMANO_CELDA - 8
    )


    cuadro = pygame.Surface(
        (
            tam,
            tam
        ),
        pygame.SRCALPHA
    )


    pygame.draw.circle(
        cuadro,
        VERDE_JUGADOR,
        (
            tam // 2,
            tam // 2
        ),
        tam // 3
    )


    return [

        cuadro.copy()

        for _ in range(
            16
        )
    ]


# =========================================================
# CARGAR SPRITE SHEET NORMAL
# =========================================================

def cargar_sprite_sheet(
    ruta_archivo,
    filas,
    columnas
):

    hoja = pygame.image.load(
        ruta_archivo
    ).convert_alpha()


    ancho_frame = (
        hoja.get_width()
        // columnas
    )


    alto_frame = (
        hoja.get_height()
        // filas
    )


    frames = []


    for fila in range(
        filas
    ):

        for columna in range(
            columnas
        ):

            rect = pygame.Rect(
                columna * ancho_frame,
                fila * alto_frame,
                ancho_frame,
                alto_frame
            )


            frame = pygame.Surface(
                (
                    ancho_frame,
                    alto_frame
                ),
                pygame.SRCALPHA
            )


            frame.blit(
                hoja,
                (
                    0,
                    0
                ),
                rect
            )


            frame = pygame.transform.smoothscale(
                frame,
                (
                    TAMANO_CELDA,
                    TAMANO_CELDA
                )
            )


            frames.append(
                frame
            )


    return frames


# =========================================================
# RANGO VISIBLE
# =========================================================

def rango_visible(
    matriz,
    camara
):

    filas = len(
        matriz
    )


    columnas = len(
        matriz[0]
    )


    col_inicio = max(
        0,
        int(
            (
                -camara.desplazamiento_x
            )
            // TAMANO_CELDA
        ) - 2
    )


    col_fin = min(
        columnas,
        int(
            (
                ANCHO_PANTALLA
                - camara.desplazamiento_x
            )
            // TAMANO_CELDA
        ) + 3
    )


    fila_inicio = max(
        0,
        int(
            (
                -camara.desplazamiento_y
            )
            // TAMANO_CELDA
        ) - 2
    )


    fila_fin = min(
        filas,
        int(
            (
                ALTO_PANTALLA
                - camara.desplazamiento_y
            )
            // TAMANO_CELDA
        ) + 3
    )


    return (
        fila_inicio,
        fila_fin,
        col_inicio,
        col_fin
    )


# =========================================================
# DIBUJAR LABERINTO
# =========================================================

def dibujar_laberinto(
    pantalla,
    matriz,
    camara,
    frame_fuego=0
):

    # =====================================================
    # FONDO ATMOSFÉRICO
    # =====================================================

    if FONDO_JUEGO:

        pantalla.blit(
            FONDO_JUEGO,
            (
                0,
                0
            )
        )

    else:

        pantalla.fill(
            (
                7,
                11,
                20
            )
        )


    # =====================================================
    # CAPA OSCURA
    # =====================================================

    capa = pygame.Surface(
        (
            ANCHO_PANTALLA,
            ALTO_PANTALLA
        ),
        pygame.SRCALPHA
    )


    capa.fill(
        (
            1,
            4,
            11,
            90
        )
    )


    pantalla.blit(
        capa,
        (
            0,
            0
        )
    )


    # =====================================================
    # CELDAS VISIBLES
    # =====================================================

    (
        fila_inicio,
        fila_fin,
        col_inicio,
        col_fin
    ) = rango_visible(
        matriz,
        camara
    )


    tiempo = (
        pygame.time.get_ticks()
    )


    pulso = (
        0.5
        + 0.5
        * math.sin(
            tiempo / 260.0
        )
    )


    for fila in range(
        fila_inicio,
        fila_fin
    ):

        for columna in range(
            col_inicio,
            col_fin
        ):

            valor = matriz[
                fila
            ][
                columna
            ]


            x = (
                columna
                * TAMANO_CELDA
                + camara.desplazamiento_x
            )


            y = (
                fila
                * TAMANO_CELDA
                + camara.desplazamiento_y
            )


            rect = pygame.Rect(
                x,
                y,
                TAMANO_CELDA,
                TAMANO_CELDA
            )


            # =================================================
            # PARED
            # =================================================

            if valor == 1:

                if IMAGEN_MURO:

                    pantalla.blit(
                        IMAGEN_MURO,
                        (
                            x,
                            y
                        )
                    )


                    pygame.draw.rect(
                        pantalla,
                        (
                            34,
                            48,
                            68
                        ),
                        rect,
                        1
                    )


                    pygame.draw.line(
                        pantalla,
                        (
                            80,
                            105,
                            140
                        ),
                        (
                            x + 2,
                            y + 2
                        ),
                        (
                            x
                            + TAMANO_CELDA
                            - 2,
                            y + 2
                        ),
                        1
                    )

                else:

                    pygame.draw.rect(
                        pantalla,
                        GRIS_PARED,
                        rect
                    )


                continue


            # =================================================
            # PISO
            # =================================================

            if TILE_PISO:

                pantalla.blit(
                    TILE_PISO,
                    (
                        x,
                        y
                    )
                )

            else:

                pygame.draw.rect(
                    pantalla,
                    (
                        12,
                        18,
                        32
                    ),
                    rect
                )


            # =================================================
            # INICIO
            # =================================================

            if valor == 2:

                pygame.draw.circle(
                    pantalla,
                    (
                        35,
                        102,
                        117
                    ),
                    rect.center,
                    13,
                    2
                )


                pygame.draw.circle(
                    pantalla,
                    CIAN,
                    rect.center,
                    4
                )


            # =================================================
            # META / PORTAL
            # =================================================

            elif valor == 3:

                glow = (
                    GLOW_META.copy()
                )


                glow.set_alpha(
                    int(
                        135
                        + 80
                        * pulso
                    )
                )


                pantalla.blit(
                    glow,
                    glow.get_rect(
                        center=rect.center
                    )
                )


                portal = rect.inflate(
                    -18,
                    -18
                )


                pygame.draw.rect(
                    pantalla,
                    (
                        255,
                        192,
                        35
                    ),
                    portal,
                    border_radius=9
                )


                pygame.draw.rect(
                    pantalla,
                    (
                        255,
                        244,
                        170
                    ),
                    portal,
                    2,
                    border_radius=9
                )


                pygame.draw.circle(
                    pantalla,
                    (
                        93,
                        48,
                        18
                    ),
                    portal.center,
                    11,
                    3
                )


                pygame.draw.circle(
                    pantalla,
                    (
                        255,
                        234,
                        119
                    ),
                    portal.center,
                    4
                )


            # =================================================
            # OBSTÁCULO
            # =================================================

            elif valor == 4:

                bloque = rect.inflate(
                    -12,
                    -12
                )


                pygame.draw.rect(
                    pantalla,
                    (
                        78,
                        25,
                        30
                    ),
                    bloque,
                    border_radius=8
                )


                pygame.draw.rect(
                    pantalla,
                    (
                        220,
                        73,
                        56
                    ),
                    bloque,
                    2,
                    border_radius=8
                )


                pygame.draw.line(
                    pantalla,
                    (
                        255,
                        136,
                        69
                    ),
                    bloque.topleft,
                    bloque.bottomright,
                    3
                )


                pygame.draw.line(
                    pantalla,
                    (
                        255,
                        136,
                        69
                    ),
                    bloque.topright,
                    bloque.bottomleft,
                    3
                )


            # =================================================
            # FUEGO
            # =================================================

            elif valor == 5:

                if GLOW_FUEGO:

                    pantalla.blit(
                        GLOW_FUEGO,
                        GLOW_FUEGO.get_rect(
                            center=rect.center
                        )
                    )


                if HOJA_FUEGO:

                    pantalla.blit(
                        HOJA_FUEGO[
                            frame_fuego
                            % len(
                                HOJA_FUEGO
                            )
                        ],
                        (
                            x,
                            y
                        )
                    )


            # =================================================
            # EXTINTOR
            # =================================================

            elif valor == 6:

                if GLOW_CIAN:

                    pantalla.blit(
                        GLOW_CIAN,
                        GLOW_CIAN.get_rect(
                            center=rect.center
                        )
                    )


                cuerpo = pygame.Rect(
                    x + 20,
                    y + 14,
                    24,
                    36
                )


                pygame.draw.rect(
                    pantalla,
                    (
                        18,
                        91,
                        111
                    ),
                    cuerpo,
                    border_radius=6
                )


                pygame.draw.rect(
                    pantalla,
                    CIAN_CLARO,
                    cuerpo,
                    2,
                    border_radius=6
                )


                # Signo +
                pygame.draw.rect(
                    pantalla,
                    BLANCO,
                    (
                        x + 30,
                        y + 22,
                        4,
                        20
                    ),
                    border_radius=2
                )


                pygame.draw.rect(
                    pantalla,
                    BLANCO,
                    (
                        x + 22,
                        y + 30,
                        20,
                        4
                    ),
                    border_radius=2
                )


# =========================================================
# DIBUJAR PERSONAJE
# =========================================================

def dibujar_jugador_completo(
    pantalla,
    logica_x,
    logica_y,
    frame_actual,
    tipo_animacion,
    camara,
    flip_x=False
):

    mundo_x = (
        logica_x
        * TAMANO_CELDA
        + 4
    )


    mundo_y = (
        logica_y
        * TAMANO_CELDA
        + 4
    )


    x = (
        mundo_x
        + camara.desplazamiento_x
    )


    y = (
        mundo_y
        + camara.desplazamiento_y
    )


    # =====================================================
    # SOMBRA
    # =====================================================

    sombra = pygame.Surface(
        (
            48,
            18
        ),
        pygame.SRCALPHA
    )


    pygame.draw.ellipse(
        sombra,
        (
            0,
            0,
            0,
            100
        ),
        sombra.get_rect()
    )


    pantalla.blit(
        sombra,
        (
            x + 4,
            y
            + TAMANO_CELDA
            - 19
        )
    )


    # =====================================================
    # FRAME
    # =====================================================

    indice_base = (
        tipo_animacion
        % 4
    ) * 4


    indice = (
        indice_base
        + (
            frame_actual
            % 4
        )
    )


    sprite = (
        HOJA_JUGADOR_PRO[
            indice
        ]
    )


    if (
        flip_x
        and tipo_animacion == 0
    ):

        sprite = pygame.transform.flip(
            sprite,
            True,
            False
        )


    pantalla.blit(
        sprite,
        (
            x,
            y
        )
    )


# =========================================================
# BARRA HUD
# =========================================================

def dibujar_barra(
    pantalla,
    rect,
    proporcion,
    color,
    color_fondo=(
        32,
        39,
        49
    )
):

    pygame.draw.rect(
        pantalla,
        color_fondo,
        rect,
        border_radius=5
    )


    relleno = rect.copy()


    relleno.width = max(
        0,
        int(
            rect.width
            * max(
                0,
                min(
                    1,
                    proporcion
                )
            )
        )
    )


    if relleno.width > 0:

        pygame.draw.rect(
            pantalla,
            color,
            relleno,
            border_radius=5
        )


    pygame.draw.rect(
        pantalla,
        (
            115,
            130,
            146
        ),
        rect,
        1,
        border_radius=5
    )


# =========================================================
# HUD
# =========================================================

def dibujar_hud(
    pantalla,
    jugador,
    cronometro
):

    fuente_titulo = pygame.font.SysFont(
        "Bahnschrift",
        14,
        bold=True
    )


    fuente_valor = pygame.font.SysFont(
        "Bahnschrift",
        19,
        bold=True
    )


    fuente_pequena = pygame.font.SysFont(
        "Bahnschrift",
        12,
        bold=True
    )


    # =====================================================
    # VIDA
    # =====================================================

    vida_panel = pygame.Rect(
        18,
        18,
        230,
        68
    )


    dibujar_panel(
        pantalla,
        vida_panel,
        borde=(
            218,
            68,
            56
        ),
        relleno=(
            8,
            13,
            23,
            225
        ),
        grosor=1
    )


    pantalla.blit(
        fuente_titulo.render(
            "VIDA",
            True,
            (
                255,
                111,
                93
            )
        ),
        (
            32,
            28
        )
    )


    pantalla.blit(
        fuente_valor.render(
            f"{jugador.vida} HP",
            True,
            BLANCO
        ),
        (
            80,
            24
        )
    )


    dibujar_barra(
        pantalla,
        pygame.Rect(
            32,
            57,
            198,
            12
        ),
        jugador.vida / 100,
        (
            232,
            68,
            55
        )
    )


    # =====================================================
    # EXTINTOR
    # =====================================================

    ext_panel = pygame.Rect(
        265,
        18,
        210,
        68
    )


    dibujar_panel(
        pantalla,
        ext_panel,
        borde=CIAN,
        relleno=(
            8,
            16,
            26,
            225
        ),
        grosor=1
    )


    pantalla.blit(
        fuente_titulo.render(
            "EXTINTOR",
            True,
            CIAN
        ),
        (
            279,
            27
        )
    )


    pantalla.blit(
        fuente_valor.render(
            (
                f"{jugador.carga_extintor}/"
                f"{jugador.carga_maxima}"
            ),
            True,
            BLANCO
        ),
        (
            383,
            24
        )
    )


    dibujar_barra(
        pantalla,
        pygame.Rect(
            279,
            57,
            178,
            12
        ),
        (
            jugador.carga_extintor
            / max(
                1,
                jugador.carga_maxima
            )
        ),
        CIAN
    )


    # =====================================================
    # TIEMPO
    # =====================================================

    tiempo_panel = pygame.Rect(
        592,
        18,
        190,
        68
    )


    dibujar_panel(
        pantalla,
        tiempo_panel,
        borde=(
            206,
            139,
            66
        ),
        relleno=(
            8,
            13,
            23,
            225
        ),
        grosor=1
    )


    pantalla.blit(
        fuente_titulo.render(
            "TIEMPO",
            True,
            (
                255,
                164,
                79
            )
        ),
        (
            607,
            28
        )
    )


    segundos = (
        cronometro.obtener_segundos()
    )


    tiempo = fuente_valor.render(
        f"{segundos:03d}s",
        True,
        BLANCO
    )


    pantalla.blit(
        tiempo,
        tiempo.get_rect(
            midright=(
                765,
                38
            )
        )
    )


    # =====================================================
    # NOMBRE DEL PERSONAJE
    # =====================================================

    nombre_panel = pygame.Rect(
        18,
        ALTO_PANTALLA - 48,
        176,
        30
    )


    pygame.draw.rect(
        pantalla,
        (
            8,
            14,
            24
        ),
        nombre_panel,
        border_radius=8
    )


    pygame.draw.rect(
        pantalla,
        CIAN,
        nombre_panel,
        1,
        border_radius=8
    )


    texto_nombre = fuente_pequena.render(
        NOMBRE_PERSONAJE_ACTUAL.upper(),
        True,
        CIAN_CLARO
    )


    pantalla.blit(
        texto_nombre,
        texto_nombre.get_rect(
            center=nombre_panel.center
        )
    )


    # =====================================================
    # ESQUINAS
    # =====================================================

    dibujar_esquinas_hud(
        pantalla
    )


# =========================================================
# LOGOS EN PANTALLA FINAL
# =========================================================

def dibujar_logos_fin(
    pantalla,
    logo_feria,
    logo_espol
):

    if logo_feria:

        mini = pygame.transform.smoothscale(
            logo_feria,
            (
                165,
                int(
                    logo_feria.get_height()
                    * 165
                    / logo_feria.get_width()
                )
            )
        )


        pantalla.blit(
            mini,
            (
                24,
                18
            )
        )


    if logo_espol:

        mini = pygame.transform.smoothscale(
            logo_espol,
            (
                120,
                int(
                    logo_espol.get_height()
                    * 120
                    / logo_espol.get_width()
                )
            )
        )


        pantalla.blit(
            mini,
            mini.get_rect(
                topright=(
                    ANCHO_PANTALLA - 24,
                    22
                )
            )
        )


# =========================================================
# CONFETI
# =========================================================

def crear_confeti(
    cantidad=70
):

    rng = random.Random(
        99
    )


    colores = [

        NARANJA,

        CIAN,

        (
            255,
            209,
            60
        ),

        (
            176,
            89,
            255
        ),

        (
            255,
            89,
            146
        )
    ]


    return [

        {
            "x": rng.uniform(
                0,
                ANCHO_PANTALLA
            ),

            "y": rng.uniform(
                -ALTO_PANTALLA,
                0
            ),

            "vy": rng.uniform(
                55,
                125
            ),

            "vx": rng.uniform(
                -16,
                16
            ),

            "tam": rng.randint(
                4,
                9
            ),

            "color": rng.choice(
                colores
            ),

            "rot": rng.randint(
                0,
                1
            )
        }

        for _ in range(
            cantidad
        )
    ]


# =========================================================
# DIBUJAR CONFETI
# =========================================================

def dibujar_confeti(
    pantalla,
    confeti,
    dt
):

    seg = (
        dt / 1000.0
    )


    for p in confeti:

        p["x"] += (
            p["vx"]
            * seg
        )


        p["y"] += (
            p["vy"]
            * seg
        )


        if (
            p["y"]
            > ALTO_PANTALLA + 10
        ):

            p["y"] = -10

            p["x"] = random.uniform(
                0,
                ANCHO_PANTALLA
            )


        if p["rot"]:

            rect = pygame.Rect(
                int(
                    p["x"]
                ),
                int(
                    p["y"]
                ),
                p["tam"],
                max(
                    2,
                    p["tam"] // 3
                )
            )

        else:

            rect = pygame.Rect(
                int(
                    p["x"]
                ),
                int(
                    p["y"]
                ),
                max(
                    2,
                    p["tam"] // 3
                ),
                p["tam"]
            )


        pygame.draw.rect(
            pantalla,
            p["color"],
            rect,
            border_radius=2
        )


# =========================================================
# ICONO TRISTE
# =========================================================

def dibujar_icono_triste(
    pantalla,
    centro
):

    x, y = centro


    nube = pygame.Surface(
        (
            120,
            90
        ),
        pygame.SRCALPHA
    )


    # Nube
    pygame.draw.circle(
        nube,
        (
            111,
            128,
            145,
            220
        ),
        (
            40,
            38
        ),
        25
    )


    pygame.draw.circle(
        nube,
        (
            111,
            128,
            145,
            220
        ),
        (
            65,
            28
        ),
        29
    )


    pygame.draw.circle(
        nube,
        (
            111,
            128,
            145,
            220
        ),
        (
            89,
            39
        ),
        23
    )


    pygame.draw.rect(
        nube,
        (
            111,
            128,
            145,
            220
        ),
        (
            30,
            38,
            70,
            27
        ),
        border_radius=14
    )


    # Ojos
    pygame.draw.circle(
        nube,
        (
            25,
            35,
            48
        ),
        (
            53,
            43
        ),
        3
    )


    pygame.draw.circle(
        nube,
        (
            25,
            35,
            48
        ),
        (
            77,
            43
        ),
        3
    )


    # Boca triste
    pygame.draw.arc(
        nube,
        (
            25,
            35,
            48
        ),
        (
            53,
            46,
            25,
            18
        ),
        math.pi,
        math.tau,
        2
    )


    # Gotas
    pygame.draw.polygon(
        nube,
        (
            66,
            168,
            205
        ),
        [
            (
                42,
                68
            ),
            (
                36,
                80
            ),
            (
                48,
                80
            )
        ]
    )


    pygame.draw.polygon(
        nube,
        (
            66,
            168,
            205
        ),
        [
            (
                78,
                68
            ),
            (
                72,
                82
            ),
            (
                84,
                82
            )
        ]
    )


    pantalla.blit(
        nube,
        nube.get_rect(
            center=(
                x,
                y
            )
        )
    )


# =========================================================
# PANTALLA FINAL
# =========================================================

def mostrar_pantalla_fin(
    pantalla,
    ha_ganado
):

    reloj = pygame.time.Clock()


    fondo = crear_fondo_atmosferico(
        semilla=61
    )


    logo_feria, logo_espol = (
        cargar_logos()
    )


    confeti = (

        crear_confeti()

        if ha_ganado

        else []
    )


    fuente_titulo = pygame.font.SysFont(
        "Bahnschrift",
        58,
        bold=True
    )


    fuente_texto = pygame.font.SysFont(
        "Bahnschrift",
        20
    )


    fuente_boton = pygame.font.SysFont(
        "Bahnschrift",
        20,
        bold=True
    )


    while True:

        dt = reloj.tick(
            60
        )


        # =================================================
        # EVENTOS
        # =================================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.event.clear()

                return False


            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_r:

                    pygame.event.clear()

                    return True


                if evento.key == pygame.K_ESCAPE:

                    pygame.event.clear()

                    return False


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


        oscuro = pygame.Surface(
            (
                ANCHO_PANTALLA,
                ALTO_PANTALLA
            ),
            pygame.SRCALPHA
        )


        oscuro.fill(
            (
                2,
                5,
                11,
                115
            )
        )


        pantalla.blit(
            oscuro,
            (
                0,
                0
            )
        )


        # =================================================
        # LOGOS
        # =================================================

        dibujar_logos_fin(
            pantalla,
            logo_feria,
            logo_espol
        )


        # =================================================
        # PANEL CENTRAL
        # =================================================

        borde = (

            NARANJA

            if ha_ganado

            else (
                89,
                117,
                138
            )
        )


        panel = pygame.Rect(
            145,
            118,
            510,
            390
        )


        dibujar_panel(
            pantalla,
            panel,
            borde=borde,
            relleno=(
                7,
                12,
                20,
                235
            ),
            grosor=2,
            glow=ha_ganado
        )


        # =================================================
        # VICTORIA
        # =================================================

        if ha_ganado:

            dibujar_confeti(
                pantalla,
                confeti,
                dt
            )


            titulo = fuente_titulo.render(
                "¡VICTORIA!",
                True,
                (
                    255,
                    203,
                    62
                )
            )


            subtitulo = fuente_texto.render(
                (
                    "Has demostrado tu "
                    "ingenio y valentía."
                ),
                True,
                BLANCO
            )


            mensaje = fuente_texto.render(
                (
                    "La salida estaba a un "
                    "paso de tus decisiones."
                ),
                True,
                CIAN
            )


            # =============================================
            # MEDALLA / FRASCO
            # =============================================

            pygame.draw.circle(
                pantalla,
                (
                    18,
                    67,
                    82
                ),
                (
                    400,
                    278
                ),
                42
            )


            pygame.draw.circle(
                pantalla,
                CIAN,
                (
                    400,
                    278
                ),
                42,
                2
            )


            pygame.draw.line(
                pantalla,
                CIAN_CLARO,
                (
                    387,
                    256
                ),
                (
                    387,
                    281
                ),
                4
            )


            pygame.draw.line(
                pantalla,
                CIAN_CLARO,
                (
                    413,
                    256
                ),
                (
                    413,
                    281
                ),
                4
            )


            pygame.draw.line(
                pantalla,
                CIAN_CLARO,
                (
                    387,
                    281
                ),
                (
                    377,
                    300
                ),
                4
            )


            pygame.draw.line(
                pantalla,
                CIAN_CLARO,
                (
                    413,
                    281
                ),
                (
                    423,
                    300
                ),
                4
            )


            pygame.draw.line(
                pantalla,
                CIAN_CLARO,
                (
                    377,
                    300
                ),
                (
                    423,
                    300
                ),
                4
            )


            pygame.draw.circle(
                pantalla,
                (
                    255,
                    203,
                    62
                ),
                (
                    392,
                    291
                ),
                3
            )


            pygame.draw.circle(
                pantalla,
                NARANJA,
                (
                    407,
                    294
                ),
                3
            )


        # =================================================
        # DERROTA
        # =================================================

        else:

            titulo = fuente_titulo.render(
                "PERDISTE",
                True,
                (
                    193,
                    199,
                    205
                )
            )


            subtitulo = fuente_texto.render(
                (
                    "El laberinto aún "
                    "guarda sus secretos."
                ),
                True,
                BLANCO
            )


            mensaje = fuente_texto.render(
                (
                    "No te rindas. Intenta "
                    "una ruta diferente."
                ),
                True,
                (
                    255,
                    140,
                    66
                )
            )


            dibujar_icono_triste(
                pantalla,
                (
                    400,
                    278
                )
            )


        # =================================================
        # TEXTOS
        # =================================================

        pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(
                    400,
                    185
                )
            )
        )


        pantalla.blit(
            subtitulo,
            subtitulo.get_rect(
                center=(
                    400,
                    340
                )
            )
        )


        pantalla.blit(
            mensaje,
            mensaje.get_rect(
                center=(
                    400,
                    370
                )
            )
        )


        # =================================================
        # BOTONES
        # =================================================

        boton_r = pygame.Rect(
            245,
            405,
            310,
            48
        )


        boton_esc = pygame.Rect(
            245,
            462,
            310,
            34
        )


        dibujar_panel(
            pantalla,
            boton_r,
            borde=borde,
            relleno=(
                18,
                18,
                22,
                235
            ),
            grosor=2,
            glow=ha_ganado
        )


        pygame.draw.rect(
            pantalla,
            (
                18,
                22,
                28
            ),
            boton_esc,
            border_radius=8
        )


        pygame.draw.rect(
            pantalla,
            (
                96,
                105,
                114
            ),
            boton_esc,
            1,
            border_radius=8
        )


        # =================================================
        # TEXTO BOTONES
        # =================================================

        texto_r = fuente_boton.render(

            (
                "[ R ]  JUGAR DE NUEVO"

                if ha_ganado

                else "[ R ]  REINTENTAR"
            ),

            True,
            BLANCO
        )


        texto_esc = fuente_boton.render(
            "[ ESC ]  SALIR",
            True,
            (
                194,
                201,
                208
            )
        )


        pantalla.blit(
            texto_r,
            texto_r.get_rect(
                center=boton_r.center
            )
        )


        pantalla.blit(
            texto_esc,
            texto_esc.get_rect(
                center=boton_esc.center
            )
        )


        # =================================================
        # ESQUINAS
        # =================================================

        dibujar_esquinas_hud(
            pantalla,
            color=borde
        )


        pygame.display.flip()


# =========================================================
# ACTUALIZAR PANTALLA
# =========================================================

def actualizar_pantalla():

    pygame.display.flip()