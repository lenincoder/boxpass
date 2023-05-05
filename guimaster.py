import tkinter
from tkinter import *
from tkinter import ttk, messagebox
import pyperclip as pc
import sqlite3

import centerwindow
import randompass as rp
# from boxconfig import get_mac_dir
from security import make_a_key, encript, decrypt
from path import check_file


class Aplicacion:

    def call_randompass(self):
        # funcion para crear una contraseña aleatoriamente

        sizepass = int(self.spvalor.get())  # obtiene el valor actual del SpinBox
        obtenerpass = rp.setpass(sizepass)  # obtiene password aleatorio

        self.entrypass.delete(0, tkinter.END)  # borra lo existente en el wiget
        self.entrypass.insert(0, obtenerpass)  # ingresa el nuevo password

    def __init__(self):
        # crea la ventana
        self.ancho = 600
        self.alto = 400
        self.raiz = Tk()
        self.raiz.geometry("%dx%d" % (self.ancho, self.alto))
        self.raiz.title('BOXPASS')
        self.raiz.resizable(False, False)
        self.raiz.update()
        centerwindow.centrar(self.raiz, self.ancho, self.alto)

        # Variables y constantes
        self.id = StringVar()
        self.checkbox_value = IntVar()
        self.hidekey = make_a_key()  # Crea una llave
        my_var = IntVar(self.raiz)  # valor por defecto del Spinbox
        my_var.set(5)

        # Widgets
        self.spvalor = ttk.Spinbox(self.raiz, from_=5, to=15, textvariable=my_var, wrap=True, state='readonly')
        self.spvalor.place(x=10, y=10, width=70, height=24)
        ttk.Button(self.raiz, text='Pass Random', command=self.call_randompass).place(x=90, y=10, width=100, height=24)
        self.entrypass = ttk.Entry(self.raiz, justify=tkinter.RIGHT)
        self.entrypass.place(x=200, y=10, width=100, height=24)
        ttk.Button(self.raiz, text='Copiar', command=self.copypass).place(x=310, y=10, height=24)

        ttk.Separator(self.raiz, orient='horizontal').place(x=0, y=50, relwidth=1)

        # Entrada de datos
        ttk.Label(self.raiz, text='URL:').place(x=10, y=60)
        self.entryurl = ttk.Entry(self.raiz)
        self.entryurl.place(x=40, y=60, width=170)
        self.entryurl.focus()
        ttk.Label(self.raiz, text='USUARIO:').place(x=220, y=60)
        self.entryusuario = ttk.Entry(self.raiz)
        self.entryusuario.place(x=280, y=60, width=110)
        ttk.Label(self.raiz, text='PASSWORD:').place(x=400, y=60)
        self.entrypassword = ttk.Entry(self.raiz)
        self.entrypassword.place(x=475, y=60, width=110)
        ttk.Button(self.raiz, text='AGREGAR', command=self.agregar).place(x=10, y=90)
        ttk.Button(self.raiz, text='MODIFICAR', command=self.modificar).place(x=110, y=90)
        self.borra = ttk.Button(self.raiz, text='BORRAR', command=self.borrar)
        self.borra.place(x=210, y=90)

        # Tabla de password
        self.tabla = ttk.Treeview(self.raiz, columns=('uri', 'usuario', 'pass'))
        self.vsb = ttk.Scrollbar(self.raiz, orient='vertical', command=self.tabla.yview)
        self.vsb.place(x=575, y=120, height=230)
        self.tabla.configure(yscrollcommand=self.vsb.set)
        # Columnas de la tabla
        self.tabla.column('#0', width=40)
        self.tabla.column('uri', width=250)
        self.tabla.column('usuario', width=150)
        self.tabla.column('pass', width=130)
        # Encabezado de la tabla
        self.tabla.heading('#0', text='No')
        self.tabla.heading('uri', text='URI')
        self.tabla.heading('usuario', text='USUARIO')
        self.tabla.heading('pass', text='PASSWORD')
        self.tabla.place(x=3, y=120)
        self.tabla.bind('<Button-1>', self.select_event)

        # Menu copiar y pegar
        self.menu = Menu(self.raiz, tearoff=False)
        # self.menu.add_command(label='Copiar', command=self.popup_copy)
        self.menu.add_command(label='Copiar', command=lambda: self.raiz.focus_get().event_generate('<<Copy>>'))
        self.menu.add_command(label='Pegar', command=lambda: self.raiz.focus_get().event_generate('<<Paste>>'))
        self.entryurl.bind('<Button-3>', self.display_popup)
        self.entryusuario.bind('<Button-3>', self.display_popup)
        self.entrypassword.bind('<Button-3>', self.display_popup)

        # ttk.Checkbutton(self.raiz, text='Iniciar con windows', variable=self.checkbox_value, onvalue=1, offvalue=0, command=self.start_windows).place(x=3, y=360)

        # Widgets ocultos
        ttk.Button(self.raiz, command=self.actualizar_tabla())

        self.raiz.mainloop()

    def display_popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def agregar(self):
        # Crea un nuevo registro en la base de datos
        # Borra el contenido de los entry
        # Encripta los registros en la base de datos
        # Actualiza la tabla de datos
        if make_a_key():
            datos = encript(self.entryurl.get(), self.hidekey), encript(self.entryusuario.get(), self.hidekey), encript(self.entrypassword.get(), self.hidekey)
            midb = check_file()
            conexion = sqlite3.connect(midb)
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO datapass VALUES(null,?,?,?)", datos)
            conexion.commit()
            cursor.close()
            conexion.close()
            self.actualizar_tabla()
        else:
            messagebox.showwarning(message='No se ha podido ingresar el registro', title='ERROR!!')
        # Borra las entradas de los Entry
        self.entryurl.delete(0, END)
        self.entryusuario.delete(0, END)
        self.entrypassword.delete(0, END)
        self.entryurl.focus()

    def actualizar_tabla(self):
        # Elimina el contenido actual de la tabla y carga una actualizacion
        # Desencripta los registros de la base de datos

        midb = check_file()
        conexion = sqlite3.connect(midb)
        cursor = conexion.cursor()

        registros = self.tabla.get_children()
        for elementos in registros:
            self.tabla.delete(elementos)

        cursor.execute("SELECT id, sitio, usuario, passw FROM datapass")
        consulta = cursor.fetchall()
        for (val, sitio, usuario, passw) in consulta:
            self.tabla.insert("", END, text=val, values=(decrypt(sitio, self.hidekey), decrypt(usuario, self.hidekey), decrypt(passw, self.hidekey)))

        cursor.close()
        conexion.close()

    def modificar(self):
        # Modifica el registro seleccionado
        datos = encript(self.entryurl.get(), self.hidekey), encript(self.entryusuario.get(), self.hidekey), encript(self.entrypassword.get(), self.hidekey)
        midb = check_file()
        conexion = sqlite3.connect(midb)
        cursor = conexion.cursor()
        cursor.execute("UPDATE datapass SET sitio=?, usuario=?, passw=? WHERE id=" + self.id.get(), datos)
        conexion.commit()
        cursor.close()
        conexion.close()
        self.entryurl.focus()
        self.actualizar_tabla()
        self.entryurl.delete(0, END)
        self.entryusuario.delete(0, END)
        self.entrypassword.delete(0, END)

    def borrar(self):
        # Borra el registro seleccionado
        midb = check_file()
        conexion = sqlite3.connect(midb)
        cursor = conexion.cursor()
        try:
            if messagebox.askyesno(message='Realmente quiere borrar el registro?', title='ADVERTENCIA!!'):
                cursor.execute("DELETE FROM datapass WHERE id=" + self.id.get())
                conexion.commit()
                cursor.close()
                conexion.close()

                self.entryurl.delete(0, END)
                self.entryusuario.delete(0, END)
                self.entrypassword.delete(0, END)
                self.entryurl.focus()
                self.actualizar_tabla()

        except sqlite3.OperationalError:
            messagebox.showwarning(message='Ocurrio un error al eliminar el registro, intente seleccionar el registro antes de eliminarlo', title='ADVERTENCIA!!')
            # 'No se ha modificado la base de datos'

    def select_event(self, event):
        # Selecciona el registro y los agrega a los widget Entry
        self.entryurl.delete(0, END)
        self.entryusuario.delete(0, END)
        self.entrypassword.delete(0, END)
        try:
            item = self.tabla.identify("item", event.x, event.y)
            self.id.set(self.tabla.item(item, "text"))
            self.entryurl.insert(0, self.tabla.item(item, "values")[0])
            self.entryusuario.insert(0, self.tabla.item(item, "values")[1])
            self.entrypassword.insert(0, self.tabla.item(item, "values")[2])
        except IndexError:
            pass

    def start_windows(self):
        # TODO funcion para que la aplicacion se incie con windows
        # https://recursospython.com/guias-y-manuales/ejecutar-aplicacion-o-script-al-iniciar-windows/
        # https://recursospython.com/guias-y-manuales/pyqt-icono-area-de-notificaciones-system-tray/
        if self.checkbox_value.get() == 0:
            print('I love Python 0')
        if self.checkbox_value.get() == 1:
            print('I love Python 1')

    def show_selection(self):
        # Muestra el id del registro
        # Esta funcion no forma parte del programa, es solo para prueba
        try:
            # Obtener el ID del primer elemento seleccionado.
            item = self.tabla.selection()[0]
        except IndexError:
            # Si la tupla está vacía, entonces no hay ningún elemento seleccionado.
            messagebox.showwarning(message='Debe seleccionar un elemento.', title='No hay selección')
        else:
            # A partir de este ID retornar el texto del elemento.
            text = self.tabla.item(item, option="text")
            # Mostrarlo en un cuadro de diálogo.
            messagebox.showinfo(message=text, title="Selección")

    def copypass(self):
        # Funcion para copiar el password en una cadena de texto
        passcopy = self.entrypass.get()  # obtiene la cadena de texto
        pc.copy(passcopy)  # copia el password al portapapeles


def main():
    mi_app = Aplicacion()
    return 0


if __name__ == "__main__":
    main()
