
import os
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .Helpers import helper

logger = logging.getLogger(__name__)


@api_view(['GET'])
def execute_shell_command(request):

    # DIR_PATH = os.getcwd() + os.environ.get('DIR_PROJECT', '')

    logger.info('Start process...') 
    logger.info('create folder files') 

    helper.create_folder('files')
    logger.info('create folder logs') 
    helper.create_folder('logs')
    #         # Configuración del archivo de registro
    # file_handler = logging.FileHandler('logs/colmena.log')
    # formatter = logging.Formatter('%(asctime)s [%(name)s]:%(levelname)s [%(filename)s, %(funcName)s(), line %(lineno)d] %(message)s')
    # file_handler.setFormatter(formatter)
    
    # # Agregar el manejador de archivo al logger
    # logger.addHandler(file_handler)
    
    # # Configuración del nivel de registro
    # logger.setLevel(logging.DEBUG)
    # file_handler.setLevel(logging.DEBUG)
    
    # Ejemplos de mensajes de registro

    helper.execute_process()
    DIR_PATH = os.getcwd() + os.environ.get('DIR_PROJECT', '')
    logger.info('DIR_PATH: ' + DIR_PATH)

    logger.info('End process...')


    return Response({'message': "prueba","dir":DIR_PATH,"data ext":os.getenv("DIR_PROJECT")}, status=200)