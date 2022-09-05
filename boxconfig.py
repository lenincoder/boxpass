from plyer import notification
from ctypes import byref, c_char_p, c_int, windll
import uuid


def nmensaje(mensaje):
    # Notificacion en el escritorio de windows
    notification.notify(
        title="BOXPASS",
        message=mensaje,
        app_name="BOXPASS",
        app_icon="xbox.ico",
        timeout=10
    )


def get_serial_number(volume=None):
    # Obtiene el numero de serie del disco duro
    serial_number = c_int(0)
    windll.kernel32.GetVolumeInformationA(
        c_char_p(volume) if volume is not None else None, None, 0, byref(serial_number), 0, None, None, 0
    )
    return serial_number.value


def get_mac_dir():
    return hex(uuid.getnode())


if __name__ == "__main__":
    s = get_mac_dir()
    print(s)
