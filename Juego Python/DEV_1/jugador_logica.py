# DEV_1/jugador_logica.py
from DEV_1.validacion import es_posicion_valida

class JugadorLogica:
    def __init__(self, fila_inicial, col_inicial):
        self.fila = fila_inicial
        self.columna = col_inicial
        self.esta_vivo = True
        self.ha_ganado = False

    def intentar_moverse(self, d_fila, d_col, matriz):
        """
        DEV 2 llamará esto cuando detecte una tecla.
        Ejemplo moverse arriba: intentar_moverse(-1, 0, matriz)
        """
        nueva_f = self.fila + d_fila
        nueva_c = self.columna + d_col
        
        if es_posicion_valida(nueva_f, nueva_c, matriz):
            self.fila = nueva_f
            self.columna = nueva_c
            self._verificar_eventos_casilla(matriz)
            return True # Se movió
        return False # Chocó con pared

    def _verificar_eventos_casilla(self, matriz):
        """Revisa qué pisó el jugador"""
        valor_casilla = matriz[self.fila][self.columna]
        
        if valor_casilla == 3: # Pisó la meta
            self.ha_ganado = True
        elif valor_casilla == 4: # Pisó trampa
            self.esta_vivo = False