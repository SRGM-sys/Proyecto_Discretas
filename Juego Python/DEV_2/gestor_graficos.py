import pygame
import os
from config import ANCHO_PANTALLA, ALTO_PANTALLA, TAMANO_CELDA, VERDE_JUGADOR, NEGRO, GRIS_PARED, ROJO_FUEGO

HOJA_JUGADOR_PRO = []
IMAGEN_MURO = None

def inicializar_pantalla():
    global HOJA_JUGADOR_PRO, IMAGEN_MURO, HOJA_FUEGO
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA)) 
    pygame.display.set_caption("Laberinto Sobrenatural Pro")
    
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.dirname(ruta_actual)
    ruta_imagen = os.path.join(ruta_raiz, 'assets', 'sprites', 'chica_pro.png')
    
    try:
        HOJA_JUGADOR_PRO = cargar_sprite_sheet(ruta_imagen, filas=4, columnas=4)
        print("¡Imagen de la chica cargada con éxito!")
    except Exception as e:
        print(f"Error cargando imagen. Buscando en: {ruta_imagen}\nEl error fue: {e}")
        cuadro_verde = pygame.Surface((TAMANO_CELDA, TAMANO_CELDA))
        cuadro_verde.fill(VERDE_JUGADOR)
        HOJA_JUGADOR_PRO = [cuadro_verde] * 16
        
        
    ruta_muro = os.path.join(ruta_raiz, 'assets', 'sprites', 'muro.jpg') # Cambia el nombre si tu imagen se llama diferente
    try:
        img_muro_original = pygame.image.load(ruta_muro).convert_alpha()
        # Escalamos la imagen al tamaño exacto de la celda (64x64 píxeles)
        IMAGEN_MURO = pygame.transform.scale(img_muro_original, (TAMANO_CELDA, TAMANO_CELDA))
        print("¡Textura de muro cargada con éxito!")
    except Exception as e:
        print(f"No se encontró la imagen de muro en {ruta_muro}. Se usará color gris. Error: {e}")
        IMAGEN_MURO = None
    
    
    ruta_fuego = os.path.join(ruta_raiz, 'assets', 'sprites', 'fuego.jpg')
    try:
        # Usamos 1 fila y 4 columnas
        HOJA_FUEGO = cargar_sprite_sheet(ruta_fuego, filas=1, columnas=4)
        print("¡Sprites de fuego cargados con éxito!")
    except Exception as e:
        print(f"No se encontró el fuego. Usando cuadro rojo. Error: {e}")
        # Fallback si no encuentra la imagen
        cuadro_rojo = pygame.Surface((TAMANO_CELDA, TAMANO_CELDA))
        cuadro_rojo.fill(ROJO_FUEGO)
        HOJA_FUEGO = [cuadro_rojo] * 4

    return pantalla

def cargar_sprite_sheet(ruta_archivo, filas, columnas):
    imagen_completa = pygame.image.load(ruta_archivo).convert_alpha()
    ancho_completo, alto_completo = imagen_completa.get_size()
    
    ancho_frame = ancho_completo // columnas
    alto_frame = alto_completo // filas
    
    frames = []
    margen = 10 
    tamano_reducido = TAMANO_CELDA - margen
    
    for f in range(filas):
        for c in range(columnas):
            rect = pygame.Rect(c * ancho_frame, f * alto_frame, ancho_frame, alto_frame)
            frame_superficie = pygame.Surface((ancho_frame, alto_frame), pygame.SRCALPHA)
            frame_superficie.blit(imagen_completa, (0, 0), rect)
            frame_escalado = pygame.transform.scale(frame_superficie, (tamano_reducido, tamano_reducido))
            frames.append(frame_escalado)
            
    return frames

