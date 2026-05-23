import csv
import os
import time
from Estructuras import ListaIndice

def cargar_sistema(nombre_archivo):
    """
    Lee el CSV curado y construye AMBOS índices exigidos por el proyecto.
    """
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_dataset = os.path.join(directorio_actual, nombre_archivo)
    
    # ==========================================
    # NUEVO: Instanciamos los DOS índices requeridos
    # ==========================================
    indice_posts = ListaIndice()     # Índice 1: Palabras -> IDs de posts
    indice_usuarios = ListaIndice()  # Índice 2: Usuarios -> IDs de amigos/contactos
    
    stop_words = {"el", "la", "los", "las", "un", "una", "de", "del", "a", "ante", 
                  "con", "en", "para", "por", "y", "o", "su", "sus", "is", "the", 
                  "and", "to", "in", "of", "for", "with", "my", "on", "a", ""}

    print("[*] Leyendo el dataset y construyendo la memoria dinámica...")
    inicio_tiempo = time.time()
    posts_procesados = 0

    with open(ruta_dataset, mode='r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        
        for fila in lector
            if len(fila) < 5: 
                continue
            
            # Freno para el video
            if posts_procesados >= 1000:
                break
            
            # --- DATOS DEL POST ---
            post_id = fila[2]               # Shortcode
            descripcion = fila[3].lower()   # ¡Ahora sí! El texto está en la fila 3 de tu nuevo CSV
            
            # --- DATOS DEL USUARIO ---
            username = fila[1].strip()      # Owner username
            contacto = fila[4].strip()      # Following (en la fila 4 de tu nuevo CSV)
            
            # 1. ÍNDICE DE USUARIOS
            if username and contacto:
                indice_usuarios.registrar_palabra(username, contacto)

            # 2. ÍNDICE DE POSTS
            palabras = descripcion.split()
            for palabra in palabras:
                palabra_limpia = palabra.strip('.,!?"\'()-[]{}#@')
                
                if not palabra_limpia or palabra_limpia in stop_words:
                    continue
                    
                indice_posts.registrar_palabra(palabra_limpia, post_id)
            
            posts_procesados += 1

    fin_tiempo = time.time()
    print(f"[+] Índices construidos exitosamente en {fin_tiempo - inicio_tiempo:.2f} segundos.")
    print(f"[+] Total de registros procesados: {posts_procesados}")
    
    # Retornamos ambos índices
    return indice_posts, indice_usuarios

# ==========================================
# MENÚ INTERACTIVO COMPLETO
# ==========================================
if __name__ == "__main__":
    print("="*50)
    print("SISTEMA DE GESTIÓN DE RED SOCIAL")
    print("="*50)
    
    # Cargamos AMBOS índices a la memoria RAM
    mi_indice_posts, mi_indice_usuarios = cargar_sistema('dataset_curado.csv')
    
    while True:
        print("\n" + "-"*50)
        print("¿Qué deseas buscar?")
        print("1. Buscar posts por palabra clave")
        print("2. Buscar contactos de un usuario")
        print("3. Salir")
        opcion = input("Elige una opción (1/2/3): ").strip()
        
        if opcion == '3':
            print("Cerrando el sistema. ¡Memoria dinámica liberada!")
            break
            
        elif opcion == '1':
            termino = input("Ingresa la palabra a buscar: ").lower().strip()
            if termino:
                mi_indice_posts.buscar_palabra(termino)
                
        elif opcion == '2':
            usuario = input("Ingresa el @username del perfil: ").strip() # Ej: christinehmcconnell
            if usuario:
                mi_indice_usuarios.buscar_palabra(usuario)
                
        else:
            print("Opción no válida.")
