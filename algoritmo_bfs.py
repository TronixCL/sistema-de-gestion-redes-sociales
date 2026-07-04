def obtener_grados_conexion(grafo, usuario_raiz):
    id_raiz = grafo.normalizar_id(usuario_raiz)

    contactos_1 = set()
    contactos_2 = set()
    contactos_3 = set()

    todos_agregados = {id_raiz}
    cola = [(id_raiz, 0)]

    while cola:
        u, nivel = cola.pop(0)

        if nivel >= 3:
            continue

        amigos = grafo.obtener_contactos_directos(u)

        for v in amigos:
            if v not in todos_agregados:
                todos_agregados.add(v)
                nuevo_nivel = nivel + 1

                if nuevo_nivel == 1:
                    contactos_1.add(v)
                elif nuevo_nivel == 2:
                    contactos_2.add(v)
                elif nuevo_nivel == 3:
                    contactos_3.add(v)

                cola.append((v, nuevo_nivel))

    return contactos_1, contactos_2, contactos_3