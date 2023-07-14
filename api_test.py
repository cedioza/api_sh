from decouple import config
import os

# Obtener el valor de la variable de entorno
variable_entorno = config('TEST')



# Crear la carpeta con el nombre de la variable de entorno
os.mkdir(variable_entorno)

# Imprimir mensaje de éxito
print(f'Carpeta "{variable_entorno}" creada exitosamente')
