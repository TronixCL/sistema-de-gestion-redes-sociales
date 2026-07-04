import os
import csv
import random

# Funcion que filtra y organiza los datos del dataset original
def curarDatos(nombreEntrada: str):
    # obtiene el directorio del preoyecto
    directorio_actual = os.path.dirname(os.path.abspath(__file__)) 
    # Ruta del archivo de entrada
    ruta_entrada = os.path.join(directorio_actual, nombreEntrada) 
    # Ruta del archivo de salida
    ruta_salida = os.path.join(directorio_actual, 'dataset_curadoParaGrafos.csv') 

    # Lista para almacenar los datos curados
    datos_curados = []

    with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
        # Lee y extrae la primera fila para el dataset curado
        lector = csv.reader(archivo)
        header = next(lector)

        # se filtran las columnas relevantes y se agrega la columna al header del dataset curado
        header_filtrado = [header[i] for i in [0, 1, 2, 4, 6]] + ['followers']    
        datos_curados.append(header_filtrado)

        # Conjunto para registrar los owner_id ya procesados
        owner_ids_vistos = set()
        
        # Lee cada fila del CSV como una lista de parametros
        # Si la fila está vacia, saltar a la siguiente iteración
        for parametros in lector:
            if not parametros:
                continue

            # Verifica que la fila tenga los 14 parametros del dataset
            # Donde se extrae el owner_id para validar 
            # la exclusion de owner_ids no numéricos, duplicados y espacios vacios
            # finalmente se agrega el validado al set owner_ids_vistos
            owner_id = parametros[0]
            if not owner_id.isdigit():
                continue
            if owner_id in owner_ids_vistos:
                continue
            owner_ids_vistos.add(owner_id)

                # luego se filtran las columnas relevantes
                # se "limpian" los saltos en fila para despues ser agregados al dataset curado 
            columnas = [0, 1, 2, 4, 6]
            fila_filtrada = [parametros[i].replace('\n', ' ') for i in columnas]
            datos_curados.append(fila_filtrada)

    # al terminar de almacenar el nuevo dataset, se llama a la funcion para agregar amigos
    datos_curados = amigo_aleatorio(datos_curados)

    # Se escribe el nuevo CSV con todo el dataset curado
    with open(ruta_salida, mode='w', encoding='utf-8', newline='') as archivo_salida:
        escritor = csv.writer(archivo_salida)
        escritor.writerows(datos_curados)

# Funcion que agrega una columna de amigos al dataset curado asegurando reciprocidad
def amigo_aleatorio(datos_curados):
    # Salta la linea del header y crea un diccionario para almacenar las variables a usar
    # Guarda todos los owner_id para la seleccion de amigos
    id_a_username = {fila[0]: fila[1] for fila in datos_curados[1:]} 
    # se extraen los ids del diccionario y se convierten en lista
    todos_los_ids = list(id_a_username.keys())
   
     # Diccionario de sets para manejar las amistades de forma bidireccional (grafo no dirigido)
    
    # Aqui es donde se almacena la lista de filas final
    lista_seguidores = [datos_curados[0]]
    
    # 1. Primero se crea un diccionario completamente vacio
    amigos_por_id = {}
    # 2. Luego iteramos elemento por elemento sobre la lista de IDs
    for i in todos_los_ids:
    # 3. A cada ID le asignamos un set nuevo e independiente
        amigos_por_id[i] = set()

    for fila in datos_curados[1:]:
        owner_id = fila[0]
        # Determinamos cuantas amistades queremos que inicie este usuario
        cantidad = random.randint(1,10)

        # el loop se encarga de asegurar que se agregue la cantidad aleatoria adecuada
        while len(amigos_por_id[owner_id]) < cantidad:
            # seleciona una id aleatoria de la lista de ids
            id_aleatorio = random.choice(todos_los_ids)
            
            # Omite si el usuario se elige a sí mismo o si el amigo ya está registrado
            if id_aleatorio == owner_id or id_aleatorio in amigos_por_id[owner_id]:
                continue
            
            # Se agrega de manera reciproca en ambos sentidos
            amigos_por_id[owner_id].add(id_aleatorio)
            amigos_por_id[id_aleatorio].add(owner_id)

    # Ahora procesamos cada fila e inyectamos su respectiva lista de usernames
    for fila in datos_curados[1:]:
        owner_id = fila[0]
        followers = []
        
        # Transformamos las IDs de amigos almacenadas en el set, de vuelta a usernames
        for amigo_id in amigos_por_id[owner_id]:
            username = id_a_username[amigo_id]
            followers.append(username)
            
        # Finalmente agrega la fila entera más la lista de followers (ahora reciproca)
        nueva_fila = fila + [str(followers)]
        lista_seguidores.append(nueva_fila)    
        
    return lista_seguidores

curarDatos('instagram_data.csv')