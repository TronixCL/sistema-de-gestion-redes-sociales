class Nodo:
    # Esta clase crea un dato tipo nodo, 
    # el cual se usa como puntero para las direcciones de una lista enlazada
    def __init__(self, dato):
        self.dato = dato         
        self.siguiente = None    

class ListaEnlazada:
    def __init__(self):
        # La cabeza es el primer nodo de la lista,
        # y el tamaño inicia en 0 pq no hay nodos al crear la lista
        self.cabeza = None
        self.tamaño = 0

    def insertar(self, dato): # O(1) al inicio
        # Crea un nuevo nodo con el dato y lo inserta al inicio de la lista
        # El nuevo nodo apunta al nodo que ERA la cabeza,
        # y luego la cabeza se actualiza para ser el nuevo nodo
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        # Incrementa el tamaño de la lista cada vez que se inserta un nuevo nodo
        self.tamaño += 1 
    
    def buscar(self,dato): # O(n)
        # Busca si un dato existe en la lista
        actual = self.cabeza
        while actual:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        # Retorna lista con todos los elementos 
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos
