class Nodo:

    def __init__(self, dato):
        self.dato = dato         
        self.siguiente = None    


class ListaEnlazada:

    def __init__(self):
        self.cabeza = None

    def insertar(self, dato):
        nuevo_nodo = Nodo(dato)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            return

        actual = self.cabeza
        while actual is not None:

            if actual.dato == dato:
                return  
            
            if actual.siguiente is None:
                break
                
            actual = actual.siguiente

        actual.siguiente = nuevo_nodo

    def mostrar(self):
  
        elementos = []
        actual = self.cabeza
        
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
            
        print(" -> ".join(elementos) + " -> NULL")


class NodoPalabra:

    def __init__(self, palabra):
        self.palabra = palabra
        self.lista_posts = ListaEnlazada() 
        self.siguiente = None              


class ListaIndice:

    def __init__(self):
        self.cabeza = None

    def registrar_palabra(self, palabra, post_id):

        actual = self.cabeza

        while actual is not None:
            if actual.palabra == palabra:
                actual.lista_posts.insertar(post_id)
                return  
            actual = actual.siguiente

        nuevo_nodo_palabra = NodoPalabra(palabra)
        nuevo_nodo_palabra.lista_posts.insertar(post_id)
        
        nuevo_nodo_palabra.siguiente = self.cabeza
        self.cabeza = nuevo_nodo_palabra

    def buscar_palabra(self, palabra):

        actual = self.cabeza
        while actual is not None:
            if actual.palabra == palabra:
                print(f"\n[+] Resultados para la palabra '{palabra}':")
                actual.lista_posts.mostrar()
                return
            actual = actual.siguiente
            
        print(f"\n[-] La palabra '{palabra}' no se encontró en el índice.")