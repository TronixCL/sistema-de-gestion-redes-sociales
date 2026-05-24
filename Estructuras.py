# ==============================================================================
# 1. MODELO DE DATOS EN MEMORIA DINÁMICA 
# ==============================================================================
class Post:
    def __init__(self, idPost, texto):
        self.idPost = idPost
        self.texto = texto
        self.siguiente = None  # Enlace para la sublista de posts del usuario

class Usuario:
    def __init__(self, username):
        self.username = username
        self.cabezaPosts = None  # Cabeza de la sublista enlazada de objetos Post
        self.siguiente = None
        
    def agregarPost(self, idPost, texto):
        nuevoPost = Post(idPost, texto)
        nuevoPost.siguiente = self.cabezaPosts
        self.cabezaPosts = nuevoPost
        return nuevoPost  # Retorna la referencia al objeto creado

# ==============================================================================
# 2. ÍNDICE INVERTIDO DE PALABRAS 
# ==============================================================================
class NodoPosteoPalabra:
    def __init__(self, postObj):
        self.post = postObj  # Referencia al objeto Post real
        self.frecuencia = 1   # Contador de apariciones
        self.siguiente = None

class ListaPosteosPalabra:
    def __init__(self):
        self.cabeza = None

    def registrarAparicion(self, postObj):
        actual = self.cabeza
        while actual is not None:
            if actual.post.idPost == postObj.idPost:
                actual.frecuencia += 1  
                return
            actual = actual.siguiente
            
        nuevoNodo = NodoPosteoPalabra(postObj)
        nuevoNodo.siguiente = self.cabeza
        self.cabeza = nuevoNodo

    def mostrar(self):
        actual = self.cabeza
        if actual is None:
            print("[-] No hay publicaciones asociadas.")
            return
        while actual is not None:
            print(f" -> Post ID: [{actual.post.idPost}] | Frecuencia: {actual.frecuencia} vez/veces")
            actual = actual.siguiente

class NodoPalabra:
    def __init__(self, palabra):
        self.palabra = palabra
        self.listaPosteo = ListaPosteosPalabra()
        self.siguiente = None

class IndicePalabras:
    def __init__(self):
        self.cabeza = None

    def registrarPalabra(self, palabra, postObj):
        actual = self.cabeza
        while actual is not None:
            if actual.palabra == palabra:
                actual.listaPosteo.registrarAparicion(postObj)
                return
            actual = actual.siguiente

        nuevoNodoPalabra = NodoPalabra(palabra)
        nuevoNodoPalabra.listaPosteo.registrarAparicion(postObj)
        nuevoNodoPalabra.siguiente = self.cabeza
        self.cabeza = nuevoNodoPalabra

    def buscarPalabra(self, palabra):
        actual = self.cabeza
        while actual is not None:
            if actual.palabra == palabra:
                print(f"\n[+] Resultados en el Índice Invertido para '{palabra}':")
                actual.listaPosteo.mostrar()
                return
            actual = actual.siguiente
        print(f"\n[-] La palabra '{palabra}' no se encuentra registrada.")

# ==============================================================================
# 3. ÍNDICE INVERTIDO SOCIAL 
# ==============================================================================
class NodoSimple:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaContactos:
    def __init__(self):
        self.cabeza = None

    def insertarSinDuplicado(self, dato):
        actual = self.cabeza
        while actual is not None:
            if actual.dato == dato:
                return  
            actual = actual.siguiente
            
        nuevoNodo = NodoSimple(dato)
        nuevoNodo.siguiente = self.cabeza
        self.cabeza = nuevoNodo

    def mostrar(self):
        elementos = []
        actual = self.cabeza
        while actual is not None:
            elementos.append(str(actual.dato))
            actual = actual.siguiente
        if not elementos:
            print(" -> Sin contactos registrados -> NULL")
        else:
            print(" -> " + " -> ".join(elementos) + " -> NULL")

class NodoUsuarioSocial:
    def __init__(self, username):
        self.username = username
        self.listaAmigos = ListaContactos()
        self.cantidadPosts = 0  # Contador de posts asociados en memoria
        self.siguiente = None

class IndiceUsuariosSocial:
    def __init__(self):
        self.cabeza = None

    def registrarContacto(self, username, contacto):
        actual = self.cabeza
        while actual is not None:
            if actual.username == username:
                actual.cantidadPosts += 1  
                if contacto:
                    actual.listaAmigos.insertarSinDuplicado(contacto)
                return
            actual = actual.siguiente

        nuevoNodoUsuario = NodoUsuarioSocial(username)
        nuevoNodoUsuario.cantidadPosts = 1  
        if contacto:
            nuevoNodoUsuario.listaAmigos.insertarSinDuplicado(contacto)
        nuevoNodoUsuario.siguiente = self.cabeza
        self.cabeza = nuevoNodoUsuario

    def buscarAmigos(self, username):
        actual = self.cabeza
        while actual is not None:
            if actual.username == username:
                print(f"\n[+] Perfil detectado para '{username}':")
                print(f" -> Cantidad de publicaciones asociadas: {actual.cantidadPosts}")
                print(f" -> Red de contactos enlazada:")
                actual.listaAmigos.mostrar()
                return
            actual = actual.siguiente
        print(f"\n[-] El usuario '{username}' no tiene registros en el índice social.")