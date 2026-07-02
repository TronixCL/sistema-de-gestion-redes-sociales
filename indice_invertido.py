import csv
import os
from estructuras import ListaEnlazada

def cargar_stopwords(archivo=os.path.dirname(os.path.abspath(__file__)) + '/stopwords.txt'):
    stopwords = set()
    with open(archivo, 'r', encoding='utf-8') as filtro:
            for linea in filtro:
                linea = linea.strip().lower()
                # Ignorar líneas vacías y comentarios
                if linea and not linea.startswith('#'):
                    stopwords.add(linea)
    print(f"Cargadas {len(stopwords)} stopwords desde {archivo}")
    return stopwords
# Se deja como variable globar para evitar cargar el archivo cada vez que se indexa un termino
STOPWORDS = cargar_stopwords()

class IndiceInvertido:
    # Estructura principal del indice invertido
    def __init__(self):
        self.indice = {}

    def indexar(self, termino, id_elemento):
        # Agrega un elemento al indice para un término dado
        termino = termino.lower().strip()
        if not termino or termino in STOPWORDS:
            return
     
        if termino not in self.indice:
            self.indice[termino] = ListaEnlazada()

        # Agregar el inicio para O(1) - documentos más recientes primero
        if not self.indice[termino].buscar(id_elemento):
            self.indice[termino].insertar(id_elemento)
    
    def buscar(self, termino):
        # Retorna la lisa enlazada de elemntos que contiene el termino
        termino = termino.lower().strip()
        if termino in self.indice:
            return self.indice[termino]
        return ListaEnlazada()
    
    def mostrar_indice(self):
        # Muestra el indice (para depurar)
        for termino, lista in self.indice.items():
            print(f"{termino}: {lista.recorrer()}")

class Usuario:
    # Modelo de usuario con lista enlazada de seguidores
    def __init__(self, owner_id, username):
        self.owner_id = owner_id
        self.username = username
        self.seguidores = ListaEnlazada()

    def agregar_seguidor(self, username_seguidor):
    # Agrega un seguidor a la lista enlazada del usuario
        self.seguidores.insertar(username_seguidor)


    def obtener_seguidores(self):
        # Retorna lista de IDs de amigos
        return self.seguidores.recorrer()
    
class Post:
    # Modelo de post con su contenido
    def __init__(self, shortcode, username, caption, likes):
        self.shortcode = shortcode
        self.username = username
        self.caption = caption
        self.likes = likes


class ProcesadorDataset:
    # Carga y procesa el dataset construyendo los indices

    def __init__(self, archivo_csv):
        self.archivo = archivo_csv
        self.usuarios = {} # owner_id -> Usuario
        self.posts = {} # shortcode -> post 
        self.indice_posts = IndiceInvertido()

    def limpiar_texto(self, texto):
        # Limpia y tokeniza un texto, eliminando stopwords
        if not texto or texto == 'None':
            return []
        
        # Convertir a minúsculas y eliminar puntuación
        texto = texto.lower()
       
        # Tokenizar y filtrar stopwords
        palabras = texto.split()
        return [p for p in palabras if p not in STOPWORDS and len(p) > 2 and p.isalpha()]
    
    def procesar_lista_followers(self, lista_str):
        # Convierte string de lista de followers a lista Python
        if not lista_str or lista_str == '[]' or lista_str == "[]":
            return []
        
        # Limpiar la cadena: eliminar corchetes y comillas
        lista_str = lista_str.strip('[]')
        if not lista_str:
            return []
        
        # Dividir por comas y limpiar
        followers = [f.strip().strip("'\"") for f in lista_str.split(',')]
        return followers
    
    def cargar_datos(self):
        # Carga el archivo CSV y construye todas las estructuras
        print("Cargando dataset:\n")
        ruta_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.archivo)
        with open(ruta_csv, 'r', encoding='utf-8') as archivo:
            # Detectar el delimitador (CSV puede ser coma o punto y coma)
            muestra = archivo.readline()
            archivo.seek(0)
            
            if ';' in muestra:
                lector = csv.DictReader(archivo, delimiter=';')
            else:
                lector = csv.DictReader(archivo, delimiter=',')
            
            contador = 0
            for fila in lector:
                # Extraer datos
                owner_id = fila.get('owner_id', '')
                owner_username = fila.get('owner_username', '')
                shortcode = fila.get('shortcode', '')
                caption = fila.get('caption', '')
                likes = fila.get('likes', '0')
                followers_str = fila.get('followers', '[]')
                
                # Crear usuario si no existe
                if owner_id not in self.usuarios:
                    self.usuarios[owner_id] = Usuario(owner_id, owner_username)
                
                # Procesar followers como amigos
                followers_list = self.procesar_lista_followers(followers_str)
                for follower in followers_list: 
                    self.usuarios[owner_id].agregar_seguidor(follower)
                
                # Crear post
                if shortcode:
                    post = Post(shortcode, owner_username, caption, likes)
                    self.posts[shortcode] = post
                    
                    # Indexar términos del caption
                    terminos = self.limpiar_texto(caption)
                    for termino in terminos:
                        self.indice_posts.indexar(termino, shortcode)
                
                contador += 1
                if contador % 100 == 0:
                    print(f"  Procesados {contador} registros")
        
        print(f"\nRegistros leidos")
        print(f"  Usuarios: {len(self.usuarios)}")
        print(f"  Posts: {len(self.posts)}")
        print(f"  Términos indexados: {len(self.indice_posts.indice)}")
    
    def buscar_posts_por_termino(self, termino):
        # Busca posts que contengan un término
        lista_posts = self.indice_posts.buscar(termino)
        return lista_posts.recorrer()
    
    def obtener_seguidores_de_usuario(self, usuario_id):
        # Obtiene lista de seguidores de un usuario
        if usuario_id in self.usuarios:
            return self.usuarios[usuario_id].obtener_seguidores()
        return []
    
    def mostrar_post(self, shortcode):
        # Muestra información de un post
        if shortcode in self.posts:
            post = self.posts[shortcode]
            print(f"\nPost: {post.shortcode}")
            print(f" Autor: {post.username}")
            print(f" Likes: {post.likes}")
            print(f" Caption: {post.caption[:100]}...")
            return True
        print(f"  Post '{shortcode}' no encontrado.")
        return False

