import os
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def execute_shell_command(request):
    file_path = request.query_params.get('file_path')

    if not file_path:
        return Response({'error': 'No se proporcionó una ruta de archivo.'}, status=400)

    try:
        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            return Response({'error': 'El archivo no existe.'}, status=404)

        # Ejecutar el comando
        output = os.popen(file_path).read().strip()

        return Response({
            'file_path': file_path,
            'output': output,
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)
