# Proyect

## PRA2 Data Visualizations

En este repositorio contiene el código fuente de la PRA2 de la asignatura de Visualización de Datos del Máster en 
Ciencia de Datos de la UOC. La autoría de este código corre a cargo de Daniel Alves Yáñez.

## Enlace Acceso a la PRA2

-  https://pra2proyect.herokuapp.com/

## HOWTO

Descarga y preparación del entorno.
```bash
 # Get the code
 git clone https://...
 
# Virtualenv modules installation (Unix based systems)
 virtualenv env
 source env/bin/activate

 # Virtualenv modules installation (Windows based systems)
 # virtualenv env
 # .\env\Scripts\activate
```

Lanzar la aplicación en local.
```bash
 # Start the application (development mode)
 python manage.py runserver # default port 8000

 # Start the app - custom port
 # python manage.py runserver 0.0.0.0:<your_port>

 # Access the web app in browser: http://127.0.0.1:8000/
```
