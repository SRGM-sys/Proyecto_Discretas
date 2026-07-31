# DEV_1/jugador_logica.py
from DEV_1.validacion import es_posicion_valida

class JugadorLogica:
    def __init__(self, fila_inicial, col_inicial):
        self.fila = fila_inicial
        self.columna = col_inicial
        self.vida = 100
        # Mecánica de Extintor: Empieza con 1 uso, puede almacenar hasta 3
        self.carga_extintor = 1 
        self.carga_maxima = 3   
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
            
        elif valor_casilla == 6: # Pisó un punto de recarga
            self.carga_extintor = self.carga_maxima # Llena el tanque al máximo
            matriz[self.fila][self.columna] = 0     # Consume la recarga del mapa
            
        elif valor_casilla == 4: # Obstáculo
            self.vida -= 15
            
        elif valor_casilla == 5: # Fuego
            if self.carga_extintor > 0:
                self.carga_extintor -= 1            # Gasta una carga
                matriz[self.fila][self.columna] = 0 # Apaga el fuego (lo vuelve camino)
            else:
                self.vida -= 1                     # Sin cargas, recibe daño directo
            
        if self.vida <= 0:
            self.vida = 0
            self.esta_vivo = False