import math
import os
import random
import pygame

from config import ANCHO_PANTALLA, ALTO_PANTALLA


# =========================================================
# COLORES GENERALES
# =========================================================

NARANJA = (255, 112, 35)
NARANJA_CLARO = (255, 166, 74)

CIAN = (0, 224, 235)
CIAN_CLARO = (115, 246, 255)

AZUL_NOCHE = (10, 15, 28)
AZUL_PANEL = (18, 27, 43)

BLANCO = (242, 246, 250)
GRIS = (158, 170, 185)


# =========================================================
# RUTAS
# =========================================================

def ruta_interfaz(nombre):
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_src = os.path.dirname(ruta_actual)
    ruta_raiz = os.path.dirname(ruta_src)
    return os.path.join(ruta_raiz, "assets", "interfaz", nombre)


# =========================================================
# CARGAR IMAGEN SIN DEFORMAR
# =========================================================

def cargar_imagen_ajustada(
    ruta,
    max_ancho,
    max_alto
):

    try:

        imagen = pygame.image.load(
            ruta
        ).convert_alpha()

        ancho, alto = imagen.get_size()

        escala = min(
            max_ancho / ancho,
            max_alto / alto
        )

        nuevo_ancho = max(
            1,
            int(ancho * escala)
        )

        nuevo_alto = max(
            1,
            int(alto * escala)
        )

        return pygame.transform.smoothscale(
            imagen,
            (
                nuevo_ancho,
                nuevo_alto
            )
        )

    except Exception as error:

        print(
            f"No se pudo cargar {ruta}: {error}"
        )

        return None


# =========================================================
# CONVERTIR LOGO A BLANCO
# =========================================================

def convertir_logo_blanco(
    imagen
):

    if imagen is None:

        return None

    mascara = pygame.mask.from_surface(
        imagen
    )

    logo_blanco = mascara.to_surface(
        setcolor=(
            245,
            248,
            255,
            255
        ),
        unsetcolor=(
            0,
            0,
            0,
            0
        )
    )

    return logo_blanco.convert_alpha()


# =========================================================
# CARGAR LOGOS
# =========================================================

def cargar_logos():

    # Logo Feria de Ciencias
    feria = cargar_imagen_ajustada(
        ruta_interfaz(
            "logo_feriaFN.png"
        ),
        205,
        72
    )

    # Logo ESPOL
    espol = cargar_imagen_ajustada(
        ruta_interfaz(
            "logo espol.png"
        ),
        165,
        58
    )

    # El logo de ESPOL se transforma a blanco
    espol = convertir_logo_blanco(
        espol
    )

    return feria, espol


# =========================================================
# CREAR FONDO ATMOSFÉRICO
# =========================================================

