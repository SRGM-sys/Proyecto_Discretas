# DEV_1/test_logica.py
import sys
import os
# Ajuste de rutas para que Python encuentre los módulos si lo corres desde adentro
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DEV_1.generador_dfs import generar_laberinto
from DEV_1.trampas import inyectar_trampas
from config import FILAS, COLUMNAS

# 1. Generar mapa y añadir trampas
mi_matriz = generar_laberinto(FILAS, COLUMNAS)
mi_matriz = inyectar_trampas(mi_matriz, 5) # 5 trampas de prueba

# 2. Imprimir en consola de forma legible
for fila in mi_matriz:
    # Convertimos los números a strings para imprimirlos juntos
    print(" ".join(map(str, fila)))