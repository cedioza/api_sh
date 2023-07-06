
# Repositorio prueba técnica de SMART DATA en Python


### Librerías :
- Django: [Documentación de Django](https://docs.djangoproject.com/)
- Django REST Framework: [Documentación de Django REST Framework](https://www.django-rest-framework.org/)


## Estructura 
## api_sh
```
.
├── api_sh/
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
```
## Shell_Runner
```
├── shell_runner
│ ├── migrations/
│ ├── init.py
│ ├── admin.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── manage.py
└── requirements.txt
```

## Instalación

Sigue estos pasos para configurar el proyecto localmente:

1. Clona el repositorio:

```bash
git clone https://github.com/cedioza/api_sh.git
```
Crea y activa un entorno virtual:
```
python3 -m venv nombre_del_entorno_virtual
source nombre_del_entorno_virtual/bin/activate
```
Instala las dependencias del proyecto:
```
pip install -r requirements.txt
```
```
## Requisito 

Este proyecto tiene los siguientes endpoints:

/api/shell/?file_path= 
En este enpoint pasamos la ruta con el archivo sh el cual deseamos ejecutar 

http://127.0.0.1:8000/api/shell/?file_path=/home/drask390/linux.sh
