import os
import csv 

def curarDatos(nombreEntrada:str):
    directorioActual = os.path.dirname(os.path.abspath(__file__))
    rutaEntrada = os.path.join(directorioActual, nombreEntrada)
    rutaSalida = os.path.join(directorioActual, 'dataset_curado.csv')

    datosCurados = []

    with open(rutaEntrada, mode='r', encoding='utf-8') as archivo:
        columnas = [0, 1, 2, 4, 6, 12]
        lector = csv.reader(archivo) 
        primerFila = next(lector, None)
        datosCurados.append([primerFila[i] for i in columnas])
        for parametros in lector: 
            if not parametros:
                continue
            
            if len(parametros) >= 14 and parametros[0]: 
                owner_id = parametros[0].strip() # .strip() quita espacios accidentales a los lados
                
                if not owner_id.isdigit():
                    continue # Si tiene letras o caracteres raros, saltamos la fila
                
                # Seguimos limpiando los saltos de línea 
                filaFiltrada = [parametros[i].replace('\n', ' ') for i in columnas]
                
                # Guardamos la lista entera
                datosCurados.append(filaFiltrada)
            else: 
                continue          
                
    # Usamos csv.writer para guardar el archivo
    with open(rutaSalida, mode='w', encoding='utf-8', newline='') as archivo_salida:
        escritor = csv.writer(archivo_salida)
        escritor.writerows(datosCurados)

if __name__ == '__main__':
    curarDatos('instagram_data.csv')
