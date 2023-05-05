from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mg

import centerwindow
import guimaster
import DBConexion


class Login:
    def log(self):
        user = self.usermaster.get()
        key = self.passmaster.get()
        conexion = DBConexion.logindbmaster(user, key)

        if conexion:  # Se evalua True o False
            # Si se puede logear se puede ingresar a la base de datos
            self.master.destroy()
            guimaster.Aplicacion()
        else:
            mg.showerror(message="Usuario o cotraseña incorrectos", title="Login")

    def newuser(self):
        # Crea una nueva base de datos con un nuevo usuario
        if self.usermaster.get() and self.passmaster.get():
            mg.showinfo(message="Esta accion borrara la base de datos anterior y no se podra recuperar.")
            new = DBConexion.nuevadb(self.usermaster.get(), self.passmaster.get())
            mg.showinfo(message="Nueva base de datos creada correctamente")
        else:
            mg.showinfo(message="Debe rellenar todos los campos para crear la nueva DB", title="Login")

    def close_win(self, e):
        # Funcion para cerrar la ventana
        self.master.destroy()

    def __init__(self):
        # crea la ventana de acceso
        self.ancho = 220
        self.alto = 120
        self.master = Tk()
        self.master.geometry("%dx%d" % (self.ancho, self.alto))
        self.master.title('BOXPASS')
        self.master.resizable(False, False)
        # self.master.iconphoto(True, PhotoImage(file='xbox.png'))
        self.master.update()
        centerwindow.centrar(self.master, self.ancho, self.alto)
        # Asocia una tecla -ENTER- para llanar a una funcion
        self.master.bind('<Return>', lambda event: self.log())
        # Asocia una tecla -ESC- para llanar a una funcion
        self.master.bind('<Escape>', lambda e: self.close_win(e))

        user = StringVar()
        password = StringVar()

        self.usuariolbl = ttk.Label(self.master, text='Usuario:')
        self.usuariolbl.place(x=25, y=5)
        self.usermaster = ttk.Entry(self.master, textvariable=user)
        self.usermaster.focus()
        self.usermaster.place(x=90, y=5, width=100)

        ttk.Label(self.master, text='Password:').place(x=25, y=40)
        self.passmaster = ttk.Entry(self.master, textvariable=password, show="*")
        self.passmaster.place(x=90, y=40, width=100)

        self.intro = ttk.Button(self.master, text='Iniciar Sesion', command=self.log)
        self.intro.place(x=10, y=80)

        ttk.Button(self.master, text='Crear nueva cuenta', command=self.newuser).place(x=100, y=80)

        self.master.mainloop()


def main():
    mi_app = Login()
    return 0


if __name__ == "__main__":
    main()
