import sqlite3
import security as sc

# https://datacarpentry.org/python-ecology-lesson-es/09-working-with-sql/index.html
# https://www.tutorialesprogramacionya.com/pythonya/detalleconcepto.php?punto=88&codigo=89&inicio=75


def logindbmaster(usermaster, passmaster):
    # Accede a la cuenta de usuario para logearse

    conexion = sqlite3.connect("database/key.db")
    cursor = conexion.cursor()
    # cursor.execute("SELECT * FROM consumer WHERE name=? AND clave=?", (superuser, superpass))
    cursor.execute("SELECT name, clave FROM consumer")
    resultado = cursor.fetchone()
    namedb = resultado[0]
    clavedb = resultado[1]

    if sc.verify(namedb, usermaster) and sc.verify(clavedb, passmaster):
        cursor.close()
        conexion.close()
        return True
    else:
        cursor.close()
        conexion.close()
        return False


def nuevadb(usermaster, passmaster):
    # Crear una nueva base de datos
    conexion = sqlite3.connect("database/key.db")
    conexion.commit()
    cursor = conexion.cursor()

    # Borrar tablas de la base de datos https://www.sqlitetutorial.net/sqlite-drop-table/
    cursor.execute("DROP TABLE IF EXISTS consumer")
    cursor.execute("DROP TABLE IF EXISTS datapass")
    conexion.commit()

    # Crear tablas
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS consumer (
        name TEXT NOT NULL UNIQUE,
        clave TEXT NOT NULL UNIQUE
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS datapass (
        id INTEGER NOT NULL,
        sitio TEXT NOT NULL,
        usuario TEXT NOT NULL,
        passw TEXT NOT NULL,
        PRIMARY KEY(id AUTOINCREMENT)
        )"""
    )
    conexion.commit()

    # Rellenar datos con datos encriptados
    newuser = sc.cifrado(usermaster)
    newpass = sc.cifrado(passmaster)
    # Rellenar la base con el nuevo usuario
    cursor.execute("INSERT INTO consumer VALUES(?,?)", (newuser, newpass))
    conexion.commit()
    conexion.close()


if __name__ == '__main__':
    logindbmaster('vicente', '9874')
