import random
# caracteres permitidos en la generacion del password
lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
number ="1234567890"
simbols = "@#%&*/_+?."
db = lower+upper+number+simbols


def setpass(length):
    # Crea una contraseña segun la cantidad de caracteres que se soiciten
    password = "".join(random.sample(db, length))
    return password


if __name__ == '__main__':
    setpass(5)