def dibujar_jugador_completo(pantalla, logica_x, logica_y, frame_actual, tipo_animacion, camara, flip_x=False):
    margen = 10
    mundo_x = (logica_x * TAMANO_CELDA) + (margen // 2)
    mundo_y = (logica_y * TAMANO_CELDA) + (margen // 2)
    
    x_pantalla = mundo_x + camara.desplazamiento_x
    y_pantalla = mundo_y + camara.desplazamiento_y
    
    indice_base = (tipo_animacion % 4) * 4 
    frame_final = indice_base + (frame_actual % 4)
    
    sprite_a_dibujar = HOJA_JUGADOR_PRO[frame_final]
    
    # MAGIA PRO: Si flip_x es True, volteamos la imagen horizontalmente
    if flip_x:
        sprite_a_dibujar = pygame.transform.flip(sprite_a_dibujar, True, False)
        
    pantalla.blit(sprite_a_dibujar, (x_pantalla, y_pantalla))

def dibujar_laberinto(pantalla, matriz, camara, frame_fuego=0): # <--- Nuevo parámetro
    pantalla.fill(NEGRO) 
    AZUL_OSCURO = (20, 20, 50)
    
    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            valor = matriz[fila][col]
            
            x_pantalla = (col * TAMANO_CELDA) + camara.desplazamiento_x
            y_pantalla = (fila * TAMANO_CELDA) + camara.desplazamiento_y
            rect = pygame.Rect(x_pantalla, y_pantalla, TAMANO_CELDA, TAMANO_CELDA)
            
            if valor != 1: 
                pygame.draw.rect(pantalla, AZUL_OSCURO, rect)
            
            if valor == 1: 
                if IMAGEN_MURO:
                    pantalla.blit(IMAGEN_MURO, (x_pantalla, y_pantalla))
                else:
                    pygame.draw.rect(pantalla, GRIS_PARED, rect)
            elif valor == 3: 
                pygame.draw.rect(pantalla, (255, 215, 0), rect) 
            elif valor == 4: 
                pygame.draw.rect(pantalla, (139, 0, 0), rect)
            elif valor == 5: # --- AQUÍ DIBUJAMOS EL FUEGO ANIMADO ---
                pantalla.blit(HOJA_FUEGO[frame_fuego], (x_pantalla, y_pantalla))
            elif valor == 6: 
                pygame.draw.rect(pantalla, (0, 255, 255), rect)

def actualizar_pantalla():
    pygame.display.flip()
    

def dibujar_hud(pantalla, jugador, cronometro):
    """
    Dibuja la barra de vida, las cargas del extintor y el tiempo en pantalla
    de forma fija (sin que se muevan con la cámara).
    """
    fuente = pygame.font.SysFont("Arial", 20, bold=True)
    
    # 1. Dibujar la Vida (HP)
    texto_vida = fuente.render(f"VIDA: {jugador.vida} HP", True, (255, 50, 50))
    pantalla.blit(texto_vida, (20, 20))
    
    # 2. Dibujar las cargas del extintor
    texto_extintor = fuente.render(f"EXTINTOR: {jugador.carga_extintor}/{jugador.carga_maxima}", True, (0, 255, 255))
    pantalla.blit(texto_extintor, (20, 50))
    
    # 3. Dibujar el Cronómetro (tiempo transcurrido)
    segundos = cronometro.obtener_segundos()
    texto_tiempo = fuente.render(f"TIEMPO: {segundos}s", True, (255, 255, 255))
    pantalla.blit(texto_tiempo, (ANCHO_PANTALLA - 130, 20))
    

def mostrar_pantalla_fin(pantalla, ha_ganado):
    fuente_titulo = pygame.font.SysFont("Arial", 50, bold=True)
    fuente_sub = pygame.font.SysFont("Arial", 22)
    
    if ha_ganado:
        texto_principal = fuente_titulo.render("¡HAS GANADO!", True, (255, 215, 0))
    else:
        texto_principal = fuente_titulo.render("¡HAS MUERTO!", True, (255, 50, 50))
        
    texto_reintentar = fuente_sub.render("Presiona [ R ] para intentar de nuevo", True, (0, 255, 255))
    texto_salir = fuente_sub.render("Presiona [ ESC ] para salir", True, (200, 200, 200))
    
    rect_principal = texto_principal.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 40))
    rect_reintentar = texto_reintentar.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 20))
    rect_salir = texto_salir.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 60))

    reloj = pygame.time.Clock()
    while True:
        pantalla.fill(NEGRO)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.event.clear()
                return False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    pygame.event.clear() # Limpiamos eventos para que no interfieran con el nuevo juego
                    return True
                if evento.key == pygame.K_ESCAPE:
                    pygame.event.clear()
                    return False

        pantalla.blit(texto_principal, rect_principal)
        pantalla.blit(texto_reintentar, rect_reintentar)
        pantalla.blit(texto_salir, rect_salir)
        
        pygame.display.flip()
        reloj.tick(60)