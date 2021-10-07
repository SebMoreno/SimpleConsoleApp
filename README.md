# SimpleConsoleApp

Los lineamientos seguidos para construir este proyecto están en el archivo `Instrucciones de Desarrollo.pdf`.

# QuickStart
Dentro de un Virtual Eviroment instala los paquetes indicados en `requirements.txt`.

Abre una consola desde la carpeta `src` y ejecuta el archivo `main.py`.

# Ejecución Detallada

> Todo el proceso siguiente es válido para Windows, si se desea ejecutar en algún otro SO habría que añadir y cambiar algunos pasos.

El proyecto fue construido con `python 3.9.4` así que se debe instalar una versión compatible para ejecutar el proyecto.

Es necesario crear un Virtual Eviroment, para lo cual puedes usar el siguiente comando usando un nombre que desees:
```
python -m venv [name]
```

Una vez creado el VE debes activarlo:
```
[name]\Scripts\activate
```

Ahora ingresa a la raíz del proyecto e instala todos los paquetes necesarios:
```
pip install -r requirements.txt
```

Finalmente para iniciar el programa debes estar dentro de la carpeta `src` y ejecutar el archivo `main.py`.
Esto lo puedes hacer de la siguiente manera:
```
cd src
python ./main.py
```
