from plyer import notification
import uuid


def nmensaje(mensaje):
    # Notificacion en el escritorio de windows
    # NO esta incluido en la segunda version porque al momento de crear el .exe arroja error
    notification.notify(
        title="BOXPASS",
        message=mensaje,
        app_name="BOXPASS",
        app_icon="xbox.ico",
        timeout=10
    )


def get_mac_dir():
    # Obtiene el numero de serie del disco duro
    # Si por alguna circunstancia se modifica la serie como el craceo de un keygen el numero cambia por lo
    # que se podria perder la base de datos
    return hex(uuid.getnode())


if __name__ == "__main__":
    print(get_mac_dir())
