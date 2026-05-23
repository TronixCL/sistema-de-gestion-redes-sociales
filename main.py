import csv
import os
import time
from Estructuras import Usuario, IndicePalabras, IndiceUsuariosSocial

def cargar_sistema(nombre_archivo):
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_dataset = os.path.join(directorio_actual, nombre_archivo)
    
    indice_filtrado_posts = IndicePalabras() 
    indice_red_social = IndiceUsuariosSocial()
    
    # Diccionario temporal para armar los objetos rápido sin penalizar el tiempo de carga
    directorio_usuarios_memoria = {} 
    
    stop_words = {"el", "la", "los", "las", "un", "una", "de", "del", "a", "ante", 
                  "con", "en", "para", "por", "y", "o", "su", "sus", "is", "the", 
                  "and", "to", "in", "of", "for", "with", "my", "on", "a", ""}

    print("[*] Leyendo el dataset curado y estructurando la memoria RAM...")
    inicio_tiempo = time.time()
    posts_procesados = 0

    with open(ruta_dataset, mode='r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        
        for fila in lector:
            if len(fila) < 5: 
                continue
            
            # CONTROL PARA EL VIDEO: Límite para una carga rápida de 2 segundos
            if posts_procesados >= 1000: 
                break
            
            post_id = fila[2]               
            descripcion = fila[3].lower()   
            username = fila[1].strip()      
            contacto = fila[4].strip()      
            
            # ------------------------------------------------------------------
            # A. RELACIÓN ORIENTADA A OBJETOS (1 a N)
            # ------------------------------------------------------------------
            if username not in directorio_usuarios_memoria:
                directorio_usuarios_memoria[username] = Usuario(username)
            
            usuario_actual = directorio_usuarios_memoria[username]
            post_obj = usuario_actual.agregar_post(post_id, descripcion)

            # ------------------------------------------------------------------
            # B. ALIMENTACIÓN DEL ÍNDICE INVERTIDO SOCIAL
            # ------------------------------------------------------------------
            if username:
                indice_red_social.registrar_contacto(username, contacto)

            # ------------------------------------------------------------------
            # C. ALIMENTACIÓN DEL ÍNDICE INVERTIDO DE PALABRAS
            # ------------------------------------------------------------------
            palabras = descripcion.split()
            for palabra in palabras:
                palabra_limpia = palabra.strip('.,!?"\'()-[]{}#@')
                
                # Filtro agresivo: elimina espacios, stop words y EMOJIS/símbolos
                if not palabra_limpia or palabra_limpia in stop_words or not palabra_limpia.isalpha():
                    continue
                
                indice_filtrado_posts.registrar_palabra(palabra_limpia, post_obj)
            
            posts_procesados += 1

    fin_tiempo = time.time()
    print(f"\n[+] Estructuras construidas con éxito en {fin_tiempo - inicio_tiempo:.2f} segundos.")
    print(f"[+] Total de publicaciones indexadas: {posts_procesados}")
    print(f"[+] Entidades 'Usuario' activas en memoria POO: {len(directorio_usuarios_memoria)}")
    
    return indice_filtrado_posts, indice_red_social

# ==============================================================================
# MENÚ INTERACTIVO DE EVALUACIÓN
# ==============================================================================
if __name__ == "__main__":
    print("="*50)
    print("SISTEMA DE GESTIÓN DE RED SOCIAL - INFRAESTRUCTURA BASE")
    print("="*50)
    
    indice_palabras, indice_social = cargar_sistema('dataset_curado.csv')
    
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
                indice_palabras.buscar_palabra(termino)
                
        elif opcion == '2':
            usuario = input("Ingresa el username del perfil (sin @): ").strip()
            if usuario:
                indice_social.buscar_amigos(usuario)
        else:
            print("[-] Opción no válida. Intente nuevamente.")