import pandas as pd
import mysql.connector
from mysql.connector import Error

dict_df = pd.read_excel('./datos/datos_procesados.xlsx', sheet_name=None)
# Limpiamos los nombres de las hojas (eliminar espacios al principio y al final) 
dict_df = {nombre.strip(): df for nombre, df in dict_df.items()}


def obtener_columnas_provincia(connection, nombre_tabla):
    """
    Obtiene las columnas que contienen la palabra 'provincia' en su nombre de una tabla específica.

    Parámetros:
    connection (MySQLConnection): La conexión activa a la base de datos MySQL.
    nombre_tabla (str): El nombre de la tabla de la cual obtener las columnas.

    Retorna:
    list: Una lista de nombres de columnas que contienen la palabra 'provincia'.
    """
    cursor = connection.cursor()
    try:
        # Obtener las columnas de la tabla
        cursor.execute(f"SHOW COLUMNS FROM `{nombre_tabla}`")
        columnas = cursor.fetchall()
        return [columna[0] for columna in columnas if "provincia" in columna[0].lower()]
    except Error as e:
        print(f"Error al obtener columnas de la tabla `{nombre_tabla}`: {e}")
    finally:
        cursor.close()

def unificar_provincias(connection, nombre_tabla, columna_provincia):
    """
    Unifica los nombres de las provincias en una columna específica de una tabla.

    Parámetros:
    connection (MySQLConnection): La conexión activa a la base de datos MySQL.
    nombre_tabla (str): El nombre de la tabla a modificar.
    columna_provincia (str): El nombre de la columna que contiene los nombres de las provincias.

    Retorna:
    None
    """
    cursor = connection.cursor()
    try:
        # Normalizamos los nombres de las provincias
        cursor.execute(f"UPDATE `{nombre_tabla}` SET `{columna_provincia}` = 'Entre Ríos' WHERE `{columna_provincia}` = 'Entre Rios'")
        cursor.execute(f"UPDATE `{nombre_tabla}` SET `{columna_provincia}` = 'Caba' WHERE `{columna_provincia}` = 'Capital Federal'")
        cursor.execute(f"UPDATE `{nombre_tabla}` SET `{columna_provincia}` = 'Neuquén' WHERE `{columna_provincia}` = 'Neuquen'")
        cursor.execute(f"UPDATE `{nombre_tabla}` SET `{columna_provincia}` = 'Río Negro' WHERE `{columna_provincia}` = 'Rio Negro'")
        cursor.execute(f"UPDATE `{nombre_tabla}` SET `{columna_provincia}` = 'Tucumán' WHERE `{columna_provincia}` = 'Tucuman'")
        connection.commit()
        print(f"Provincias unificadas en la tabla `{nombre_tabla}` en la columna `{columna_provincia}`.")
    except Error as e:
        print(f"Error al unificar provincias en la tabla `{nombre_tabla}` en la columna `{columna_provincia}`: {e}")
    finally:
        cursor.close()

def unificar_provincias_en_bd(connection):
    """
    Unifica los nombres de las provincias en todas las tablas de la base de datos.

    Parámetros:
    connection (MySQLConnection): La conexión activa a la base de datos MySQL.

    Retorna:
    None
    """
    cursor = connection.cursor()
    try:
        # Obtenemos todas las tablas de la base de datos
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()
        for (tabla,) in tablas:
            columnas_provincia = obtener_columnas_provincia(connection, tabla)
            for columna_provincia in columnas_provincia:
                unificar_provincias(connection, tabla, columna_provincia)
    except Error as e:
        print(f"Error al obtener tablas: {e}")
    finally:
        cursor.close()

def map_dtype(dtype):
    """
    Mapea los tipos de datos de pandas a los tipos de datos de MySQL.

    Parámetros:
    dtype (dtype): El tipo de datos de la columna en pandas.

    Retorna:
    str: El tipo de datos correspondiente en MySQL.
    """
    if pd.api.types.is_integer_dtype(dtype):
        return 'INT'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'DATETIME'
    else:
        return 'VARCHAR(250)'

# Conexión a MySQL (ajusta los parámetros según tu configuración)
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root1234',
    )

    if connection.is_connected():
        cursor = connection.cursor()
        # Creamos la base de datos si no existe y seleccionarla
        cursor.execute("CREATE DATABASE IF NOT EXISTS `proyecto`")
        cursor.execute("USE `proyecto`")

        # Procesar cada DataFrame en el diccionario dict_df
        for nombre_hoja, df in dict_df.items():
            # Limpiamos los nombres de las columnas
            df.columns = [col.replace(' ', '_').replace('(', '').replace(')', '') for col in df.columns]

            # Se crea la tabla en la base de datos con los tipos de datos correctos
            create_table_query = f'''
                CREATE TABLE IF NOT EXISTS `{nombre_hoja}` (
                    {', '.join([f'`{col}` {map_dtype(df[col].dtype)}' for col in df.columns])}
                );
            '''
            cursor.execute(create_table_query)

            # Se insertan los datos
            for i, row in df.iterrows():
                placeholders = ', '.join(['%s'] * len(row))
                insert_query = f"INSERT INTO `{nombre_hoja}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({placeholders})"
                cursor.execute(insert_query, tuple(row))
        
        # Renombramos la tabla penetracion-poblacion, debido a un inconveniente al utilizarla en el dashboard
        cursor.execute(f"ALTER TABLE `penetración-poblacion` RENAME TO `penetracion-poblacion`")
        # Revisamos las provincias para que todas esten escritas de la misma manera
        unificar_provincias_en_bd(connection)
        connection.commit()

except Error as e:
    print(f"Error al conectar a MySQL: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión a MySQL cerrada.")

print("Tablas creadas e importadas exitosamente a MySQL.")
