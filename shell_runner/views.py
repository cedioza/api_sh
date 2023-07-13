
import os
import logging
import subprocess
from rest_framework.decorators import api_view
from rest_framework.response import Response



from dotenv import load_dotenv

load_dotenv()



logger = logging.getLogger(__name__)
    

@api_view(['GET'])
def execute_shell_command(request):
    try:
        # Obtener la ruta actual
        ruta_actual = os.getcwd()

        logger.info(f"Ruta por variable de entorno : {os.environ.get('DIR_PROJECT', 'no_fount')}")
        logger.info(f'Ruta actual: {ruta_actual}')

        # Construir la ruta completa
        ruta_deseada = os.path.join(ruta_actual, "var", "www", "html", "api_sh")

        # Cambiar al directorio deseado
        os.chdir(ruta_deseada)

        # Obtener una lista de elementos en la ruta deseada
        elementos = os.listdir(ruta_deseada)

        logger.info(f'Elementos en la ruta "{ruta_deseada}": {elementos}')

        # Ejecutar el archivo "prueba.py" en la ruta deseada
        archivo_prueba = os.path.join(ruta_deseada, "api_test.py")
        resultado = subprocess.run(['python', archivo_prueba], capture_output=True, text=True)

        logger.info(f'Archivo "prueba.py" ejecutado correctamente. Salida: {resultado.stdout}')

        # Restablecer la ruta actual
        os.chdir(ruta_actual)

        return Response({'ruta_actual': ruta_actual, 'elementos_ruta': elementos})

    except Exception as e:
        error_message = 'Ocurrió un error: {}'.format(str(e))
        logger.exception(error_message)
        return Response({'error': error_message}, status=500)