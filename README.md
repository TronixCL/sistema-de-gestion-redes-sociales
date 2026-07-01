# Documentación Tecnica
Este proyecto consiste en implementar la infraestructura base de un sistema de gestión de red social para modelar y visualizar la relación entre usuarios y sus publicaciones (posts). Construimos un Índice Invertido utilizando estructuras de datos lineales para permitir búsquedas "eficientes" sobre el contenido generado por los usuarios y sobre los contactos de cada usuario. <br> Haciendo uso de 3 codigos hechos en Python y 1 dataset como archivo.csv el proyecto funciona, en este caso usamos un dataset sacado de Kaggle.com. La forma en la que se utilizan a grandes rasgos es:
- 1.- Poner los 3 codigos y dataset dentro de una misma carpeta.
- 2.- Ejecutar "curado_dataset.py" para filtrar los datos necesarios (más adelante se explica como).
- 3.- Ejecutar "indice invertido" para procesar el Dataset e indexar sus datos en 2 indices Usuario y Post
- 4.- Al abrirse la interfaz de usuario, que al presionar 1, 2 o 3 en el teclado se puede:
    <br> a) Revisar por palabras clave, en que post aparecer y su autor.
    <br> b) Buscar un nombre de usuario y mostrar la lista de seguidores de este.
    <br> c) Finalizar las consultas.

## Codigos:
-----------
### curado_dataset.py:
#### Bibliotecas: 
- **"os":** os es utilizada para la obtención correcta de la ruta de acceso del dataset original que se filtra. <br>
- **"csv":** csv es utilizada para la correcta manipulación del archivo en caso de que haya problemas con los metodos estandar de python. <br>
- **"random":** random es utilizada para el algoritmo función que permite el agregado de seguidores a un usuario en particular.
#### Funciones:
**1.- curar_datos():** Esta función filtra y organiza el dataset original obteniendo el directorio de la carpeta donde se encuentra todo el proyecto, determina la ubicación de la carpeta donde esta el proyecto y crea 2 variables "ruta_entrada" y "ruta_salida" donde almacena la ruta del dataset original y nuevo. Luego crear una lista donde guarda todos los datos del nuevo dataset, abre el archivo en modo lectura, almacena el header y lo filtra con los parametros que necesitamos más la nueva columna que crea el codigo. Crea un set para las ids de usuario (ya que decidimos tomar un solo post por usuario debido al tamaño del dataset elegido) y comienza un loop for, este lee cada fila del csv en la lista, donde se usan las siguientes restricciones para filtrarla de manera adecuada, Si la fila esta vacia salta a la siguiente iteración, se extrae la id del usuario de la fila (conocida como owner_id), si el owner_id no es numerico se salta la fila, y si el owner_id es parte de la lista de ids ya vistas salta tambien, luego se agrega al set de las ids vistas. Así filtra que filas se va a utilizar el dataset curado, las reemplaza en el dataset original y las agrega a la lista con el metodo append(). Cuando la función termina de curar el dataset llama a la otra función del codigo para agregar seguidores para cada usuario y finalmente abre la ruta de salida y crea el nuevo archivo.csv.  

**2.- seguidor_aleatorio():** Está función comienza creando un diccionario donde almacena las ids de usuario junto a su nombre, este lo convierte en lista y crea otra donde se almacena la nueva columna. luego con un ciclo for, guarda la id del usuario de esa fila, elige aleatoriamente un numero entre 1 y 100 (que simboiliza la cantidad de amigos que tendra el usuario de esa fila), y una lista para sus segudiores. Haciendo un ciclo anidado for crea un contador que este dentro del rango de la cantidad de seguidores seleccionado y comienza: Selecciona un id aleatorio de la lista total. Revisa si el id seleccionado es igual al de la fila en la que esta, si lo es reinicia el ciclo. En caso de no serlo toma el username del diccionario de la id seleccionada, revisa si el username esta dentro de la lista de seguidores, si lo está reinicia el ciclo, sino la agrega a la lista de seguidores y aumenta el contador de seguidores. Tras finalizar el agregado, en una nueva variable junta la fila toamda con la lista de seguidores creada y la reemplaza en el dataset curado, así hasta que todos los usuarios tengan seguidores.

### estructuras.py:
#### Clases:
- Nodo: Clase generica que crea objetos del tipo para una lista enlazada. Guarda un dato y una referencia al siguiente nodo, inicializan con un parametro para el dato y apuntan a nada.
- ListaEnlazada: Clase que se usa para crear listas enlazadas. Inicializa con un header o dirección que apunta a nada y un tamaño númerico 0. 
#### Funciones:
(Todas las funciones son de la clase ListaEnlazada) <br>
**1.- insertar_inicio():** Crea un nodo nuevo y lo apunta al header de la lista. Como es el unico nodo en la lisa apunta así mismo y aumenta el tamaño de la lista en 1. Es O(1) porque no recorre nada.  

**2.- insertar_final():** insertar_final(dato) Crea un nodo nuevo y le asigna el header de la lista. Si la lista está vacía lo pone como cabeza; si no, recorre toda la cadena hasta el último nodo y lo enlaza ahí. Es O(n) por ese recorrido.  

**3.- buscar():** buscar(dato)
Recorre la lista nodo por nodo buscando el dato. Retorna True si lo encuentra, False si llega al final sin éxito.  

**4.- eliminar():** Busca y elimina el primer nodo que contenga el dato:
Si es la cabeza, mueve la cabeza al siguiente nodo.
Si no, recorre hasta encontrarlo y "salta" ese nodo reconectando los punteros.
Retorna True si eliminó algo, False si no lo encontró.  

**5.- recorrer():** recorrer()
Recorre toda la lista y va acumulando cada dato en una lista de Python, que retorna al final. Útil para visualizar el contenido completo.  

**6.- len():**__len__
Retorna directamente el atributo tamaño. Es O(1) porque el tamaño se mantiene actualizado en cada inserción y eliminación, sin necesidad de contar.

### indice_inverso.py:
#### Bibliotecas
#### Clases:
#### Funciones:
