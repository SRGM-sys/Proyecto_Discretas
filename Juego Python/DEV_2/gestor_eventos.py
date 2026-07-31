import pygame

def procesar_inputs():
    """
    Devuelve el intento de movimiento en X e Y, y si el jugador cerró la ventana.
    Dev 1 llamará a esto para actualizar sus coordenadas.
    """
    mov_x, mov_y = 0, 0
    salir = False

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            salir = True

    teclas = pygame.key.get_pressed()
    
    # Arriba / Abajo
    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        mov_y = -1
    elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        mov_y = 1
        
    # Izquierda / Derecha
    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        mov_x = -1
    elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        mov_x = 1

    return mov_x, mov_y, salir