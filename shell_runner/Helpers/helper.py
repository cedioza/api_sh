import pandas as pd
import re
import numpy as np
import os, shutil
from datetime import date, datetime
from .conn_db import MysqlConnection
from .constants import (COLSPECS_COBRO, COLSPECS_COBRO_46, COLSPECS_PREV, 
                        COLSPECS_PREV_24, COLUMNS_DB)


ruta_actual = os.getcwd()

ruta_actual = os.path.join(ruta_actual, "var", "www", "html", "api_sh")
# Cambiar al directorio deseado
os.chdir(ruta_actual)

def create_folder(folder, logger):
    logger.info(f'Ruta actual: {folder}')
    # Crear la carpeta con el nombre de la variable de entorno si no existe
    if not os.path.exists(folder):
        os.mkdir(folder)
        # Registrar mensaje de éxito
        logger.info(f'Carpeta "{folder}" creada exitosamente')

def execute_process(logger):
    logger.info("Comienzo de proceso ")

    """ Load directory path local and save mysql data """
    # list file and directories
    files_path = os.path.join(ruta_actual, 'files')
    logger.info(f"ruta actual para proceso: {files_path}")
    logger.info(f"listado de archivos: {os.listdir(files_path)}")

    for path in os.listdir(files_path):
        if os.path.isfile(os.path.join(files_path, path)):
            logger.info('Processing file: ' + path)
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



            read_file = pd.read_fwf(
                os.path.join(files_path, path),
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
            # db_connection = MysqlConnection(
            #     host=os.environ.get('MYSQL_DB_HOST'),
            #     user=os.environ.get('MYSQL_DB_USER'),
            #     password=os.environ.get('MYSQL_DB_PASSWORD'),
            #     database=os.environ.get('MYSQL_DB_NAME')
            # )

            # logger.info(f"conexion base de datos")


            # head = "INSERT INTO %s " % db_table
            # columns = '(%s)' % ','.join(data)
            # values = """VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            #     %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            # """

            # logger.info(f"Información insertada con éxito en la tabla {db_table}")
            # list_params = []
            # for record in records:
            #     if db_table == 'preventiva':
            #         pattern = '\S+[\@]\S+'
            #         email = re.findall(pattern, record['35'], re.IGNORECASE)
            #         record['35'] = email[0] if email else ''

            #     record['36'] = file_date
            #     record['37'] = month
            #     record['38'] = file_name

            #     # remove decimals
            #     for i in ['14', '15', '16']:
            #         try:
            #             record[i] = str(int(record[i]))
            #         except:
            #             pass

            #     params = tuple(record.values())
            #     list_params.append(params[1:38])

            # if list_params:
            #     query = head + columns + values
            #     try:
            #         db_connection.insert(query=query, params=list_params)
            #         logger.info(f"se inserto con extio  carpeta ")

            #     except Exception as e:
            #         logger.info(f"error insertando base de datos ")

            #         logger.error(str(e))

            new_folder = day + '-' + month + '-' + year
            logger.info(f"nombre carpeta: {new_folder}")
            current_path = os.path.join(files_path, path)
            logger.info(f"current path actual: {current_path}")

            move_to = os.path.join(files_path, new_folder)
            files_path = os.path.join(ruta_actual, 'files')
            logger.info(f"ruta actual para proceso: {files_path}")
            logger.info(f"listado de archivos: {os.listdir(files_path)}")
            logger.info(f"moviendo carpeta ")
            logger.info(f" ruta a mover :{move_to}")
            create_folder(move_to,logger)
            logger.info(f"muere intentando mover  carpeta ")
            shutil.move(current_path, move_to)

            logger.info("Proceso Finalizado ")
