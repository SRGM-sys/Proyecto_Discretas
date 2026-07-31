# DEV_2/gestor_menu.py
import pygame
import os
from config import ANCHO_PANTALLA, ALTO_PANTALLA, NEGRO

def mostrar_menu(pantalla):
    """
    Dibuja la pantalla de inicio con una imagen pequeña debajo del texto.
    """
    reloj = pygame.time.Clock()
    fuente_titulo = pygame.font.SysFont("Arial", 50, bold=True)
    fuente_instruccion = pygame.font.SysFont("Arial", 24)
    
    # --- CARGAR IMAGEN PEQUEÑA ---
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.dirname(ruta_actual)
    # Cambia 'logo_menu.png' por el nombre real de tu archivo pequeño
    ruta_imagen = os.path.join(ruta_raiz, 'assets', 'sprites', 'menu_bg.webp') 
    
    imagen_menu = None
    try:
        # Usamos convert_alpha() por si tu imagen pequeña tiene transparencia
        img_original = pygame.image.load(ruta_imagen).convert_alpha()
        
        # Define aquí el tamaño pequeño que quieras (por ejemplo, 120x120 píxeles)
        ancho_deseado, alto_deseado = 120, 120
        imagen_menu = pygame.transform.scale(img_original, (ancho_deseado, alto_deseado))
    except Exception as e:
        print(f"No se encontró la imagen en {ruta_imagen}. Error: {e}")

    # Textos renderizados
    texto_titulo = fuente_titulo.render("LABERINTO SOBRENATURAL", True, (255, 69, 0))
    texto_sub = fuente_instruccion.render("Sobrevive al terremoto y al fuego", True, (240, 240, 240))
    texto_start = fuente_instruccion.render("Presiona [ENTER] para comenzar", True, (0, 255, 255))
    
    # Posiciones de los textos
    rect_titulo = texto_titulo.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 80))
    rect_sub = texto_sub.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 30))
    rect_start = texto_start.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 130))
    
    # Posición de la imagen (centrada horizontalmente y ubicada debajo de los subtítulos)
    if imagen_menu:
        rect_imagen = imagen_menu.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 45))

    contador_parpadeo = 0

    en_menu = True
    while en_menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True 

        # Fondo negro limpio para que resalte la imagen pequeña
        pantalla.fill(NEGRO)
        
        # Dibujar textos
        pantalla.blit(texto_titulo, rect_titulo)
        pantalla.blit(texto_sub, rect_sub)

        # Dibujar la imagen pequeña debajo del texto (si cargó bien)
        if imagen_menu:
            pantalla.blit(imagen_menu, rect_imagen)

        # Texto parpadeante
        contador_parpadeo += 1
        if (contador_parpadeo // 30) % 2 == 0:
            pantalla.blit(texto_start, rect_start)

        pygame.display.flip()
        reloj.tick(60)