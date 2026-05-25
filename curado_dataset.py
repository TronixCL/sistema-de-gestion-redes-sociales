import os
import csv
import random

# Funcion que filtra y organiza los datos del dataset original
def curarDatos(nombreEntrada: str):
    directorio_actual = os.path.dirname(os.path.abspath(__file__)) # obtiene el directorio del preoyecto
    ruta_entrada = os.path.join(directorio_actual, nombreEntrada) # Ruta del archivo de entrada
    ruta_salida = os.path.join(directorio_actual, 'dataset_curado.csv') # Ruta del archivo de salida

    # Lista para almacenar los datos curados
    datos_curados = []
    # Conjunto para registrar los owner_id ya procesados
    owner_ids_vistos = set()

    with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
        # Lee y extrae la primera fila para el dataset curado
        lector = csv.reader(archivo)
        header = next(lector)

        # se filtran las columnas relevantes y se agrega la columna al header del dataset curado
        header_filtrado = [header[i] for i in [0, 1, 2, 4, 6]] + ['followers']    
        datos_curados.append(header_filtrado)

        # Lee cada fila del CSV como una lista de parametros
        # Si la fila está vacia, saltar a la siguiente iteración
        for parametros in lector:
            if not parametros:
                continue

            # Verifica que la fila tenga los 14 parametros del dataset
            # Donde se extrae el owner_id para validar 
            # la exclusion de owner_ids no numéricos, duplicados y espacios vacios
            # finalmente se agrega el validado al set owner_ids_vistos
            if len(parametros) >= 14:
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

# Funcion que agrega una columna de amigos al dataset curado
def amigo_aleatorio(datos_curados):
    # Salta la linea del header y crea un diccionario para almacenar las variables a usar
    # Guarda todos los owner_id para la seleccion de amigos
    id_a_username = {fila[0]: fila[1] for fila in datos_curados[1:]} 
    todos_los_ids = list(id_a_username.keys())

    # Aqui es donde se almacena la lista seguidores
    lista_seguidores = [datos_curados[0]]

    for fila in datos_curados[1:]:
        # Verificador anti-duplicaods
        owner_id = fila [0]
        cantidad = random.randint(1, 70)
        followers = []
        # Se utiliza para evitar duplicados en followers
        followers_set = set()

        # el loop se encarga de asegurar que se agregue la cantidad aleatoria adecuada
        while len(followers) < cantidad:
            # seleciona una id aleatoria de la lista de ids
            id_aleatorio = random.choice(todos_los_ids)
            if id_aleatorio == owner_id:
                continue

            username = id_a_username[id_aleatorio]
            # Omite el username si ya esta en la lista de seguidores
            if username in followers_set:
                continue
            
            # Se agrega el dicho username a las dos listas
            followers.append(username)
            followers_set.add(username) 

        # Finalmente agrega la fila entera más la lista de followers
        nueva_fila = fila + [str(followers)]
        lista_seguidores.append(nueva_fila)    
    return lista_seguidores

curarDatos('instagram_data.csv')