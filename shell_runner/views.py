from rest_framework.decorators import api_view
from rest_framework.response import Response
from subprocess import run, PIPE

@api_view(['GET'])
def execute_shell_command(request):
    file_path = request.query_params.get('file_path')

    if not file_path:
        return Response({'error': 'No se proporcionó una ruta de archivo.'}, status=400)

    try:
        command = ['bash', file_path] 
        result = run(command, shell=False, stdout=PIPE, stderr=PIPE, text=True)
        stdout = result.stdout.strip().splitlines()
        stderr = result.stderr.strip()

        return Response({
            'file_path': file_path,
            'stdout': stdout,
            'stderr': stderr,
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)