import pygame
import os
# Importamos del config ORIGINAL de la raíz
from config import ANCHO_PANTALLA,ALTO_PANTALLA,TAMANO_CELDA,VERDE_JUGADOR,NEGRO,GRIS_PARED,ROJO_FUEGO

# Dejamos la lista vacía al inicio
HOJA_JUGADOR_PRO = []

def inicializar_pantalla():
    """Levanta la ventana de Pygame, la devuelve Y carga la imagen."""
    global HOJA_JUGADOR_PRO 
    
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA)) 
    pygame.display.set_caption("Laberinto Sobrenatural Pro")
    
    # MAGIA PRO: Construimos la ruta exacta y absoluta sin importar dónde ejecutes el código
    ruta_actual = os.path.dirname(os.path.abspath(__file__)) # Esto nos da la ruta de DEV_2
    ruta_raiz = os.path.dirname(ruta_actual) # Subimos una carpeta a la raíz del proyecto
    ruta_imagen = os.path.join(ruta_raiz, 'assets', 'sprites', 'chica_pro.png')
    
    try:
        HOJA_JUGADOR_PRO = cargar_sprite_sheet(ruta_imagen, filas=4, columnas=4)
        print("¡Imagen de la chica cargada con éxito!")
    except Exception as e:
        print(f"Error cargando imagen. Buscando en: {ruta_imagen}")
        print(f"El error fue: {e}")
        # Fallback verde
        cuadro_verde = pygame.Surface((TAMANO_CELDA, TAMANO_CELDA))
        cuadro_verde.fill(VERDE_JUGADOR)
        HOJA_JUGADOR_PRO = [cuadro_verde] * 16

    return pantalla

def cargar_sprite_sheet(ruta_archivo, filas, columnas):
    imagen_completa = pygame.image.load(ruta_archivo).convert_alpha()
    ancho_completo, alto_completo = imagen_completa.get_size()
    
    ancho_frame = ancho_completo // columnas
    alto_frame = alto_completo // filas
    
    frames = []
    for f in range(filas):
        for c in range(columnas):
            rect = pygame.Rect(c * ancho_frame, f * alto_frame, ancho_frame, alto_frame)
            frame_superficie = pygame.Surface((ancho_frame, alto_frame), pygame.SRCALPHA)
            frame_superficie.blit(imagen_completa, (0, 0), rect)
            frame_escalado = pygame.transform.scale(frame_superficie, (TAMANO_CELDA, TAMANO_CELDA))
            frames.append(frame_escalado)
            
    return frames

def dibujar_jugador_completo(pantalla, logica_x, logica_y, frame_actual, tipo_animacion=0):
    x_pixel = logica_x * TAMANO_CELDA
    y_pixel = logica_y * TAMANO_CELDA
    
    indice_base = (tipo_animacion % 4) * 4 
    frame_final = indice_base + (frame_actual % 4)
    
    sprite_a_dibujar = HOJA_JUGADOR_PRO[frame_final]
    pantalla.blit(sprite_a_dibujar, (x_pixel, y_pixel))

def dibujar_laberinto(pantalla, matriz):
    pantalla.fill(NEGRO) 
    
    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            valor = matriz[fila][col]
            
            x_pixel = col * TAMANO_CELDA
            y_pixel = fila * TAMANO_CELDA
            rect = pygame.Rect(x_pixel, y_pixel, TAMANO_CELDA, TAMANO_CELDA)
            
            # Tu compa Dev 1 añadió nuevas cosas (5 = fuego, 6 = extintor)
            if valor == 1: 
                pygame.draw.rect(pantalla, GRIS_PARED, rect)
            elif valor == 3: # Meta
                pygame.draw.rect(pantalla, (255, 215, 0), rect) 
            elif valor == 4: # Escombros
                pygame.draw.rect(pantalla, (139, 0, 0), rect)
            elif valor == 5: # Fuego
                pygame.draw.rect(pantalla, ROJO_FUEGO, rect)
            elif valor == 6: # Extintor
                pygame.draw.rect(pantalla, (0, 255, 255), rect) # Cian para el extintor

def actualizar_pantalla():
    pygame.display.flip()