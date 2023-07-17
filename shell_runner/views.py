import os
import logging
import subprocess
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .Helpers import helper

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

@api_view(['GET'])
def execute_shell_command(request):
    try:
        # Obtener la ruta actual

         # Ejecutar el archivo "script.sh" en la ruta deseada
        logger.info('Ejecutando test() desde Helpers')
        helper.create_folder("files",logger)
        helper.execute_process(logger)


        # Construir la ruta completa
       

        return Response({'test': "ok"})

    except Exception as e:
        error_message = 'Ocurrió un error: {}'.format(str(e))
        logger.exception(error_message)
        return Response({'error': error_message}, status=500)
