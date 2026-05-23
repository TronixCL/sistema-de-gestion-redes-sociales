import os
import csv 

def curarDatos(nombreEntrada:str):
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(directorio_actual, nombreEntrada)
    ruta_salida = os.path.join(directorio_actual, 'dataset_curado.csv')

    datos_curados = []

    with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo) 
        
        for parametros in lector: 
            if not parametros:
                continue
            
            if len(parametros) >= 14 and parametros[0]: 
                columnas = [0, 1, 2, 4, 13]
                
                # Seguimos limpiando los saltos de línea (Enters)
                fila_filtrada = [parametros[i].replace('\n', ' ') for i in columnas]
                
                # ¡CAMBIO 1! Guardamos la lista entera, sin hacerle '.join()'
                datos_curados.append(fila_filtrada)
            else: 
                continue          
                
    # ¡CAMBIO 2! Usamos csv.writer para guardar el archivo.
    # Nota: Agregamos newline='' para evitar que se creen filas vacías en blanco
    with open(ruta_salida, mode='w', encoding='utf-8', newline='') as archivo_salida:
        escritor = csv.writer(archivo_salida)
        escritor.writerows(datos_curados)

if __name__ == '__main__':
    curarDatos('instagram_data.csv')

