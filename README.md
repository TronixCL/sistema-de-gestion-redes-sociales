# Documentación Tecnica
Este proyecto consiste en implementar la infraestructura base de un sistema de gestión de red social para modelar y visualizar la relación entre usuarios y sus publicaciones (posts). Construimos un Índice Invertido utilizando estructuras de datos lineales para permitir búsquedas "eficientes" sobre el contenido generado por los usuarios y sobre los contactos de cada usuario. <br> Haciendo uso de 3 codigos hechos en Python y 1 dataset como archivo.csv el proyecto funciona, en este caso usamos un dataset sacado de Kaggle.com. La forma en la que se utilizan a grandes rasgos es:
- 1.- Poner los 3 codigos y dataset dentro de una misma carpeta.
- 2.- Ejecutar "curado_dataset.py" para filtrar los datos necesarios (más adelante se explica como).
- 3.- Ejecutar "indice invertido" para procesar el Dataset e indexar sus datos en 2 indices Usuario y Post
- 4.- Al abrirse la interfaz de usuario, que al presionar 1, 2 o 3 en el teclaso se puede:
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
**curar_datos():** Esta función filtra y organiza el dataset original obteniendo el directorio de la carpeta donde se encuentra todo el proyecto, determina la ubicación de la carpeta donde esta el proyecto y crea 2 variables "ruta_entrada" y "ruta_salida" donde almacena la ruta del dataset original y nuevo. Luego crear una lista donde guarda todos los datos del nuevo dataset, abre el archivo en modo lectura, almacena el header y lo filtra con los parametros que necesitamos más la nueva columna que crea el codigo. Crea un set para las ids de usuario (ya que decidimos tomar un solo post por usuario) y comienza un loop for, este lee cada fila del csv en la lista, donde se usan las siguientes restricciones para filtrarla de manera adecuada: 
- linea 29: Si la fila esta vacia salta a la siguiente iteración.
- linea 36-41: Se extrae la owner_id de la fila, si el owner_id no es numerico se salta la fila, y si el owner_id es parte de la lista de ids ya vistas salta tambien, luego se agrega al set de las ids vistas.
- linea 45-47: Así filtra que filas se va a utilizar el dataset curado, las reemplaza en el dataset original y las agrega a la lista con el metodo append().

Cuando la función termina de curar el dataset llama a la otra función del codigo para agregar seguidores para cada usuario y finalmente abre la ruta de salida y crea el nuevo archivo.csv.  

**seguidor_aleatorio():** Está función comienza creando un diccionario donde almacena las ids de usuario junto a su nombre y 2 listas, una con todas las ids, y otra donde almacena el dataset ya curado, elheader más especificamente. Para luego con un primer ciclo for, guardar la id del usuario de esa fila, un numero entre 1 y 100, y una lista para los segudiores. Con el otro ciclo for crea un contador que este dentro del rango de la cantidad de seguidores seleccionado y comienza:
- linea 75: Selecciona un id aleatorio de la lista total.
- lineas 77-79: Revisa si el id seleccionado es el de la fila en la que esta, si lo es suma al contador y reinicia el ciclo.
- linea 81: En caso de no serlo toma el username del diccionario de la id seleccionada.
- lineas 83-88: revisa si el username esta dentro de la lista de seguidores, si lo está aumenta el contador y reinicia el ciclo, sino la agrega a la lista de seguidores y aumenta el contador.

Tras finalizar el agregar seguidores a un usuario agrega esa nueva fila al dataset curado, así hasta que todos los usuarios tengan seguidores.

### estructuras.py:
#### Clases: 
#### Funciones:


### indice_inverso.py:
#### Bibliotecas
#### Clases:
#### Funciones:
