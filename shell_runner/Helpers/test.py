import os, shutil
import csv
import pandas as pd
import mysql.connector
import re
import numpy as np





def procesar_datos(logger):
    try:
        ruta_actual = os.getcwd()
        logger.info(f'Ruta actual: {ruta_actual}')

        ruta_deseada = os.path.join(ruta_actual, "var", "www", "html", "api_sh")

        # Cambiar al directorio deseado
        os.chdir(ruta_deseada)
        logger.info(f'Ruta deseada: {ruta_deseada}')

        # Obtener el valor de la variable de entorno
        variable_entorno = os.getenv('test')

        # Crear la carpeta con el nombre de la variable de entorno si no existe
        if not os.path.exists(variable_entorno):
            os.mkdir(variable_entorno)
            # Registrar mensaje de éxito
            logger.info(f'Carpeta "{variable_entorno}" creada exitosamente')

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
            logger.info(f'Archivo CSV "{nombre_archivo}" creado exitosamente')

        # Leer el archivo CSV con Pandas
        logger.info(f'Leyendo archivo CSV "{nombre_archivo}"...')
        data = pd.read_csv(nombre_archivo)

        # Imprimir los primeros registros del archivo CSV
        logger.info('Registros del archivo CSV:')
        logger.info(data.head())

        # Conectar a la base de datos MySQL
        logger.info('Conectando a la base de datos...')
        cnx = mysql.connector.connect(user=os.getenv('user'), password=os.getenv('password'), host=os.getenv('host'), database=os.getenv('database'))

        # Crear un cursor para ejecutar consultas
        cursor = cnx.cursor()

        # Ejemplo de consulta y recuperación de datos
        logger.info('Ejecutando consulta en la base de datos...')
        cursor.execute('SELECT * FROM `Election`')
        resultados = cursor.fetchall()

        logger.info(f"\n resultado completo \n {resultados}")


        # Imprimir los resultados de la consulta
        logger.info('Resultados de la consulta:')
        for row in resultados:
            print(row)
            logger.info(f"\n linea 1 \n {row}")

        # Cerrar la conexión a la base de datos
        logger.info('Cerrando conexión a la base de datos...')
        cnx.close()

        return True

    except Exception as e:
        error_message = 'Ocurrió un error: {}'.format(str(e))
        logger.exception(error_message)
        return False
    
def cargar_informacion(logger):
    variable_entorno = os.getenv('test')
     # Crear la carpeta con el nombre de la variable de entorno si no existe
    if not os.path.exists(variable_entorno):
         os.mkdir(variable_entorno)
         # Registrar mensaje de éxito
         logger.info(f'Carpeta "{variable_entorno}" creada exitosamente')
     # Acceder a la carpeta creada
    os.chdir(variable_entorno)


    logger.info(files_path)
    for path in os.listdir(files_path):
        if os.path.isfile(os.path.join(files_path, path)):
            logger.info('Precessing file: ' + path)
            # extract the file name and extension
            split_tup = os.path.splitext(path)
            file_name, _ = split_tup
            
            names = []
            data = COLUMNS_DB[:34]
            if file_name.lower().startswith('cobro'):
                date_str = file_name[21:29]
                if len(file_name) > 29:
                    db_table = 'cobro_46'
                    data.extend(['fecha_dia_46', 'mes_a_trabajar', 'nombre_db'])
                    colspecs = COLSPECS_COBRO_46
                    for i in range(1, 36, 1):
                        names.append(str(i))
                else:
                    db_table = 'cobro'
                    colspecs = COLSPECS_COBRO
                    data.extend(['fecha_entrega_colmena', 'mes_a_trabajar', 'nombre_db'])
                    for i in range(1, 39, 1):
                        names.append(str(i))
            elif file_name.lower().startswith('preventiva'):
                date_str = file_name[27:35]
                if len(file_name) > 35:
                    db_table = 'preventiva'
                    colspecs = COLSPECS_PREV
                    data.extend(['fecha_entrega_colmena', 'mes_a_trabajar', 'nombre_db'])
                    for i in range(1, 36, 1):
                        names.append(str(i))
                else:
                    db_table = 'preventiva_24'
                    colspecs = COLSPECS_PREV_24
                    data.extend(['fecha_dia_24', 'mes_a_trabajar', 'nombre_db'])
                    for i in range(1, 36, 1):
                        names.append(str(i))
            else:
                continue
            
            logger.info('db_table: ' + db_table)
                
            read_file = pd.read_fwf(
                files_path + path,
                # skiprows=36,
                # skipfooter=5,
                colspecs=colspecs,
                encoding='ISO-8859-1',
                names=names
            )
            
            # Create csv File
            # read_file.to_csv(
            #     files_path + file_name + '.csv', 
            #     sep='|',
            #     index=False,
            #     encoding='utf8'
            # )
            
            # Create Dataframe
            df = pd.DataFrame(read_file)
            df = df.replace(np.nan, '')
            records = df.to_dict(orient='records')
            year = date_str[:4]
            month = date_str[4:6]
            day = date_str[6:8]
            file_date = date(int(year), int(month), int(day))
            
            # Connect DB
            db_connection = MysqlConnection(
                host=os.environ.get('MYSQL_DB_HOST'),
                user=os.environ.get('MYSQL_DB_USER'),
                password=os.environ.get('MYSQL_DB_PASSWORD'),
                database=os.environ.get('MYSQL_DB_NAME')
            )
            
            head = "INSERT INTO %s " % db_table
            columns = '(%s)' % ','.join(data)
            values = """VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            list_params = []
            for record in records:
                if db_table == 'preventiva':
                    pattern = '\S+[\@]\S+'
                    email = re.findall(pattern, record['35'], re.IGNORECASE)
                    record['35'] = email[0] if email else ''
                    
                record['36'] = file_date
                record['37'] = month
                record['38'] = file_name
                
                # remove decimals
                for i in ['14', '15', '16']:
                    try:
                        record[i] = str(int(record[i]))
                    except:
                        pass
                    
                params = tuple(record.values())
                list_params.append(params[1:38])
                    
            if list_params:                
                query = head + columns + values
                # logger.info('execute query... /n' + query)
                try:
                    db_connection.insert(query=query, params=list_params)
                except Exception as e:
                    logger.error(str(e))
                   
            new_folder = day + '-' + month + '-' + year
            current_path = 'files/' + path
            move_to = 'files/' + new_folder
            create_folder(move_to)
            shutil.move(current_path, move_to)

def create_folder(folder, logger):
    """ Create folder if exist"""
    full_path = DIR_PATH + '/' + folder
    if not os.path.isdir(full_path):
        # not present then create it.
        os.makedirs(full_path)