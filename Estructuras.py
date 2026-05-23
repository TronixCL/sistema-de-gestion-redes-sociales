# ==============================================================================
# 1. MODELO DE DATOS EN MEMORIA DINÁMICA (Relación 1 a N)
# ==============================================================================
class Post:
    def __init__(self, id_post, texto):
        self.id_post = id_post
        self.texto = texto
        self.siguiente = None  # Enlace para la sublista de posts del usuario

class Usuario:
    def __init__(self, username):
        self.username = username
        self.cabeza_posts = None  # Cabeza de la sublista enlazada de objetos Post
        self.siguiente = None
        
    def agregar_post(self, id_post, texto):
        nuevo_post = Post(id_post, texto)
        nuevo_post.siguiente = self.cabeza_posts
        self.cabeza_posts = nuevo_post
        return nuevo_post  # Retorna la referencia al objeto creado

# ==============================================================================
# 2. ÍNDICE INVERTIDO DE PALABRAS (Conteo de Frecuencias)
# ==============================================================================
class NodoPosteoPalabra:
    def __init__(self, post_obj):
        self.post = post_obj  # Referencia al objeto Post real
        self.frecuencia = 1   # Contador de apariciones
        self.siguiente = None

class ListaPosteosPalabra:
    def __init__(self):
        self.cabeza = None

    def registrar_aparicion(self, post_obj):
        actual = self.cabeza
        while actual is not None:
            if actual.post.id_post == post_obj.id_post:
                actual.frecuencia += 1  
                return
            actual = actual.siguiente
            
        nuevo_nodo = NodoPosteoPalabra(post_obj)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo

    def mostrar(self):
        actual = self.cabeza
        if actual is None:
            print("[-] No hay publicaciones asociadas.")
            return
        while actual is not None:
            print(f" -> Post ID: [{actual.post.id_post}] | Frecuencia: {actual.frecuencia} vez/veces")
            actual = actual.siguiente

class NodoPalabra:
    def __init__(self, palabra):
        self.palabra = palabra
        self.lista_posteos = ListaPosteosPalabra()
        self.siguiente = None

class IndicePalabras:
    def __init__(self):
        self.cabeza = None

    def registrar_palabra(self, palabra, post_obj):
        actual = self.cabeza
        while actual is not None:
            if actual.palabra == palabra:
                actual.lista_posteos.registrar_aparicion(post_obj)
                return
            actual = actual.siguiente

        nuevo_nodo_palabra = NodoPalabra(palabra)
        nuevo_nodo_palabra.lista_posteos.registrar_aparicion(post_obj)
        nuevo_nodo_palabra.siguiente = self.cabeza
        self.cabeza = nuevo_nodo_palabra

    def buscar_palabra(self, palabra):
        actual = self.cabeza
        while actual is not None:
            if actual.palabra == palabra:
                print(f"\n[+] Resultados en el Índice Invertido para '{palabra}':")
                actual.lista_posteos.mostrar()
                return
            actual = actual.siguiente
        print(f"\n[-] La palabra '{palabra}' no se encuentra registrada.")

# ==============================================================================
# 3. ÍNDICE INVERTIDO SOCIAL (Relación de Contactos y Contador de Posts)
# ==============================================================================
class NodoSimple:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaContactos:
    def __init__(self):
        self.cabeza = None

    def insertar_sin_duplicado(self, dato):
        actual = self.cabeza
        while actual is not None:
            if actual.dato == dato:
                return  
            actual = actual.siguiente
            
        nuevo_nodo = NodoSimple(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo

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
        self.lista_amigos = ListaContactos()
        self.cantidad_posts = 0  # Contador de posts asociados en memoria
        self.siguiente = None

class IndiceUsuariosSocial:
    def __init__(self):
        self.cabeza = None

    def registrar_contacto(self, username, contacto):
        actual = self.cabeza
        while actual is not None:
            if actual.username == username:
                actual.cantidad_posts += 1  
                if contacto:
                    actual.lista_amigos.insertar_sin_duplicado(contacto)
                return
            actual = actual.siguiente

        nuevo_nodo_usuario = NodoUsuarioSocial(username)
        nuevo_nodo_usuario.cantidad_posts = 1  
        if contacto:
            nuevo_nodo_usuario.lista_amigos.insertar_sin_duplicado(contacto)
        nuevo_nodo_usuario.siguiente = self.cabeza
        self.cabeza = nuevo_nodo_usuario

    def buscar_amigos(self, username):
        actual = self.cabeza
        while actual is not None:
            if actual.username == username:
                print(f"\n[+] Perfil detectado para '{username}':")
                print(f" -> Cantidad de publicaciones asociadas: {actual.cantidad_posts}")
                print(f" -> Red de contactos enlazada:")
                actual.lista_amigos.mostrar()
                return
            actual = actual.siguiente
        print(f"\n[-] El usuario '{username}' no tiene registros en el índice social.")