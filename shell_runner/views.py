import subprocess
import os
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)

@api_view(['GET'])
def execute_shell_command(request):
    script_path = request.query_params.get('script_path')

    if not script_path:
        return Response({'error': 'No se proporcionó una ruta de script.'}, status=400)

    try:
        # Verificar si el archivo del script existe
        if not os.path.exists(script_path):
            return Response({'error': 'El archivo del script no existe.'}, status=404)

        # Ejecutar el script utilizando subprocess
        result = subprocess.check_output(['python', script_path], stderr=subprocess.STDOUT)
        output = result.decode('utf-8')

        # Registrar información utilizando el logger
        logger.info(f'Script ejecutado: {script_path}')
        logger.info(f'Salida del script: {output}')

        return Response({
            'script_path': script_path,
            'output': output,
        })
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode('utf-8')

        # Registrar información de error utilizando el logger
        logger.error(f'Error al ejecutar el script: {script_path}')
        logger.error(f'Salida de error: {error_output}')

        return Response({'error': error_output}, status=400)
    except Exception as e:
        # Registrar información de error utilizando el logger
        logger.error(f'Error inesperado: {str(e)}')

        return Response({'error': str(e)}, status=500)
