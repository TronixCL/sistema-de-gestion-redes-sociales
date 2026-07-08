# Sistema de Gestión de Red Social - Índice Invertido, Grafos y Tablas Hash (Entregas I, II y III)

Este proyecto implementa el backend de análisis y búsqueda para una red social (basado en un dataset de Instagram). A través de las tres entregas, el sistema evoluciona desde la indexación básica de texto hasta el modelamiento de relaciones complejas en grafos y la optimización extrema de búsquedas mediante tablas hash propias.

## Arquitectura del Proyecto

El proyecto está modularizado en los siguientes scripts principales:

* **`main.py`**: Interfaz de usuario (CLI) y orquestación del procesamiento de datos.
* **`estructuras.py`**: Implementación desde cero de nodos y listas enlazadas (usadas como base para las demás estructuras).
* **`curado_dataset_paraGrafos.py`**: Preprocesador de datos que limpia el CSV original y genera relaciones de amistad simétricas controladas.
* **`grafo_parte2.py`**: Implementación del modelo de Grafo No Dirigido mediante listas de adyacencia.
* **`algoritmo_bfs.py`**: Motor de búsqueda en anchura con control estricto de niveles y exclusión de ciclos.
* **`tabla_hash.py`** *(Nuevo - Entrega III)*: Estructura de dispersión con función `djb2` y encadenamiento separado.
* **Archivos de apoyo**: `stopwords.txt` (filtro de palabras) y `dataset_curadoParaGrafos.csv`.

---

## Instrucciones de Ejecución

1.  Asegúrese de tener Python 3.x instalado.
2.  Coloque todos los archivos `.py`, el dataset `.csv` y `stopwords.txt` en el mismo directorio.
3.  *(Opcional)* Si desea generar un nuevo dataset aleatorio, ejecute: `python curado_dataset_paraGrafos.py`
4.  Para iniciar el sistema y el menú interactivo, ejecute: 
    ```bash
    python indice_invertido.py
    ```

---

## Especificaciones Técnicas por Entrega

### Entrega I: Índice Invertido y Listas Enlazadas
Se procesa el contenido de las publicaciones (captions) descartando *stopwords*. Cada término se indexa en una estructura que mapea la palabra hacia una `ListaEnlazada` propia que contiene los IDs de los posts donde aparece. Esto permite consultas rápidas por palabra clave.

### Entrega II: Grafo No Dirigido y BFS por Niveles
Se modelan las conexiones entre usuarios utilizando un **Grafo No Dirigido**.
* **Estructura:** Lista de adyacencia construida exclusivamente sobre la clase `ListaEnlazada` de la Entrega I.
* **Algoritmo BFS:** Se implementa un recorrido en anchura (Breadth-First Search) personalizado.
* **Control de Niveles y Duplicados:** El algoritmo utiliza un conjunto global (`todos_agregados`) evaluado en $O(1)$ que previene ciclos infinitos y garantiza que un usuario (o la raíz misma) no aparezca duplicado ni sea clasificado en un grado incorrecto.
* **Complejidad BFS:** El algoritmo está acotado a $O(V_{visitados} + E_{visitadas})$ hasta el nivel 3, siendo mucho más eficiente que recorrer el grafo completo.

### Entrega III: Tabla Hash y Función DJB2
Para contabilizar la frecuencia del vocabulario de la red social en tiempo $O(1)$ (promedio), se reemplaza el uso de diccionarios de Python por una estructura propia.

* **Función de Dispersión:** Se implementa el algoritmo **`djb2`** (Daniel J. Bernstein). Para asegurar el rendimiento en Python, el valor se trunca a 32 bits en cada iteración mediante una máscara a nivel de bits (`hash_val &= 0xFFFFFFFF`).
* **Resolución de Colisiones:** Se utiliza **Encadenamiento Separado**. El arreglo base almacena referencias a la `ListaEnlazada` de la Entrega I. Los pares `(término, frecuencia)` que colisionan en un índice se anexan a esta lista.
* **Dimensionamiento y Factor de Carga ($\alpha$):** Para mantener un factor de carga eficiente ($\alpha \le 0.67$), el arreglo se dimensiona con un número primo $M \ge 1.5 \times N$.
    * **N (Tamaño del vocabulario detectado):** *[NOTA AL ALUMNO: Reemplaza esto con la cantidad de palabras de tu índice, ej. 4150]*
    * **M (Tamaño primo de la Tabla Hash):** *[NOTA AL ALUMNO: Reemplaza con el primo seleccionado de la tabla de la rúbrica, ej. 10007]*
    * **$\alpha$ (Factor de carga actual):** *[NOTA AL ALUMNO: Calcula N / M, ej. 0.41]*
* **Funcionalidad Top-N:** Se incluye un método de ordenamiento que permite extraer los $N$ términos más repetidos en la red social.

---
