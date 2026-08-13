from src.core.validacion import es_posicion_valida

class JugadorLogica:
    def __init__(self, fila_inicial, col_inicial):
        self.fila = fila_inicial
        self.columna = col_inicial
        self.vida = 100
        
        self.carga_extintor = 10 
        self.carga_maxima = 10   
        
        self.esta_vivo = True
        self.ha_ganado = False
        
        # Guardamos la dirección: (d_fila, d_columna). Por defecto mira hacia abajo.
        self.direccion_mirada = (1, 0)

    def intentar_moverse(self, d_fila, d_col, matriz):
        # Siempre actualizamos hacia dónde mira, incluso si choca con una pared
        if d_fila != 0 or d_col != 0:
            self.direccion_mirada = (d_fila, d_col)
            
        nueva_f = self.fila + d_fila
        nueva_c = self.columna + d_col
        
        if es_posicion_valida(nueva_f, nueva_c, matriz):
            self.fila = nueva_f
            self.columna = nueva_c
            self._verificar_eventos_casilla(matriz)
            return True
        return False

    def usar_extintor(self, matriz):
        """Dispara en un área de 3x2 inteligente que se adapta al pasillo."""
        if self.carga_extintor <= 0:
            return [] # No hay cargas
            
        self.carga_extintor -= 1
        df, dc = self.direccion_mirada
        celdas_afectadas = []
        
        # 1. Determinar hacia qué lado ensanchar el disparo (buscamos la otra mitad del pasillo)
        ancho_offsets = [0] # Siempre disparamos en la línea donde estamos parados
        
        if df != 0: # Mirando Verticalmente (Arriba o Abajo)
            # Buscamos a la derecha o izquierda para ver dónde está el pasillo
            if es_posicion_valida(self.fila, self.columna + 1, matriz):
                ancho_offsets.append(1)
            elif es_posicion_valida(self.fila, self.columna - 1, matriz):
                ancho_offsets.append(-1)
                
            # 2. Proyectar 3 cuadros de largo por los 2 de ancho
            for profundidad in range(1, 4):
                for ancho in ancho_offsets:
                    celdas_afectadas.append((self.fila + (df * profundidad), self.columna + ancho))
                    
        else: # Mirando Horizontalmente (Izquierda o Derecha)
            # Buscamos arriba o abajo para ver dónde está el pasillo
            if es_posicion_valida(self.fila + 1, self.columna, matriz):
                ancho_offsets.append(1)
            elif es_posicion_valida(self.fila - 1, self.columna, matriz):
                ancho_offsets.append(-1)
                
            # 2. Proyectar 3 cuadros de largo por los 2 de ancho
            for profundidad in range(1, 4):
                for ancho in ancho_offsets:
                    celdas_afectadas.append((self.fila + ancho, self.columna + (dc * profundidad)))

        # 3. Apagar el fuego y crear zona incombustible (el valor 7)
        for f, c in celdas_afectadas:
            if 0 <= f < len(matriz) and 0 <= c < len(matriz[0]):
                if matriz[f][c] == 5:
                    matriz[f][c] = 7
                    
        return celdas_afectadas

    def _verificar_eventos_casilla(self, matriz):
        valor_casilla = matriz[self.fila][self.columna]
        
        if valor_casilla == 3: 
            self.ha_ganado = True
        elif valor_casilla == 6: 
            self.carga_extintor = self.carga_maxima 
            matriz[self.fila][self.columna] = 0     
        elif valor_casilla == 4: 
            self.vida -= 15
        elif valor_casilla == 5: 
            # Recibes daño si pisas fuego sin apagarlo
            self.vida -= 1                     
                
        if self.vida <= 0:
            self.vida = 0
            self.esta_vivo = False

            # Comentario UwU