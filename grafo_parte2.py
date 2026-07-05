from estructuras import ListaEnlazada 

class GrafoRedSocial:
    def __init__(self, procesador):
        self.procesador = procesador
        self.vertices = self.procesador.usuarios

        # Diccionario traductor para buscar IDs por username en O(1)
        self.username_a_id = {}
        for uid, usr in self.vertices.items():
            self.username_a_id[usr.username] = uid

        # Lista de Adyacencia: id_usuario -> ListaEnlazada de ids vecinos
        self.lista_adyacencia = {}
        self.construir_lista_adyacencia()

    def construir_lista_adyacencia(self):
        # Se construye una sola vez al crear el grafo
        for uid in self.vertices:
            vecinos = ListaEnlazada()
            seguidores_raw = self.procesador.obtener_seguidores_de_usuario(uid)

            for seguidor in seguidores_raw:
                id_vecino = self.normalizar_id(seguidor)
                # Evita duplicados dentro de la lista de un mismo vértice
                if not vecinos.buscar(id_vecino):
                    vecinos.insertar(id_vecino)

            self.lista_adyacencia[uid] = vecinos

    def normalizar_id(self, identificador):
        
        return self.username_a_id.get(identificador, identificador)

    def obtener_contactos_directos(self, identificador):
        id_usuario = self.normalizar_id(identificador)

        if id_usuario not in self.lista_adyacencia:
            return []

        # Convierte la ListaEnlazada a lista Python para que el BFS la recorra normal
        return self.lista_adyacencia[id_usuario].recorrer()

    def validar_grafo(self):
        total_usuarios = len(self.vertices)
        return total_usuarios
    
    def validar_simetria(self):
        # Recorre toda la lista de adyacencia y confirma que cada relacion
        # sea reciproca: si A tiene a B como vecino, B debe tener a A
        inconsistencias = []
        for uid, vecinos in self.lista_adyacencia.items():
            for vecino_id in vecinos.recorrer():
                vecinos_del_vecino = self.lista_adyacencia.get(vecino_id)
                if vecinos_del_vecino is None or not vecinos_del_vecino.buscar(uid):
                    inconsistencias.append((uid, vecino_id))
        return inconsistencias
    
    def validar_sin_bucles(self):
        # Recorre la lista de adyacencia y confirma que ningun usuario
        # se tenga a si mismo como vecino (bucle / self-loop)
        bucles = []
        for uid, vecinos in self.lista_adyacencia.items():
            if vecinos.buscar(uid):
                bucles.append(uid)
        return bucles