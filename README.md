# Documentación Tecnica
Se hace uso de 3 codigos hechos en Python y 1 dataset como archivo.csv para que el proyecto funcione (en este caso usamos un dataset sacado de Kaggle.com), estos codigos son "curado_dataset.py", "estructuras.py", "indice_invertido.py". 
La forma en la que se utilizan a grandes rasgos es:
- 1.- Poner los 3 codigos y dataset dentro de una misma carpeta.
- 2.- Ejecutar "curado_dataset.py" para filtrar los datos necesarios (más adelante se explica como).
- 3.- Ejecutar "indice invertido" para procesar el Dataset e indexar sus datos en 2 indices Usuario y Post
- 4.- Al abrirse la interfaz de usuario, que al presionar 1, 2 o 3 en el teclaso se puede:
    <br> a) Revisar por palabras clave, en que post aparecer y su autor.<br>
    b) Buscar un nombre de usuario y mostrar la lista de seguidores de este.<br>
    c) Finalizar las consultas.

Ahora se detallará que hace cada funcion del codigo:
-----------------------------------------------------------
## curado_dataset.py:
### Bibliotecas: 
**"os": os es utilizada para la obtención correcta de la ruta de acceso del dataset original que se filtra. <br>
"csv": csv es utilizada para la correcta manipulación del archivo en caso de que haya problemas con los metodos estandar de python. <br>
"random": random es utilizada para el algoritmo función que permite el agregado de seguidores a un usuario en particular.**
### Funciones:
**curar_datos(nombreEntrada: str):** Esta función filtra y organiza el dataset original obteniendo el directorio
de la carpeta donde se encuentra todo el proyecto, toma la ruta del archivo del dataset original y tambien el nuevo dataset que almacena como dos variables por el nombre de "ruta_entrada" y "ruta_salida" para después crear una variable lista donde almacena todos los datos del nuevo dataset, también es creado un set para guardar cada owner_id visto (para prevenir que se repitan los posts de una misma persona, esto por decisión del equipo y reducir tiempos de carga). <br>
Se toma abre el dataset en modo lectura como la variable "archivo", con el metodo csv.reader(archivo), y se guarda el encabezado en otra variable llamado "header" se toma esta nueva variable y se filtra con las columnas a usar más la columna que se crea del algoritmo de seguidores aleatorios y se almacena en el nuevo dataset con un .append(). <br>
Se crea un loop for que lee cada fila del csv como una lista de parametros, donde se crean las siguientes restricciones para filtrarla de manera adecuada: <br>
- linea 28: si la fila esta vacia salta a la siguiente iteración
- linea 35-47: se verifica que la fila tenga los 14 parametros del dataset, se extrae la owner_id de la fila y con eso se crean 2 condicionales, si el owner_id no es numerico se salta la fila, y si el owner_id es parte de la lista de ids ya vistas se salta tambien, luego en caso de no estarlo se agrega a la lista y luego filtra que filas se van a utilizar en el dataset curado para luego reemplazarlas en el nuevo dataset, hacer un salto de linea y agregarlos con un .append()
------------------------------------------------------------
## estructuras.py:
### Clases: 
### Funciones:
------------------------------------------------------------
## indice_inverso.py:
### Bibliotecas
### Clases:
### Funciones:
