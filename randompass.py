import random
# caracteres permitidos en la generacion del password
db = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#%&*/_+?."


def setpass(longitud):
    # Crea una contraseña segun la cantidad de caracteres que se soiciten
    password = "".join(random.sample(db, longitud))
    return password


if __name__ == '__main__':
    print(setpass(5))
