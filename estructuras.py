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

    def insertar_inicio(self, dato): # O(1) al inicio
        # Crea un nuevo nodo con el dato y lo inserta al inicio de la lista
        # El nuevo nodo apunta al nodo que ERA la cabeza,
        # y luego la cabeza se actualiza para ser el nuevo nodo
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        # Incrementa el tamaño de la lista cada vez que se inserta un nuevo nodo
        self.tamaño += 1 
    
    def insertar_final(self, dato): # O(n) cada que se agrega un nuevo nodo
        # Misma creacion que la insercion del inicio,
        # con la diferencia que el nuevo nodo se inserta al final de la lista
        # si la lisa esta vacía, el nuevo nodo se convierte en la cabeza
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            # Recorre la lista hasta llegar al último nodo
            while actual.siguiente: 
                # actual.siguiente es el nodo que apunta al siguiente nodo
                actual = actual.siguiente 
                if actual.siguiente is None:
                    break
            actual.siguiente = nuevo_nodo
        self.tamaño += 1
    
    def buscar(self,dato): # O(n)
        # Busca si un dato existe en la lista
        actual = self.cabeza
        while actual:
            if actual.dato == dato:
                return True
            actual = actual.siguiente
        return False

    def eliminar(self, dato): # O(n)
        # Elimina el primer nodo que contiene el dato especificado
        # Si la lista está vacía, no se puede eliminar
        if not self.cabeza:
            return False 
        
        # si el dato a eliminar es el de la cabeza,
        # la cabeza se actualiza para ser el siguiente nodo
        # y el tamaño de la lista se decrementa
        if self.cabeza.dato == dato:
            self.cabeza = self.cabeza.siguiente
            self.tamaño -= 1
            return True
        
        # Si el dato a eliminarno es de la cabeza,
        # se recorre la lista buscando el nodo que contiene
        # el dato a eliminar, y se actualizan los punteros para saltar el nodo eliminado
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self.tamaño -= 1
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

    def __len__(self):
        # Retorna el tamaño de la lista
        return self.tamaño
