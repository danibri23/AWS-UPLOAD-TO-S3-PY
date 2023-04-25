Este script es un programa que te ayuda a guardar archivos en un bucket S3 de AWS usando el servidor de Flask. Tiene dos partes: una para elegir el archivo y otra para enviarlo y guardarlo.

- Primeramente se debe configurar un virtual enviroment
- Luego se decarga los requerimientos
- Por ultimo correr el script

Datos

- aws sts get-session-token
  Con este comando se consigue los datos temporales para configurar el .env y tener que instalar amazon cli, localmente.