def crear_fondo_atmosferico(
    ancho=ANCHO_PANTALLA,
    alto=ALTO_PANTALLA,
    semilla=13
):

    fondo = pygame.Surface(
        (
            ancho,
            alto
        )
    ).convert()


    # =====================================================
    # DEGRADADO OSCURO
    # =====================================================

    for y in range(
        alto
    ):

        t = y / max(
            1,
            alto - 1
        )

        r = int(
            9 + 24 * t
        )

        g = int(
            13 + 8 * t
        )

        b = int(
            25 + 3 * t
        )

        pygame.draw.line(
            fondo,
            (
                r,
                g,
                b
            ),
            (
                0,
                y
            ),
            (
                ancho,
                y
            )
        )


    rng = random.Random(
        semilla
    )


    atmosfera = pygame.Surface(
        (
            ancho,
            alto
        ),
        pygame.SRCALPHA
    )


    # =====================================================
    # LUCES DEL INCENDIO
    # =====================================================

    for _ in range(
        10
    ):

        x = rng.randint(
            -40,
            ancho + 40
        )

        y = rng.randint(
            int(
                alto * 0.46
            ),
            int(
                alto * 0.82
            )
        )

        radio = rng.randint(
            70,
            180
        )


        for rr in range(
            radio,
            0,
            -18
        ):

            alpha = max(
                0,
                int(
                    2
                    + 18
                    * (
                        rr / radio
                    )
                )
            )

            pygame.draw.circle(
                atmosfera,
                (
                    255,
                    83,
                    20,
                    alpha
                ),
                (
                    x,
                    y
                ),
                rr
            )


    # =====================================================
    # HUMO
    # =====================================================

    for _ in range(
        28
    ):

        x = rng.randint(
            -80,
            ancho + 80
        )

        y = rng.randint(
            70,
            int(
                alto * 0.72
            )
        )

        rx = rng.randint(
            70,
            170
        )

        ry = rng.randint(
            30,
            85
        )


        nube = pygame.Surface(
            (
                rx * 2,
                ry * 2
            ),
            pygame.SRCALPHA
        )


        pygame.draw.ellipse(
            nube,
            (
                72,
                59,
                70,
                rng.randint(
                    14,
                    28
                )
            ),
            nube.get_rect()
        )


        atmosfera.blit(
            nube,
            (
                x - rx,
                y - ry
            )
        )


    fondo.blit(
        atmosfera,
        (
            0,
            0
        )
    )


    # =====================================================
    # BOSQUE
    # =====================================================

    arboles = pygame.Surface(
        (
            ancho,
            alto
        ),
        pygame.SRCALPHA
    )


    suelo = int(
        alto * 0.90
    )


    for _ in range(
        25
    ):

        x = rng.randint(
            -20,
            ancho + 20
        )


        altura = rng.randint(
            int(
                alto * 0.22
            ),
            int(
                alto * 0.62
            )
        )


        tronco = max(
            3,
            int(
                altura * 0.035
            )
        )


        color = rng.choice(
            [
                (
                    5,
                    9,
                    14,
                    230
                ),

                (
                    8,
                    11,
                    17,
                    220
                ),

                (
                    14,
                    14,
                    20,
                    215
                )
            ]
        )


        pygame.draw.rect(
            arboles,
            color,
            (
                x - tronco // 2,
                suelo - altura,
                tronco,
                altura
            )
        )


        niveles = rng.randint(
            4,
            7
        )


        for nivel in range(
            niveles
        ):

            yy = (
                suelo
                - altura
                + int(
                    (
                        nivel + 1
                    )
                    * altura
                    / (
                        niveles + 1
                    )
                )
            )


            mitad = int(
                (
                    nivel + 1
                )
                * altura
                * 0.10
            )


            pygame.draw.polygon(
                arboles,
                color,
                [
                    (
                        x,
                        yy
                        - int(
                            altura * 0.12
                        )
                    ),

                    (
                        x - mitad,
                        yy
                        + int(
                            altura * 0.08
                        )
                    ),

                    (
                        x + mitad,
                        yy
                        + int(
                            altura * 0.08
                        )
                    )
                ]
            )


    fondo.blit(
        arboles,
        (
            0,
            0
        )
    )


    # =====================================================
    # FUEGO DE LA PARTE INFERIOR
    # =====================================================

    fuego = pygame.Surface(
        (
            ancho,
            alto
        ),
        pygame.SRCALPHA
    )


    for _ in range(
        55
    ):

        x = rng.randint(
            0,
            ancho
        )


        base_y = rng.randint(
            int(
                alto * 0.76
            ),
            alto + 20
        )


        h = rng.randint(
            16,
            78
        )


        w = rng.randint(
            8,
            28
        )


        pygame.draw.ellipse(
            fuego,
            (
                255,
                63,
                10,
                rng.randint(
                    20,
                    54
                )
            ),
            (
                x - w // 2,
                base_y - h,
                w,
                h
            )
        )


        if rng.random() < 0.65:

            pygame.draw.ellipse(
                fuego,
                (
                    255,
                    166,
                    30,
                    rng.randint(
                        18,
                        45
                    )
                ),
                (
                    x - w // 4,
                    base_y
                    - int(
                        h * 0.68
                    ),
                    max(
                        4,
                        w // 2
                    ),
                    int(
                        h * 0.58
                    )
                )
            )


    fondo.blit(
        fuego,
        (
            0,
            0
        )
    )


    # =====================================================
    # OSCURECER EL FONDO
    # =====================================================

    capa_oscura = pygame.Surface(
        (
            ancho,
            alto
        ),
        pygame.SRCALPHA
    )


    capa_oscura.fill(
        (
            5,
            8,
            16,
            128
        )
    )


    fondo.blit(
        capa_oscura,
        (
            0,
            0
        )
    )


    # =====================================================
    # VIÑETA
    # =====================================================

    vignette = pygame.Surface(
        (
            ancho,
            alto
        ),
        pygame.SRCALPHA
    )


    for i in range(
        8
    ):

        margen = i * 12

        alpha = (
            12
            + i * 3
        )


        pygame.draw.rect(
            vignette,
            (
                0,
                0,
                0,
                alpha
            ),
            (
                margen,
                margen,
                ancho
                - 2 * margen,
                alto
                - 2 * margen
            ),
            width=24
        )


    fondo.blit(
        vignette,
        (
            0,
            0
        )
    )


    return fondo


# =========================================================
# PANEL VISUAL
# =========================================================

