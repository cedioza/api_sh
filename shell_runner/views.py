
import os
import logging
import subprocess
from rest_framework.decorators import api_view
from rest_framework.response import Response


logger = logging.getLogger(__name__)


import os
import subprocess
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(['GET'])
def execute_shell_command(request):
    try:
        # Obtener la ruta actual
        ruta_actual = os.getcwd()

        logger.info(f'Ruta actual: {ruta_actual}')

        elementosP = os.listdir(ruta_actual)

        logger.info(f'elementos ruta: {elementosP}')


        # Cambiar al directorio "shell_runner"
        carpeta_deseada = "var"
        ruta_carpeta_deseada = os.path.join(ruta_actual, carpeta_deseada)
        os.chdir(ruta_carpeta_deseada)

        elementosP = os.listdir(ruta_actual)

        logger.info(f'elementos ruta: {elementosP}')

        # Cambiar al directorio "helpers"
        subcarpeta_deseada = "www"
        ruta_subcarpeta_deseada = os.path.join(ruta_carpeta_deseada, subcarpeta_deseada)
        os.chdir(ruta_subcarpeta_deseada)

        

        # Obtener una lista de elementos en la subcarpeta deseada
        elementos = os.listdir(ruta_subcarpeta_deseada)

        logger.info(f'Elementos en la subcarpeta "{subcarpeta_deseada}": {elementos}')

        return Response({'ruta_actual': ruta_actual, 'elementos_subcarpeta': elementos})

    except Exception as e:
        error_message = 'Ocurrió un error: {}'.format(str(e))
        logger.exception(error_message)
        return Response({'error': error_message}, status=500)