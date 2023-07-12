
import os
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .Helpers import helper

logger = logging.getLogger(__name__)


@api_view(['GET'])
def execute_shell_command(request):
    try:
        logger.info('Start process...')
        logger.info('create folder files')
        helper.create_folder('files')
        logger.info('create folder logs')
        helper.create_folder('logs')

        helper.execute_process()
        DIR_PATH = os.getcwd() + os.environ.get('DIR_PROJECT', '')
        logger.info('DIR_PATH: ' + DIR_PATH)

        logger.info('End process...')

        return Response({'message': 'prueba', 'dir': DIR_PATH, 'data_ext': os.getenv('DIR_PROJECT')}, status=200)

    except Exception as e:
        error_message = 'An error occurred: {}'.format(str(e))
        logger.error(error_message)
        return Response({'error': error_message,"directorio":os.environ.get('DIR_PROJECT', '--')}, status=500)
