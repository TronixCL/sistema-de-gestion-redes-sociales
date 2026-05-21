import os

def curarDatos(nombreEntrada:str):
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(directorio_actual, nombreEntrada)
    ruta_salida = os.path.join(directorio_actual, 'dataset_curado.csv')

    with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
    
    datos_curados = []

    for linea in lineas: 
       
        if not linea.strip():
            continue
            
        parametros = linea.strip().split(',')
        
        if len(parametros) == 14 and parametros[0] :
            columnas_a_usar = [0,1, 2, 13]
        
            fila_filtrada = [parametros[i] for i in columnas_a_usar]
            fila_unida = ','.join(fila_filtrada)
            datos_curados.append(fila_unida + '\n')
        else: 
            continue
        
        
    print(datos_curados)    

    with open(ruta_salida, mode='w', encoding='utf-8') as archivo_salida:
        archivo_salida.writelines(datos_curados)

curarDatos('instagram_data.csv')
