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

    with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
        # Lee y extrae la primera fila para el dataset curado
        lector = csv.reader(archivo)
        header = next(lector)

        # se filtran las columnas relevantes y se agrega la columna al header del dataset curado
        header_filtrado = [header[i] for i in [0, 1, 2, 4, 6]] + ['followers']    
        datos_curados.append(header_filtrado)

        # Conjunto para registrar los owner_id ya procesados
        # Esto evita repeticiones que no van en la primera entrega
        owner_ids_vistos = set()
        
        # Lee cada fila del CSV como una lista de parametros
        # Si la fila está vacia, saltar a la siguiente iteración
        for parametros in lector:
            if not parametros:
                continue

            # Se extrae el owner_id para validar las cuentas 
            # se excluyen filas donde los owner_ids no son numéricos, estan duplicados o en espacios vacios
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

    # al terminar de almacenar el nuevo dataset, se llama a la funcion para agregar seguidores
    datos_curados = seguidor_aleatorio(datos_curados)

    # Se escribe el nuevo CSV con todo el dataset curado
    with open(ruta_salida, mode='w', encoding='utf-8', newline='') as archivo_salida:
        escritor = csv.writer(archivo_salida)
        escritor.writerows(datos_curados)

# Funcion que agrega una columna de seguidores al dataset curado
def seguidor_aleatorio(datos_curados):
    
    # el diccionario almacena los ids y sus nombres, actuando como una tabla
    # de busqueda para el algoritmo de agregación aleatoria 
    id_a_username = {fila[0]: fila[1] for fila in datos_curados[1:]} 
    # se extraen los ids del diccionario y se convierten en lista
    todos_los_ids = list(id_a_username.keys())
    # se almacena el dataset con el header, el cual el for salta
    dataset_curado = [datos_curados[0]]

    # ciclo que recorre cada fila omitiendo el header
    for fila in datos_curados[1:]:
        owner_id = fila[0]
        cantidad = random.randint(1, 100)
        seguidores = []

        for i in range(cantidad):
            # la lista de ids se utiliza para seleccionar seguidores aleatorios
            id_aleatorio = random.choice(todos_los_ids)
            # si la id que selecciono es la del usuario de la fila, se omite
            if id_aleatorio == owner_id:
                continue 
            # se obtiene el username de la id aleatoria seleccionada
            username = id_a_username[id_aleatorio]
            # si el username ya esta en la lista de seguidores, se omite
            if username in seguidores:
                continue
            # Se agrega el dicho username a las lista de seguidores
            seguidores.append(username)
            i += 1
            
        # Finalmente agrega la fila entera más la lista de followers
        nueva_fila = fila + [seguidores]
        dataset_curado.append(nueva_fila) 

    return dataset_curado

#funcion principal que comienza con el codigo
curarDatos('instagram_data.csv')