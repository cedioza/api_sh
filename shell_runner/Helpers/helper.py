import pandas as pd
import re
import numpy as np
import os, shutil
import logging
from datetime import date, datetime
from .conn_db import MysqlConnection
from .constants import (COLSPECS_COBRO, COLSPECS_COBRO_46, COLSPECS_PREV, 
                        COLSPECS_PREV_24, COLUMNS_DB)





DIR_PATH = os.getcwd() + os.environ.get('DIR_PROJECT', '')


def create_folder(folder):
    """ Create folder if exist"""
    full_path = DIR_PATH + '/' + folder
    if not os.path.isdir(full_path):
        # not present then create it.
        os.makedirs(full_path)


def execute_process():   
    """ Load directory path local and save mysql data """
    # list file and directories
    files_path = DIR_PATH + '/files/'
    logging.info(files_path)
    for path in os.listdir(files_path):
        if os.path.isfile(os.path.join(files_path, path)):
            logging.info('Precessing file: ' + path)
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
            
            logging.info('db_table: ' + db_table)
                
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
                # logging.info('execute query... /n' + query)
                try:
                    db_connection.insert(query=query, params=list_params)
                except Exception as e:
                    logging.error(str(e))
                   
            new_folder = day + '-' + month + '-' + year
            current_path = 'files/' + path
            move_to = 'files/' + new_folder
            create_folder(move_to)
            shutil.move(current_path, move_to)
                    
        
if __name__ == '__main__':
    create_folder('files')
    create_folder('logs')
    logging.basicConfig(
        filename=DIR_PATH + "/logs/colmena.log", 
        format="%(asctime)s [%(name)s]:%(levelname)s [%(filename)s, %(funcName)s(), line %(lineno)d] %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S", 
        level=logging.DEBUG,
        # filemode="w", 
    )

    

        
    
    logging.info('Start process...')    
    logging.info('DIR_PATH: ' + DIR_PATH)
    execute_process()
    logging.info('End process...')
    
    