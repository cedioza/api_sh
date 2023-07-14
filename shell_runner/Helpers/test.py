import os
import logging
import csv
import pandas as pd
import mysql.connector

# Configurar el registro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def procesar_datos():
    try:
        # Obtener el valor de la variable de entorno
        variable_entorno = os.getenv('test')

        # Crear la carpeta con el nombre de la variable de entorno si no existe
        if not os.path.exists(variable_entorno):
            os.mkdir(variable_entorno)
            # Registrar mensaje de éxito
            logging.info(f'Carpeta "{variable_entorno}" creada exitosamente')

        # Acceder a la carpeta creada
        os.chdir(variable_entorno)

        # Definir los datos
        datos = [
            {'id': 1, 'nombre': 'John Doe', 'edad': 25, 'correo': 'johndoe@example.com'},
            {'id': 2, 'nombre': 'Jane Smith', 'edad': 30, 'correo': 'janesmith@example.com'},
            {'id': 3, 'nombre': 'Mark Johnson', 'edad': 35, 'correo': 'markjohnson@example.com'}
        ]

        # Definir el nombre del archivo CSV
        nombre_archivo = 'datos.csv'

        # Escribir los datos en el archivo CSV si el archivo no existe
        if not os.path.exists(nombre_archivo):
            with open(nombre_archivo, 'w', newline='') as archivo:
                campos = ['id', 'nombre', 'edad', 'correo']
                escritor = csv.DictWriter(archivo, fieldnames=campos)

                # Escribir la línea de encabezado
                escritor.writeheader()

                # Escribir los datos
                for dato in datos:
                    escritor.writerow(dato)

            # Registrar mensaje de éxito
            logging.info(f'Archivo CSV "{nombre_archivo}" creado exitosamente')

        # Leer el archivo CSV con Pandas
        logging.info(f'Leyendo archivo CSV "{nombre_archivo}"...')
        data = pd.read_csv(nombre_archivo)

        # Imprimir los primeros registros del archivo CSV
        logging.info('Registros del archivo CSV:')
        print(data.head())

        # Conectar a la base de datos MySQL
        logging.info('Conectando a la base de datos...')
        cnx = mysql.connector.connect(user=os.getenv('user'), password=os.getenv('password'), host=os.getenv('host'), database=os.getenv('database'))

        # Crear un cursor para ejecutar consultas
        cursor = cnx.cursor()

        # Ejemplo de consulta y recuperación de datos
        logging.info('Ejecutando consulta en la base de datos...')
        cursor.execute('SELECT * FROM tabla')
        resultados = cursor.fetchall()

        # Imprimir los resultados de la consulta
        logging.info('Resultados de la consulta:')
        for row in resultados:
            print(row)
            logging.info(row)

        # Cerrar la conexión a la base de datos
        logging.info('Cerrando conexión a la base de datos...')
        cnx.close()

        return True

    except Exception as e:
        error_message = 'Ocurrió un error: {}'.format(str(e))
        logging.exception(error_message)
        return False
