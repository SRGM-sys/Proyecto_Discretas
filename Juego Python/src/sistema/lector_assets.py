# DEV_2/lector_assets.py
import pygame
import os

def inicializar_audio():
    """Inicializa el mezclador y reproduce la música de fondo en bucle."""
    pygame.mixer.init()
    try:
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_src = os.path.dirname(ruta_actual)
        ruta_raiz = os.path.dirname(ruta_src)
        ruta_musica = os.path.join(ruta_raiz, 'assets', 'sonidos', 'Liella! - Vitamin SUMMER!  [Karaoke].mp3')
        
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        print("¡Música de fondo cargada con éxito!")
    except Exception as e:
        print(f"Aviso: No se pudo cargar la música de fondo. Error: {e}")