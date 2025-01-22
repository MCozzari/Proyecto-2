
# Internet Analisis

## Descripcion

Este programa está diseñado para llevar a cabo un Análisis Exploratorio de Datos (EDA) utilizando los datos proporcionados por el ENAMOC sobre las conexiones de internet en el país. Además, automatiza la carga de estos datos en una base de datos MySQL, con el objetivo de facilitar su representación en un dashboard interactivo.

### Características principales:

 - Realiza un análisis exhaustivo y detallado de los datos de conexiones de internet.

 - Limpia y normaliza los datos para garantizar su calidad y consistencia.

 - Automatiza la carga de datos en una base de datos MySQL, asegurando una estructura óptima.

 - Prepara los datos para su visualización en un dashboard, permitiendo una comprensión clara y efectiva de la información.

 - Este programa es ideal para quienes buscan transformar datos crudos en visualizaciones significativas y tomar decisiones informadas basadas en datos precisos.

## Trabajo Realizado

### 1. Preparación de Datos

 - **Carga de Datos:** Se Cargaron los datos desde el respectivo archivo xlsx
 - **Limpieza de Datos:** Se verifico que para cada df tenga los datos completos y no duplicados, en caso de encontrarlos se soluciono.
 - **Uso de Graficos:** Se utilizaron diversos graficos para poder analizar la respectiva informacion, buscando Outliers, patrones y tendencias claves.

### 2. Creacion de la Base de Datos:
La creación de una base de datos en MySQL fue un paso fundamental para manejar y estructurar los datos de manera eficiente. A continuación, se detalla el proceso llevado a cabo:

 -Establecimiento de la Conexión: Se estableció una conexión segura con el servidor MySQL utilizando las credenciales apropiadas. Este paso es crucial para asegurar que todos los procesos subsecuentes se realicen de manera segura y eficiente.

 -Creación de la Base de Datos: Se creó una nueva base de datos denominada proyecto, destinada a almacenar todos los datos relacionados con las conexiones de internet proporcionados por el ENAMOC. Este paso asegura que los datos estén centralizados y organizados.

 -Definición de las Tablas: Se definieron las tablas necesarias para almacenar los datos de manera estructurada. Cada tabla se diseñó considerando las columnas pertinentes y sus tipos de datos, para asegurar que la información se almacene de manera coherente y eficiente.

 -Limpieza y Normalización de Datos: Antes de insertar los datos en la base de datos, se llevó a cabo un proceso de limpieza y normalización. Este proceso incluyó la verificación de duplicados, la corrección de nombres de provincias y la conversión de los datos a los formatos adecuados. Esto asegura que la base de datos contenga información precisa y confiable.

 -Carga de Datos: Los datos fueron cargados desde archivos de Excel (.xlsx) a la base de datos MySQL. Se utilizaron scripts automatizados para insertar los datos en las tablas correspondientes, lo que asegura eficiencia y reducción de errores.

 -Renombrado de Tablas: Se renombró la tabla penetración-poblacion a penetracion-poblacion para evitar inconvenientes al utilizarla en el dashboard.

 -Unificación de Provincias: Se revisaron las provincias para que todas estuvieran escritas de la misma manera en todas las tablas, garantizando la consistencia de los datos.
### 3. Creacion del Dashboard:
Se diseñó un dashboard interactivo con el propósito de visualizar los datos analizados de manera clara y accesible. El dashboard permite a los usuarios explorar la información de las conexiones de internet en el país de una manera dinámica y comprensible.

## Uso

1. Clona el repositorio: 
```sh 
git clone https://github.com/MCozzari/proyecto-2.git 
cd proyecto-2
```
2. Instala las dependencias usando pip:
```sh
pip install -r requirements.txt
```
3. Modifica los datos de connection, con respecto a tu base de datos

```sh
    connection = mysql.connector.connect( 
        host='localhost', 
        user='TuUsuario', 
        password='TuContraseña'
    )
```

4. Ejecuta el script principal.

```sh 
python main.py
```