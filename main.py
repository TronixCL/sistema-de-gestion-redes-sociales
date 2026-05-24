import csv
import os
import time
from Estructuras import Usuario, IndicePalabras, IndiceUsuariosSocial

def cargarSistema(nombreArchivo):
    directorioActual = os.path.dirname(os.path.abspath(__file__))
    rutaDataset = os.path.join(directorioActual, nombreArchivo)
    
    indiceFiltradoPost = IndicePalabras() 
    indiceRedSocial = IndiceUsuariosSocial()
    
    # Diccionario temporal para armar los objetos 
    directorioMemoria = {} 
    
    stopWords = {"el", "la", "los", "las", "un", "una", "de", "del", "a", "ante", 
                  "con", "en", "para", "por", "y", "o", "su", "sus", "is", "the", 
                  "and", "to", "in", "of", "for", "with", "my", "on", "a", ""}

    print("[*] Leyendo el dataset curado y estructurando la memoria RAM...")
    inicioTiempo = time.time()
    postProcesado = 0

    with open(rutaDataset, mode='r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        
        for fila in lector:
            if len(fila) < 5: 
                continue
            
            # CONTROL PARA EL VIDEO
            if postProcesado >= 3000: 
                break
            
            postId = fila[2]               
            descripcion = fila[3].lower()   
            username = fila[1].strip()      
            contacto = fila[4].strip()      
            

            # RELACIÓN ORIENTADA A OBJETOS 
            if username not in directorioMemoria:
                directorioMemoria[username] = Usuario(username)
            
            usuarioActual = directorioMemoria[username]
            postObj = usuarioActual.agregarPost(postId, descripcion)
            
            # ALIMENTACIÓN DEL ÍNDICE INVERTIDO SOCIAL
            if username:
                indiceRedSocial.registrarContacto(username, contacto)

            # ALIMENTACIÓN DEL ÍNDICE INVERTIDO DE PALABRAS

            palabras = descripcion.split()
            for palabra in palabras:
                palabraLimpia = palabra.strip('.,!?"\'()-[]{}#@')
                
                # Filtro: elimina stop words
                if not palabraLimpia or palabraLimpia in stopWords or not palabraLimpia.isalpha():
                    continue
                
                indiceFiltradoPost.registrarPalabra(palabraLimpia, postObj)
            
            postProcesado += 1

    fin_tiempo = time.time()
    print(f"\n[+] Estructuras construidas con éxito en {fin_tiempo - inicioTiempo:.2f} segundos.")
    print(f"[+] Total de publicaciones indexadas: {postProcesado}")
    print(f"[+] Entidades 'Usuario' activas en memoria POO: {len(directorioMemoria)}")
    
    return indiceFiltradoPost, indiceRedSocial


if __name__ == "__main__":
    os.system('cls')
    print("="*50)
    print("SISTEMA DE GESTIÓN DE RED SOCIAL - INFRAESTRUCTURA BASE")
    print("="*50)
    
    indicePalabras, indiceSocilal = cargarSistema('dataset_curado.csv')
    
    while True:
        print("\n" + "-"*50)
        print("MÓDULO DE CONSULTAS Y BÚSQUEDA EFICIENTE")
        print("1. Buscar publicaciones por palabra clave (Muestra Frecuencias)")
        print("2. Buscar red de contactos de un usuario (Índice Social)")
        print("3. Salir del Sistema")
        opcion = input("Seleccione una opción (1/2/3): ").strip()
        
        if opcion == '3':
            print("Cerrando el sistema. ¡Memoria dinámica liberada correctamente!")
            break
            
        elif opcion == '1':
            termino = input("Ingresa la palabra a buscar: ").lower().strip()
            if termino:
                indicePalabras.buscarPalabra(termino)
                
        elif opcion == '2':
            usuario = input("Ingresa el username del perfil (sin @): ").strip()
            if usuario:
                indiceSocilal.buscarAmigos(usuario)
        else:
            print("[-] Opción no válida. Intente nuevamente.")