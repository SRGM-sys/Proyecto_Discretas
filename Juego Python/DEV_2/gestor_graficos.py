
import pygame

from config2 import ANCHO_PANTALLA, ALTO_PANTALLA, TAMANO_CELDA, NEGRO


def inicializar_pantalla():
    """Levanta la ventana de Pygame y la devuelve."""
    pygame.init()
    # Usamos los nuevos nombres de tu config
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA)) 
    pygame.display.set_caption("Laberinto Sobrenatural")
    return pantalla

def cargar_sprite_sheet(ruta_archivo, filas, columnas):
    """
    Carga una imagen transparente (alfa) y la corta en una lista de frames.
    Automáticamente escala los frames al tamaño TAMANO_CELDA.
    """
    # Usamos convert_alpha() para transparencia nítida
    imagen_completa = pygame.image.load(ruta_archivo).convert_alpha()
    ancho_completo, alto_completo = imagen_completa.get_size()
    
    ancho_frame = ancho_completo // columnas
    alto_frame = alto_completo // filas
    
    frames = []
    
    for f in range(filas):
        for c in range(columnas):
            # Recortamos cada frame individual
            rect = pygame.Rect(c * ancho_frame, f * alto_frame, ancho_frame, alto_frame)
            
            # Creamos superficie vacía y copiamos el trozo
            frame_superficie = pygame.Surface((ancho_frame, alto_frame), pygame.SRCALPHA)
            frame_superficie.blit(imagen_completa, (0, 0), rect)
            
            # Escalamos al tamaño exacto de tu celda del laberinto
            frame_escalado = pygame.transform.scale(frame_superficie, (TAMANO_CELDA, TAMANO_CELDA))
            frames.append(frame_escalado)
            
    return frames

# --- Carga de Assets Pro ---
# Guardamos la cuadrícula de 4x4 en una lista plana de 16 frames.
try:
    # Esta es la ruta exacta según la estructura de carpetas de arriba
    HOJA_JUGADOR_PRO = cargar_sprite_sheet('assets/sprites/chica_pro.png', filas=4, columnas=4)
except FileNotFoundError:
    print("Error: No se encontró la imagen en 'assets/sprites/chica_pro.png'")
    # Fallback rápido: un rectángulo verde si no encuentra la imagen
    HOJA_JUGADOR_PRO = [pygame.Surface((TAMANO_CELDA, TAMANO_CELDA))]
    HOJA_JUGADOR_PRO[0].fill((0, 255, 0)) # VERDE_JUGADOR


def dibujar_jugador_completo(pantalla, logica_x, logica_y, frame_actual, tipo_animacion=0):
    """
    Dibuja al jugador usando la hoja de sprites completa de 4x4.
    
    tipo_animacion (Índice de Fila, 0-3):
        0 = Caminata Lateral Derecha (Original) (Row 1)
        1 = Caminata Top-Down (Row 2) - Útil para laberintos
        2 = Daño Sobrenatural - Fuego (Row 3)
        3 = Daño Sobrenatural - Agua (Row 4)
        
    frame_actual (Índice de Columna, 0-3): Índice de animación en esa fila.
    """
    x_pixel = logica_x * TAMANO_CELDA
    y_pixel = logica_y * TAMANO_CELDA
    
    # Calculamos el índice base: (tipo_animacion * columnas_totales)
    # columnas_totales es 4 en nuestra hoja
    indice_base = (tipo_animacion % 4) * 4 # Asegura que esté entre 0-3 y multiplique
    
    # Nos aseguramos de que el frame_actual esté entre 0 y 3
    # Luego sumamos al indice_base para obtener el frame final (0-15)
    frame_final = indice_base + (frame_actual % 4)
    
    # Obtenemos el frame escalado
    sprite_a_dibujar = HOJA_JUGADOR_PRO[frame_final]
    
    pantalla.blit(sprite_a_dibujar, (x_pixel, y_pixel))

def dibujar_laberinto(pantalla, matriz):
    """
    Lee la matriz de DEV_1 y dibuja los bloques.
    1 = Pared, 3 = Meta, 4 = Trampa, 0/2 = Camino
    """
    pantalla.fill(NEGRO) # Fondo negro por defecto
    
    for fila in range(len(matriz)):
        for col in range(len(matriz[fila])):
            valor = matriz[fila][col]
            
            x_pixel = col * TAMANO_CELDA
            y_pixel = fila * TAMANO_CELDA
            rect = pygame.Rect(x_pixel, y_pixel, TAMANO_CELDA, TAMANO_CELDA)
            
            if valor == 1: # Pared
                pygame.draw.rect(pantalla, GRIS_PARED, rect)
            elif valor == 3: # Meta (la ponemos de color dorado)
                pygame.draw.rect(pantalla, (255, 215, 0), rect) 
            elif valor == 4: # Trampa (la ponemos roja oscura, si quieren hacerla visible)
                pygame.draw.rect(pantalla, (139, 0, 0), rect)

def actualizar_pantalla():
    pygame.display.flip()