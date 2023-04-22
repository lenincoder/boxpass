import sqlite3
from hashlib import md5
from hmac import compare_digest
import cryptocode


def cifrado(keyword):
    # Cifrado de una cadena, devuelve una cadena hexadecimal
    encrypt = md5(keyword.encode('utf-8')).hexdigest()
    return encrypt


def verify(cadenaencriptada, cadenasinencriptar):
    # Compara que una encriptacion no haya sido alterada
    stringclient = md5(cadenasinencriptar.encode('utf-8')).hexdigest()  # Encripta una cadena
    return compare_digest(cadenaencriptada, stringclient)   # regresa True o False


def make_a_key():
    # Hace una consulta la db para extraer en nombre de usuario y formar una key
    conexion = sqlite3.connect("database/key.db")
    cursor = conexion.cursor()
    # cursor.execute("SELECT * FROM consumer WHERE name=? AND clave=?", (superuser, superpass))
    cursor.execute("SELECT name FROM consumer")
    resultado = cursor.fetchone()
    namedb = resultado[0]
    cursor.close()
    conexion.close()
    # Crea una palabra clave en base al nombre del usuario para desemcriptar
    if len(namedb) > 0:
        dokey = '2022'+namedb[:4]+'lml'
        return dokey


def encript(toencript, keyword):
    # Encripta una cadena mediante la utilizacion de una palabra clave
    # ESTRUCTURA: cryptocode.encrypt("CADENA A ENCRIPTAR", "PALABRA CLAVE")
    # https://www.delftstack.com/es/howto/python/python-encrypt-string/
    str_encoded = cryptocode.encrypt(toencript, keyword)
    return str_encoded


def decrypt(todecript, keyword):
    # Desecripta una cadena con la utilizacion de una palabra clave
    # ESTRUCTURA: cryptocode.decrypt("CADENA ENCRYPTADA", "PALABRA CLAVE PARA DESEMCRIPTAR")
    str_decoded = cryptocode.decrypt(todecript, keyword)
    return str_decoded


if __name__ == '__main__':
    # cadena = cifrado('hola mundo')
    # print(cadena)
    # print(verify(cadena, 'hola mundo'))
    print(make_a_key())