def dibujar_panel(
    superficie,
    rect,
    borde=CIAN,
    relleno=(
        12,
        18,
        30,
        218
    ),
    grosor=2,
    radio=12,
    glow=False
):

    # =====================================================
    # GLOW
    # =====================================================

    if glow:

        for extra, alpha in (
            (
                12,
                25
            ),
            (
                7,
                38
            ),
            (
                3,
                55
            )
        ):

            capa = pygame.Surface(
                (
                    rect.width
                    + extra * 2,

                    rect.height
                    + extra * 2
                ),
                pygame.SRCALPHA
            )


            pygame.draw.rect(
                capa,
                (
                    *borde,
                    alpha
                ),
                capa.get_rect(),
                width=2,
                border_radius=(
                    radio
                    + extra // 2
                )
            )


            superficie.blit(
                capa,
                (
                    rect.x - extra,
                    rect.y - extra
                )
            )


    # =====================================================
    # PANEL
    # =====================================================

    panel = pygame.Surface(
        rect.size,
        pygame.SRCALPHA
    )


    pygame.draw.rect(
        panel,
        relleno,
        panel.get_rect(),
        border_radius=radio
    )


    pygame.draw.rect(
        panel,
        (
            *borde,
            235
        ),
        panel.get_rect(),
        width=grosor,
        border_radius=radio
    )


    superficie.blit(
        panel,
        rect.topleft
    )


# =========================================================
# ESQUINAS DE LA INTERFAZ
# =========================================================

def dibujar_esquinas_hud(
    superficie,
    color=CIAN
):

    largo = 30
    margen = 12
    grosor = 2


    puntos = [

        (
            (
                margen,
                margen + largo
            ),
            (
                margen,
                margen
            ),
            (
                margen + largo,
                margen
            )
        ),

        (
            (
                ANCHO_PANTALLA
                - margen
                - largo,
                margen
            ),
            (
                ANCHO_PANTALLA
                - margen,
                margen
            ),
            (
                ANCHO_PANTALLA
                - margen,
                margen
                + largo
            )
        ),

        (
            (
                margen,
                ALTO_PANTALLA
                - margen
                - largo
            ),
            (
                margen,
                ALTO_PANTALLA
                - margen
            ),
            (
                margen + largo,
                ALTO_PANTALLA
                - margen
            )
        ),

        (
            (
                ANCHO_PANTALLA
                - margen
                - largo,
                ALTO_PANTALLA
                - margen
            ),
            (
                ANCHO_PANTALLA
                - margen,
                ALTO_PANTALLA
                - margen
            ),
            (
                ANCHO_PANTALLA
                - margen,
                ALTO_PANTALLA
                - margen
                - largo
            )
        )
    ]


    for a, b, c in puntos:

        pygame.draw.line(
            superficie,
            color,
            a,
            b,
            grosor
        )

        pygame.draw.line(
            superficie,
            color,
            b,
            c,
            grosor
        )


# =========================================================
# CREAR PARTÍCULAS
# =========================================================

def crear_particulas(
    cantidad,
    ancho=ANCHO_PANTALLA,
    alto=ALTO_PANTALLA,
    modo="ascender"
):

    rng = random.Random(
        31
    )


    particulas = []


    for _ in range(
        cantidad
    ):

        particulas.append(
            {
                "x": rng.uniform(
                    0,
                    ancho
                ),

                "y": rng.uniform(
                    0,
                    alto
                ),

                "vx": rng.uniform(
                    -10,
                    10
                ),

                "vy": (
                    rng.uniform(
                        -36,
                        -15
                    )
                    if modo
                    == "ascender"
                    else rng.uniform(
                        45,
                        90
                    )
                ),

                "tam": rng.randint(
                    1,
                    3
                ),

                "fase": rng.uniform(
                    0,
                    math.tau
                ),

                "color": rng.choice(
                    [
                        NARANJA,
                        NARANJA_CLARO,
                        CIAN
                    ]
                )
            }
        )


    return particulas


# =========================================================
# ACTUALIZAR PARTÍCULAS
# =========================================================

def actualizar_particulas(
    superficie,
    particulas,
    dt,
    modo="ascender"
):

    segundos = (
        dt / 1000.0
    )


    ancho, alto = (
        superficie.get_size()
    )


    for p in particulas:

        p["x"] += (
            p["vx"]
            * segundos
        )


        p["y"] += (
            p["vy"]
            * segundos
        )


        p["fase"] += (
            segundos
            * 2.0
        )


        p["x"] += (
            math.sin(
                p["fase"]
            )
            * 0.15
        )


        if modo == "ascender":

            if p["y"] < -8:

                p["y"] = (
                    alto + 5
                )

                p["x"] = random.uniform(
                    0,
                    ancho
                )

        else:

            if p["y"] > alto + 8:

                p["y"] = -5

                p["x"] = random.uniform(
                    0,
                    ancho
                )


        alpha = (
            110
            + int(
                75
                * (
                    0.5
                    + 0.5
                    * math.sin(
                        p["fase"]
                    )
                )
            )
        )


        pygame.draw.circle(
            superficie,
            (
                *p["color"],
                max(
                    30,
                    min(
                        220,
                        alpha
                    )
                )
            ),
            (
                int(
                    p["x"]
                ),
                int(
                    p["y"]
                )
            ),
            p["tam"]
        )