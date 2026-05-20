import os

directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_entrada = os.path.join(directorio_actual, 'instagram_data.csv')
ruta_salida = os.path.join(directorio_actual, 'dataset_curado.csv')

columnas_a_usar = [0, 1, 2, 13]

with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
    lineas = archivo.readlines()

datos_curados = []

for linea in lineas:
    print(linea.strip())
    
    if not linea.strip():
        continue
        
    parametros = linea.strip().split(',')
    
    if len(parametros) < 14:
        parametros.extend([''] * (14 - len(parametros)))
    elif len(parametros) > 14:
        parametros = parametros[:14]
        
    fila_filtrada = [parametros[i] for i in columnas_a_usar]
    datos_curados.append(','.join(fila_filtrada) + '\n')

    

with open(ruta_salida, mode='w', encoding='utf-8') as archivo_salida:
    archivo_salida.writelines(datos_curados)