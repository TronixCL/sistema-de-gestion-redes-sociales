import math
from estructuras import ListaEnlazada

# FUNCION HASH DJB2 

def djb2(cadena):
    # hash(0) = 5381, segun la definicion del enunciado
    hash_val = 5381

    for caracter in cadena:
        # hash(i) = hash(i-1) * 33 + c[i]
        hash_val = (hash_val * 33) + ord(caracter)
        # OBLIGATORIO en Python: truncar a 32 bits en cada iteracion,
        # de lo contrario el entero crece indefinidamente (precision
        # arbitraria) y el rendimiento se degrada
        hash_val &= 0xFFFFFFFF

    return hash_val



# CALCULO DEL TAMAÑO M DE LA TABLA (menor primo >= 1.5 * N)

def es_primo(n):
    # Comprueba si un numero es primo, usado para encontrar M
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def siguiente_primo(n):
    # Retorna el menor numero primo mayor o igual a n
    if n <= 2:
        return 2

    candidato = n if n % 2 != 0 else n + 1
    while not es_primo(candidato):
        candidato += 2

    return candidato


def calcular_tamano_tabla(n_vocabulario):
    # Calcula M como el menor primo que cumple M >= 1.5 * N
    # (factor de carga alpha <= 0.67), segun el enunciado
    # ANTES: se simulaba el redondeo hacia arriba con un if manual
    # AHORA: math.ceil() hace lo mismo en una sola linea, sin duplicar logica
    minimo_requerido = math.ceil(n_vocabulario * 1.5)
    return siguiente_primo(minimo_requerido)



# PAR (termino, contador) que se guarda dentro de cada
# ListaEnlazada de la tabla (esto resuelve el encadenamiento)

class ParFrecuencia:
    def __init__(self, termino, contador=1):
        self.termino = termino
        self.contador = contador



# TABLA HASH PROPIA CON ENCADENAMIENTO SEPARADO

class TablaHash:
    def __init__(self, tamano_m):
        self.m = tamano_m

        # El "arreglo" es una lista Python de tamaño M, pero se usa
        # unicamente como array indexado (no como estructura hash),
        # cada posicion contiene una ListaEnlazada propia
        self.tabla = [ListaEnlazada() for _ in range(tamano_m)]

        # Contadores para las metricas obligatorias
        self.colisiones_totales = 0
        self.terminos_unicos = 0  # esto termina siendo N real insertado

    def _indice_hash(self, termino):
        # Aplica djb2 y reduce el resultado al rango [0, M)
        return djb2(termino) % self.m

    def _buscar_par(self, lista_en_posicion, termino):
        # NUEVO: metodo auxiliar que unifica la busqueda de un par dentro
        # de una lista de una posicion. ANTES esta misma logica estaba
        # repetida por separado en insertar() y en obtener_frecuencia();
        # ahora ambos reutilizan este unico metodo.
        for par in lista_en_posicion.recorrer():
            if par.termino == termino:
                return par
        return None

    def insertar(self, termino):
        # Inserta una ocurrencia del termino: si ya existe, incrementa
        # su contador; si no existe, crea un nuevo par en la lista
        # enlazada de esa posicion (si la lista ya tenia elementos,
        # se cuenta como colision)
        indice = self._indice_hash(termino)
        lista_en_posicion = self.tabla[indice]

        par_existente = self._buscar_par(lista_en_posicion, termino)
        if par_existente is not None:
            par_existente.contador += 1  # ya existe: solo se incrementa
            return

        # No existia: si la lista ya tenia algun elemento, es una colision.
        # Se usa lista_en_posicion.tamaño (atributo ya trackeado por
        # ListaEnlazada) en vez de volver a recorrer la lista para contar
        if lista_en_posicion.tamaño > 0:
            self.colisiones_totales += 1

        nuevo_par = ParFrecuencia(termino, 1)
        lista_en_posicion.insertar(nuevo_par)
        self.terminos_unicos += 1

    def top_n(self, n):
        # Recorre TODA la tabla, junta todos los pares (termino, contador)
        # y retorna los n con mayor frecuencia, ordenados descendente.
        # NOTA: sorted() es una funcion de ordenamiento de Python, no una
        # estructura hash, por lo que no viola la restriccion del enunciado
        # (la restriccion aplica solo a dict/HashMap/unordered_map).
        todos_los_pares = []
        for lista_en_posicion in self.tabla:
            todos_los_pares.extend(lista_en_posicion.recorrer())

        ordenados = sorted(todos_los_pares, key=lambda par: par.contador, reverse=True)

        return [(par.termino, par.contador) for par in ordenados[:n]]

    def calcular_metricas(self):
        # Calcula y retorna: N, M, factor de carga, colisiones totales,
        # largo maximo de cadena y largo promedio de cadena
        largos_todas_las_posiciones = [lista.tamaño for lista in self.tabla]
        largos_ocupados = [largo for largo in largos_todas_las_posiciones if largo > 0]

        largo_maximo = max(largos_todas_las_posiciones) if largos_todas_las_posiciones else 0
        largo_promedio = (sum(largos_ocupados) / len(largos_ocupados)) if largos_ocupados else 0
        factor_carga = self.terminos_unicos / self.m

        return {
            "n_vocabulario": self.terminos_unicos,
            "m_tabla": self.m,
            "factor_carga": factor_carga,
            "colisiones_totales": self.colisiones_totales,
            "largo_maximo_cadena": largo_maximo,
            "largo_promedio_cadena": largo_promedio,
        }
