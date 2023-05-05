import os
from tkinter import messagebox as mg


def check_file():
    carpeta_personal = os.path.expanduser('~')

    # Nombre de la carpeta en la que se creará el archivo
    nombre_carpeta = 'database'

    # Nombre del archivo por defecto a crear
    nombre_archivo = '0001key.db'

    # Ruta completa de la carpeta
    ruta_carpeta = os.path.join(carpeta_personal, nombre_carpeta)

    # Ruta completa del archivo a crear
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)

    # Verifica si el archivo ya existe
    if not os.path.exists(ruta_archivo):
        # Avisa si no existe el archivo
        mg.showerror(message='No se encuentra la Base de Datos en la ruta especificada. Cree un nuevo usuario.', title='Error!!')
    else:
        return ruta_archivo


def new_filedb():
    # Obtiene la ruta de la carpeta personal del usuario
    carpeta_personal = os.path.expanduser("~")

    # Nombre de la carpeta en la que se creará el archivo
    nombre_carpeta = "database"

    # Nombre del archivo por defecto a crear
    nombre_archivo = "0001key.db"

    # Ruta completa de la carpeta
    ruta_carpeta = os.path.join(carpeta_personal, nombre_carpeta)

    # Ruta completa del archivo a crear
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)

    # Verifica si la carpeta ya existe
    if not os.path.exists(ruta_carpeta):
        # Crea la carpeta si no existe
        os.makedirs(ruta_carpeta)
        # print(f"Se ha creado la carpeta '{nombre_carpeta}' en la carpeta personal.")

    # Verifica si el archivo ya existe
    if not os.path.exists(ruta_archivo):
        # Crea el archivo si no existe
        with open(ruta_archivo, "w+") as archivo:
            archivo.close()
        # print(f"Se ha creado el archivo '{nombre_archivo}' en la carpeta '{nombre_carpeta}'.")
        return ruta_archivo


if __name__ == '__main__':
    # check_file()
    new_filedb()
