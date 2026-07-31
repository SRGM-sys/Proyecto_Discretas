# DEV_1/jugador_logica.py
from DEV_1.validacion import es_posicion_valida

class JugadorLogica:
    def __init__(self, fila_inicial, col_inicial):
        self.fila = fila_inicial
        self.columna = col_inicial
        self.vida = 100          # Nueva mecánica: Vida del jugador
        self.esta_vivo = True
        self.ha_ganado = False

    def intentar_moverse(self, d_fila, d_col, matriz):
        nueva_f = self.fila + d_fila
        nueva_c = self.columna + d_col
        
        if es_posicion_valida(nueva_f, nueva_c, matriz):
            self.fila = nueva_f
            self.columna = nueva_c
            self._verificar_eventos_casilla(matriz)
            return True
        return False

    def _verificar_eventos_casilla(self, matriz):
        valor_casilla = matriz[self.fila][self.columna]
        
        if valor_casilla == 3: 
            self.ha_ganado = True
        elif valor_casilla == 4: # Pisó un obstáculo (escombro caliente)
            self.vida -= 15
        elif valor_casilla == 5: # Pisó fuego directamente
            self.vida -= 30
            
        # Verificar si murió quemado o por daño
        if self.vida <= 0:
            self.vida = 0
            self.esta_vivo = False