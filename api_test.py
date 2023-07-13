import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de la variable de entorno
variable_entorno = os.getenv('DIR_PROJECT')

# Abrir el archivo de logs en modo de escritura
with open('logs.txt', 'w') as archivo_logs:
    # Escribir en el archivo de logs
    archivo_logs.write('Hola mundo\n')
    archivo_logs.write(f'Valor de la variable de entorno: {variable_entorno}\n')

# Imprimir mensaje de éxito
print('Archivo de logs creado exitosamente')
