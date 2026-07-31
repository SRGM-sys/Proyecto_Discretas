import pygame
import os
from config import ANCHO_PANTALLA, ALTO_PANTALLA, TAMANO_CELDA, VERDE_JUGADOR, NEGRO, GRIS_PARED, ROJO_FUEGO

HOJA_JUGADOR_PRO = []

def inicializar_pantalla():
    global HOJA_JUGADOR_PRO 
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

def dibujar_laberinto(pantalla, matriz, camara):
    pantalla.fill(NEGRO) 
    
    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            valor = matriz[fila][col]
            
            x_pantalla = (col * TAMANO_CELDA) + camara.desplazamiento_x
            y_pantalla = (fila * TAMANO_CELDA) + camara.desplazamiento_y
            
            rect = pygame.Rect(x_pantalla, y_pantalla, TAMANO_CELDA, TAMANO_CELDA)
            
            if valor == 1: 
                pygame.draw.rect(pantalla, GRIS_PARED, rect)
            elif valor == 3: 
                pygame.draw.rect(pantalla, (255, 215, 0), rect) 
            elif valor == 4: 
                pygame.draw.rect(pantalla, (139, 0, 0), rect)
            elif valor == 5: 
                pygame.draw.rect(pantalla, ROJO_FUEGO, rect)
            elif valor == 6: 
                pygame.draw.rect(pantalla, (0, 255, 255), rect) 

def actualizar_pantalla():
    pygame.display.flip()