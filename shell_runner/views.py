
import os
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .Helpers import helper

logger = logging.getLogger(__name__)


# @api_view(['GET'])
# def execute_shell_command(request):
#     try:
#         # logger.info('Start process...')
#         # logger.info('create folder files')


#         # helper.create_folder('files')
#         # logger.info('create folder logs')
#         # helper.create_folder('logs')

#         # helper.execute_process()
#         # DIR_PATH = os.getcwd() + os.environ.get('DIR_PROJECT', '')
#         # logger.info('DIR_PATH: ' + DIR_PATH)



#         logger.info('End process...')

#         return Response({'message': 'prueba', 'dir': DIR_PATH, 'data_ext': os.getenv('DIR_PROJECT')}, status=200)

#     except Exception as e:
#         error_message = 'An error occurred: {}'.format(str(e))
#         logger.error(error_message)
#         return Response({'error': error_message,"directorio":os.environ.get('DIR_PROJECT', '--')}, status=500)

@api_view(['GET'])
def execute_shell_command(request):
    try:


        logger.info('Start process...')
        # Obtener la ruta del directorio principal (home)
        directorio_principal = os.path.expanduser("~")
        logger.info('Start Home ', directorio_principal)

        try:

            os.chdir(directorio_principal)
            mensaje = f"Cambiado al directorio principal: {directorio_principal}"
            logger.info(mensaje)

        except OSError:
            mensaje = f"No se pudo cambiar al directorio principal: {directorio_principal}"
            return Response({'error': mensaje}, status=500)





        # Obtener la lista de archivos en la ruta final
        archivos_en_ruta_objetivo = os.listdir(directorio_principal)
        logger.info('Start colmena_cobros ', archivos_en_ruta_objetivo)


    except Exception as e:
        error_message = 'An error occurred: {}'.format(str(e))
        logger.error(error_message)
        return Response({'error': error_message,"directorio":os.environ.get('DIR_PROJECT', '--')}, status=500)


    # Devolver la lista de archivos en la respuesta
    return Response(archivos_en_ruta_objetivo)


@api_view(['GET'])
def change_to_home_directory(request):
    # Obtener la ruta del directorio principal (home)
    directorio_principal = os.path.expanduser("~")

    # Cambiar al directorio principal
    try:
        os.chdir(directorio_principal)
        mensaje = f"Cambiado al directorio principal: {directorio_principal}"
        return Response({'mensaje': mensaje})
    except OSError:
        mensaje = f"No se pudo cambiar al directorio principal: {directorio_principal}"
        return Response({'error': mensaje}, status=500)