import pygame


def procesar_inputs():

    """
    Devuelve:

    mov_x -> movimiento horizontal
    mov_y -> movimiento vertical
    salir -> True si el usuario quiere cerrar el juego
    """

    mov_x = 0
    mov_y = 0

    salir = False


    # =====================================================
    # EVENTOS
    # =====================================================

    for evento in pygame.event.get():

        # -------------------------------------------------
        # CERRAR VENTANA
        # -------------------------------------------------

        if evento.type == pygame.QUIT:

            salir = True


        # -------------------------------------------------
        # ESC = SALIR INMEDIATAMENTE
        # -------------------------------------------------

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:

                salir = True


    # =====================================================
    # TECLAS DE MOVIMIENTO
    # =====================================================

    teclas = pygame.key.get_pressed()


    # =====================================================
    # ARRIBA
    # =====================================================

    if (
        teclas[pygame.K_w]
        or teclas[pygame.K_UP]
    ):

        mov_y = -1


    # =====================================================
    # ABAJO
    # =====================================================

    elif (
        teclas[pygame.K_s]
        or teclas[pygame.K_DOWN]
    ):

        mov_y = 1


    # =====================================================
    # IZQUIERDA
    # =====================================================

    if (
        teclas[pygame.K_a]
        or teclas[pygame.K_LEFT]
    ):

        mov_x = -1


    # =====================================================
    # DERECHA
    # =====================================================

    elif (
        teclas[pygame.K_d]
        or teclas[pygame.K_RIGHT]
    ):

        mov_x = 1


    # =====================================================
    # RETORNO
    # =====================================================

    return (
        mov_x,
        mov_y,
        salir
    )