class RedSocial:
    # Interfaz del sistema
    os.system('cls')
    def __init__(self, archivo_dataset):
        print("Sistema de índice invertido\n")
        self.procesador = ProcesadorDataset(archivo_dataset)
        self.procesador.cargar_datos()
    
    def menu(self):
        # Menú principal interactivo
        while True:
            print("\nMenú principal\n")
            print("1. Buscar posts por palabra clave")
            print("2. Ver seguidores de un usuario")
            print("3. Salir")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == '1':
                self.buscar_por_palabra()
            elif opcion == '2':
                self.ver_seguidores()
            elif opcion == '3':
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida, intente de nuevo")
    
    def buscar_por_palabra(self):
        # Búsqueda por una palabra 
        termino = input("Ingrese la palabra a buscar: ").strip()
        if not termino:
            return
        
        resultados = self.procesador.buscar_posts_por_termino(termino)
        
        print(f"\nResultados para '{termino}': {len(resultados)} posts encontrados")
        if resultados:
            print("\nResultados encontrados:")
            # se utiliza el enumerar resultado porque lo que arroja resultados son los captions en si
            for shortcode in resultados:
                self.procesador.mostrar_post(shortcode)
        elif termino in STOPWORDS:
            print(f" La palabra '{termino}' es una stopword y no se indexa. ")
        else:
            print(f" No hay posts con la palabra '{termino}'.")

    def ver_seguidores(self):
        # Ver seguidores de un usuario
        entrada = input("Ingrese el ID del usuario: ").strip()
        if not entrada:
            return

        usuario_id = None
        if entrada in self.procesador.usuarios:
            usuario_id = entrada
        else:
            for uid, usr in self.procesador.usuarios.items():
                if usr.username == entrada:
                    usuario_id = uid
                    break
        
        if not usuario_id:
            print(f" Usuario '{entrada}' no encontrado.")
            return

        seguidores = self.procesador.obtener_seguidores_de_usuario(usuario_id)
        usr = self.procesador.usuarios[usuario_id]
        print(f"\n Usuario: @{usr.username} (ID: {usr.owner_id})")
        print(f"Seguidores ({len(seguidores)}):")
        for i, seguidor in enumerate(seguidores[:20], 1):
            print(f"  {i}. @{seguidor}")
        if len(seguidores) > 20:
            print(f"  ... y {len(seguidores) - 20} más")


# Punto de entrada principal
if __name__ == "__main__":
    # Crear y ejecutar la red social
    app = RedSocial("dataset_curado.csv")
    app.menu()
