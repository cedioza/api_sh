import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener el valor de la variable de entorno
variable_entorno = os.getenv('test')

# Crear la carpeta con el nombre de la variable de entorno
os.mkdir(variable_entorno)

# Imprimir mensaje de éxito
print(f'Carpeta "{variable_entorno}" creada exitosamente')
