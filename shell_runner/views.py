import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from subprocess import run, PIPE

@api_view(['GET'])
def execute_shell_command(request):
    file_path = request.query_params.get('file_path')

    if not file_path:
        return Response({'error': 'No se proporcionó una ruta de archivo.'}, status=400)

    try:
        # Cambia los permisos del archivo para otorgar el permiso de ejecución
        os.chmod(file_path, 0o755)

        # Ejecuta el comando
        result = run(file_path, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        return Response({
            'file_path': file_path,
            'stdout': stdout,
            'stderr': stderr,
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)
