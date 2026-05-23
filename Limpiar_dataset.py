import os
import csv 

def curarDatos(nombreEntrada:str):
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(directorio_actual, nombreEntrada)
    ruta_salida = os.path.join(directorio_actual, 'dataset_curado.csv')

    datos_curados = []
    ids_vistos = set() 

    with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
        columnas = [0, 1, 2, 4, 6, 12]
        lector = csv.reader(archivo) 
        primer_fila = next(lector, None)
        datos_curados.append([primer_fila[i] for i in columnas])
        for parametros in lector: 
            if not parametros:
                continue
            
            if len(parametros) >= 14 and parametros[0]: 
                owner_id = parametros[0].strip() # .strip() quita espacios accidentales a los lados
                
                if not owner_id.isdigit():
                    continue # Si tiene letras o caracteres raros, saltamos la fila
                
                # Registramos el ID válido en nuestro set
                ids_vistos.add(owner_id)
                
                # Seguimos limpiando los saltos de línea (Enters)
                fila_filtrada = [parametros[i].replace('\n', ' ') for i in columnas]
                
                # Guardamos la lista entera
                datos_curados.append(fila_filtrada)
            else: 
                continue          
                
    # Usamos csv.writer para guardar el archivo
    with open(ruta_salida, mode='w', encoding='utf-8', newline='') as archivo_salida:
        escritor = csv.writer(archivo_salida)
        escritor.writerows(datos_curados)

if __name__ == '__main__':
    curarDatos('instagram_data.csv')