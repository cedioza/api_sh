import pandas as pd
import re
import numpy as np
import os, shutil
from dotenv import load_dotenv
from datetime import date, datetime
from .conn_db import MysqlConnection
from .constants import (COLSPECS_COBRO, COLSPECS_COBRO_46, COLSPECS_PREV, 
                        COLSPECS_PREV_24, COLSPECS_COBRO_VT,
                        COLSPECS_PREV_VT, COLUMNS_DB)
load_dotenv()



def create_folder(folder, logger):
    logger.info(f'Ruta actual: {folder}')
    # Crear la carpeta con el nombre de la variable de entorno si no existe
    if not os.path.exists(folder):
        os.mkdir(folder)
        # Registrar mensaje de éxito
        logger.info(f'Carpeta "{folder}" creada exitosamente')

def execute_process(logger):
    logger.info("Comienzo de proceso ")

    
    # Guardar la ruta actual
    ruta_principal = os.getcwd()
    # print("ruta principal", ruta_principal)
    ruta_actual ='/var/www/html/api_sh/files'
    
    
   
    # Verificar si ya estás en la ruta principal
    if ruta_actual != ruta_principal:
        logger.info(f'se encuentra en la ruta diferente "{ruta_principal}"')


        # Cambiar al directorio deseado
        ruta_actual = os.path.join(ruta_principal, "var", "www", "html", "api_sh", "files")
        # ruta_actual = os.path.join(ruta_principal,"files")
        
        os.chdir(ruta_actual)
    logger.info(f'se encuentra en la ruta igual {ruta_actual}')
    logger.info(f"test env -- { os.environ.get('MYSQL_DB_HOST')}")
   
    
    os.chdir(ruta_actual)

    """ Load directory path local and save mysql data """
    # list file and directories

    logger.info(f"ruta actual para proceso: {ruta_actual}")
    logger.info(f"listado de archivos: {os.listdir(ruta_actual)}")

    for path in os.listdir(ruta_actual):
        if os.path.isfile(os.path.join(ruta_actual, path)):
            logger.info('Processing file: ' + path)

            logger.info(f"inicia proceso dataframe carpeta ")

            # extract the file name and extension
            split_tup = os.path.splitext(path)
            file_name, _ = split_tup

            names = []
            data = COLUMNS_DB[:34]
            if file_name.lower().startswith('cobro'):
                date_str = file_name[21:29]
                if file_name.lower().endswith("_46") :
                    db_table = 'cobro_46'
                    data.extend(['fecha_dia_46', 'mes_a_trabajar', 'nombre_db'])
                    colspecs = COLSPECS_COBRO_46
                    for i in range(1, 36, 1):
                        names.append(str(i))
                        
                    print(f"file_name: {file_name}, table = {db_table} date = {date_str} ")
                    print("---------------")  
                    
                elif file_name.lower().endswith("46_vt"):
                    db_table = 'cobro_46'
                    colspecs = COLSPECS_COBRO_VT
                    data.extend(['fecha_dia_46', 'mes_a_trabajar', 'nombre_db'])
                    date_str = file_name.replace('-','').split('_')[1]
                    for i in range(1, 36, 1):
                        names.append(str(i))
                        
                    print(f"file_name: {file_name}, table = {db_table} date = {date_str} ")
                    print("---------------")  
                        
                elif file_name.lower().endswith("_31") :
                    db_table = 'cobro'
                    colspecs = COLSPECS_COBRO
                    data.extend(['fecha_entrega_colmena', 'mes_a_trabajar', 'nombre_db'])
                    for i in range(1, 39, 1):
                        names.append(str(i))
                        
                    print(f"file_name: {file_name}, table = {db_table} date = {date_str} ")
                    print("---------------")  
                        
                elif file_name.lower().endswith("31_vt") :
                    db_table = 'cobro'
                    colspecs = COLSPECS_COBRO_VT
                    data.extend(['fecha_entrega_colmena', 'mes_a_trabajar', 'nombre_db'])
                    date_str = file_name.replace('-','').split('_')[1]
                    for i in range(1, 36, 1):
                        
                        names.append(str(i))
                        
                    print(f"file_name: {file_name}, table = {db_table} date = {date_str} ")
                    print("---------------")  
                        
            elif file_name.lower().startswith('preventiva'):
                date_str = file_name[26:34]
                if file_name.lower().endswith("21") :
                    db_table = 'preventiva'
                    colspecs = COLSPECS_PREV
                    data.extend(['fecha_entrega_colmena', 'mes_a_trabajar', 'nombre_db'])
                    date_str= file_name.replace('-','').split('_')[2]
                    for i in range(1, 36, 1):
                        names.append(str(i))
                        
                    print(f"file_name: {file_name}, table = {db_table} date = {date_str} ")
                    print("---------------")  
                        
                elif file_name.lower().endswith("21_vt") :
                    db_table = 'preventiva'
                    colspecs = COLSPECS_PREV_VT
                    data.extend(['fecha_entrega_colmena', 'mes_a_trabajar', 'nombre_db'])
                    
                    
                    date_str  = file_name.replace('-','').split('_')[1]
                    for i in range(1, 36, 1):
                        names.append(str(i))
                    print(f"file_name: {file_name}, table = {db_table} date = {date_str} ")
                    print("---------------")                        
                        
                        
                elif file_name.lower().endswith("_24") :
                    db_table = 'preventiva_24'
                    colspecs = COLSPECS_PREV_24
                    data.extend(['fecha_dia_24', 'mes_a_trabajar', 'nombre_db'])
                    date_str= file_name.replace('-','').split('_')[2]
                    for i in range(1, 36, 1):
                        names.append(str(i))
                    
                    print(f"file_name: {file_name}, table = {db_table} date = {date_str} ")
                    print("---------------")      
                        
                elif file_name.lower().endswith("24_vt")  :
                    db_table = 'preventiva_24'
                    colspecs = COLSPECS_PREV_VT
                    data.extend(['fecha_dia_24', 'mes_a_trabajar', 'nombre_db'])
                    
                    date_str= file_name.replace('-','').split('_')[1]
                    for i in range(1, 36, 1):
                        names.append(str(i))
                    
                    print(f"file_name: {file_name}, table = {db_table} date = {date_str} ")
                    print("---------------")      
                        
                    
            else:
                continue



            read_file = pd.read_fwf(
                os.path.join(ruta_actual, path),
                # skiprows=36,
                # skipfooter=5,
                colspecs=colspecs,
                encoding='ISO-8859-1',
                names=names
            )


            # Create csv File
            # read_file.to_csv(
            #     ruta_actual + file_name + '.csv', 
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
            logger.info(f"Termina proceso de dataframe")


            # Connect DB
            db_connection = MysqlConnection(
                host=os.environ.get('MYSQL_DB_HOST'),
                user=os.environ.get('MYSQL_DB_USER'),
                password=os.environ.get('MYSQL_DB_PASSWORD'),
                database=os.environ.get('MYSQL_DB_NAME')
            )
            logger.info(f"informacion database - host {os.environ.get('MYSQL_DB_HOST')} - username {os.environ.get('MYSQL_DB_USER')} - password {os.environ.get('MYSQL_DB_PASSWORD')}")


            logger.info(f"conexion base de datos")


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
            logger.info(f"creando consulta para insertar  ")

            if list_params:
                query = head + columns + values
                try:
                    db_connection.insert(query=query, params=list_params)
                    logger.info(f"se inserto con extio  en base de datos ")

                except Exception as e:
                    logger.info(f"error insertando base de datos ")

                    logger.error(str(e))

            new_folder = day + '-' + month + '-' + year
            logger.info(f"nombre carpeta: {new_folder}")
            current_path = os.path.join(ruta_actual, path)
            logger.info(f"current path actual: {current_path}")

            move_to = os.path.join(ruta_actual, new_folder)
            logger.info(f"ruta actual para proceso: {ruta_actual}")
            logger.info(f"listado de archivos: {os.listdir(ruta_actual)}")
            logger.info(f"moviendo carpeta ")
            logger.info(f" ruta a mover :{new_folder}")
            create_folder(new_folder,logger)
            shutil.move(current_path, move_to)

            logger.info("Proceso Finalizado ")

    logger.info(f"ya no hay archivos para procesar para proceso: {ruta_actual}")
    logger.info(f"listado de archivos: {os.listdir(ruta_actual)}")

