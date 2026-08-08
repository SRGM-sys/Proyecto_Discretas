import pygame

from config import ANCHO_PANTALLA, ALTO_PANTALLA, NEGRO
from DEV_2.personajes import PERSONAJES


def cargar_vista_previa(ruta_imagen):
    """
    Carga la imagen del personaje y la adapta
    para mostrarla en la pantalla de selección.
    """
    try:
        imagen = pygame.image.load(ruta_imagen).convert_alpha()
        imagen = pygame.transform.smoothscale(imagen, (95, 95))
        return imagen

    except Exception as error:
        print(f"No se pudo cargar {ruta_imagen}: {error}")

        imagen_error = pygame.Surface((95, 95))
        imagen_error.fill((100, 100, 100))

        fuente = pygame.font.SysFont("Arial", 50, bold=True)
        signo = fuente.render("?", True, (255, 255, 255))
        rect_signo = signo.get_rect(center=(47, 47))
        imagen_error.blit(signo, rect_signo)

        return imagen_error


def seleccionar_personaje(pantalla):
    """
    Muestra los personajes y devuelve
    el personaje elegido por el usuario.

    Devuelve None si el usuario desea salir.
    """
    reloj = pygame.time.Clock()

    fuente_titulo = pygame.font.SysFont("Arial", 34, bold=True)
    fuente_nombre = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_numero = pygame.font.SysFont("Arial", 15)
    fuente_instrucciones = pygame.font.SysFont("Arial", 20)

    imagenes = []

    for personaje in PERSONAJES:
        imagen = cargar_vista_previa(personaje["archivo"])
        imagenes.append(imagen)

    indice_seleccionado = 0

    teclas_numericas = {
        pygame.K_1: 0,
        pygame.K_2: 1,
        pygame.K_3: 2,
        pygame.K_4: 3,
        pygame.K_5: 4,
        pygame.K_6: 5
    }

    columnas = 3

    while True:
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                return None

            if evento.type == pygame.KEYDOWN:

                # Elegir directamente con números
                if evento.key in teclas_numericas:
                    indice_seleccionado = teclas_numericas[evento.key]

                # Izquierda
                elif evento.key in (pygame.K_LEFT, pygame.K_a):
                    indice_seleccionado -= 1
                    if indice_seleccionado < 0:
                        indice_seleccionado = len(PERSONAJES) - 1

                # Derecha
                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    indice_seleccionado += 1
                    if indice_seleccionado >= len(PERSONAJES):
                        indice_seleccionado = 0

                # Arriba
                elif evento.key in (pygame.K_UP, pygame.K_w):
                    indice_seleccionado -= columnas
                    if indice_seleccionado < 0:
                        indice_seleccionado += len(PERSONAJES)

                # Abajo
                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    indice_seleccionado += columnas
                    if indice_seleccionado >= len(PERSONAJES):
                        indice_seleccionado -= len(PERSONAJES)

                # Confirmar selección
                elif evento.key == pygame.K_RETURN:
                    return PERSONAJES[indice_seleccionado]

                # Salir
                elif evento.key == pygame.K_ESCAPE:
                    return None

        pantalla.fill(NEGRO)

        # Título
        texto_titulo = fuente_titulo.render(
            "SELECCIONA TU PERSONAJE",
            True,
            (255, 100, 20)
        )

        rect_titulo = texto_titulo.get_rect(
            center=(ANCHO_PANTALLA // 2, 65)
        )

        pantalla.blit(texto_titulo, rect_titulo)

        # Diseño en 2 filas x 3 columnas
        columnas = 3
        filas = 2
        ancho_tarjeta = 150
        alto_tarjeta = 180
        separacion_x = 20
        separacion_y = 25

        ancho_total = columnas * ancho_tarjeta + (columnas - 1) * separacion_x
        inicio_x = (ANCHO_PANTALLA - ancho_total) // 2
        inicio_y = 130

        for indice, personaje in enumerate(PERSONAJES):
            fila = indice // columnas
            columna = indice % columnas

            posicion_x = inicio_x + columna * (ancho_tarjeta + separacion_x)
            posicion_y = inicio_y + fila * (alto_tarjeta + separacion_y)

            tarjeta = pygame.Rect(
                posicion_x,
                posicion_y,
                ancho_tarjeta,
                alto_tarjeta
            )

            if indice == indice_seleccionado:
                color_fondo = (65, 45, 25)
                color_borde = (255, 140, 0)
                grosor_borde = 5
            else:
                color_fondo = (30, 30, 45)
                color_borde = (120, 120, 120)
                grosor_borde = 2

            pygame.draw.rect(
                pantalla,
                color_fondo,
                tarjeta,
                border_radius=10
            )

            pygame.draw.rect(
                pantalla,
                color_borde,
                tarjeta,
                grosor_borde,
                border_radius=10
            )

            rect_imagen = imagenes[indice].get_rect(
                center=(tarjeta.centerx, posicion_y + 58)
            )

            pantalla.blit(imagenes[indice], rect_imagen)

            texto_nombre = fuente_nombre.render(
                personaje["nombre"],
                True,
                (255, 255, 255)
            )

            rect_nombre = texto_nombre.get_rect(
                center=(tarjeta.centerx, posicion_y + 125)
            )

            pantalla.blit(texto_nombre, rect_nombre)

            texto_numero = fuente_numero.render(
                f"Tecla {indice + 1}",
                True,
                (190, 190, 190)
            )

            rect_numero = texto_numero.get_rect(
                center=(tarjeta.centerx, posicion_y + 152)
            )

            pantalla.blit(texto_numero, rect_numero)

        nombre_elegido = PERSONAJES[indice_seleccionado]["nombre"]

        texto_elegido = fuente_instrucciones.render(
            f"Seleccionado: {nombre_elegido}",
            True,
            (255, 215, 0)
        )

        rect_elegido = texto_elegido.get_rect(
            center=(ANCHO_PANTALLA // 2, 550)
        )

        pantalla.blit(texto_elegido, rect_elegido)

        texto_controles = fuente_instrucciones.render(
            "Usa flechas o A/W/S/D para elegir",
            True,
            (230, 230, 230)
        )

        texto_confirmar = fuente_instrucciones.render(
            "Presiona ENTER para comenzar",
            True,
            (0, 255, 255)
        )

        texto_salir = fuente_instrucciones.render(
            "Presiona ESC para salir",
            True,
            (180, 180, 180)
        )

        pantalla.blit(
            texto_controles,
            texto_controles.get_rect(
                center=(ANCHO_PANTALLA // 2, 585)
            )
        )

        pantalla.blit(
            texto_confirmar,
            texto_confirmar.get_rect(
                center=(ANCHO_PANTALLA // 2, 615)
            )
        )

        pantalla.blit(
            texto_salir,
            texto_salir.get_rect(
                center=(ANCHO_PANTALLA // 2, 645)
            )
        )

        pygame.display.flip()
        reloj.tick(60)