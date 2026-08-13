import pygame

def procesar_inputs():
    """
    Devuelve:
    mov_x -> movimiento horizontal
    mov_y -> movimiento vertical
    accion -> True si presiona la barra espaciadora
    salir -> True si el usuario quiere cerrar el juego
    """
    mov_x = 0
    mov_y = 0
    accion = False
    salir = False

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            salir = True
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                salir = True

    teclas = pygame.key.get_pressed()

    # =====================================================
    # ACCIÓN (DISPARAR EXTINTOR)
    # =====================================================
    if teclas[pygame.K_SPACE]:
        accion = True

    # =====================================================
    # MOVIMIENTO
    # =====================================================
    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        mov_y = -1
    elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        mov_y = 1

    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        mov_x = -1
    elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        mov_x = 1

    return mov_x, mov_y, accion, salir