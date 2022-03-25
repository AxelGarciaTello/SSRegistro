import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import date
from datetime import datetime
import sqlite3

"""Función para el regitro de salida"""
def registrarSalida(ventana2):
    """Conexión con la BD"""
    try:
        cnx = sqlite3.connect('CMPL.db')
    except sqlite3.OperationalError as err:
        print(err)
    else:

        """Obtención del último registro"""
        cursor = cnx.cursor()

        query = ("SELECT ID FROM RegistroAulaComputo ORDER BY ID DESC LIMIT 1")

        cursor.execute(query)

        """Edición del último registro con la hora de salida"""
        for (ID,) in cursor:
            sentencia = (
                            "UPDATE RegistroAulaComputo "
                            "SET HoraSalida=? WHERE ID=?"
                        )
            now = datetime.now()
            hora = str(now.hour)+":"+str(now.minute)
            informacion = (hora, ID)

            cursor.execute(sentencia,informacion)
            cnx.commit()

        cursor.close()
        cnx.close()
        ventana2.destroy()

"""Función para mostrar la ventana de registro de salida"""
def mostrarVentanaSalida():
    ventana2 = tk.Tk()
    ventana2.title("Registro de Salida")
    ventana2.geometry('225x75+0+0')
    ventana2['bg']='#A0F572'

    boton_salida = tk.Button(
                        ventana2,
                        text = "Registrar salida",
                        font = ("Arial",12),
                        bg = "#72F5B2",
                        width = 22,
                        command = lambda: registrarSalida(ventana2)
                   )
    boton_salida.grid(row = 0,column = 0,pady = 20)

    ventana2.mainloop()

"""Registro de la información en la BD"""
def registrar():
    """Verificación del llenado de datos"""
    nombre = caja_nombre.get()
    fecha = caja_fecha.get()
    entrada = caja_entrada.get()
    responsable = caja_responsable.get()
    actividad = caja_actividad.get()

    if (nombre == "" or
        fecha == "" or
        entrada == "" or
        actividad == ""):
        print("Error: faltan datos por llenar")
    else:
        """Conexión con la BD"""
        try:
            cnx = sqlite3.connect('CMPL.db')
        except sqlite3.OperationalError as err:
            print(err)
        else:
            """Registro de los datos"""
            cursor = cnx.cursor()

            sentencia=(
                            "INSERT INTO RegistroAulaComputo("
                            "Nombre,Fecha,HoraEntrada,"
                            "HoraSalida,Responsable,Actividad)"
                            "VALUES(?,?,?,NULL,?,?)"
                      )
            informacion = (nombre,fecha,entrada,responsable,actividad,)
            cursor.execute(sentencia,informacion)
            cnx.commit()

            cursor.close()
            cnx.close()
            ventana.destroy()
            mostrarVentanaSalida()

"""Construcción de la ventana principal"""
ventana = tk.Tk()
ventana.title("Regitro")
ventana.attributes('-fullscreen',True)
ventana['bg'] = '#A0F572'

"""Tamaños dinamicos para la cuadricula de objetos"""
ventana.columnconfigure(0,weight=1)
ventana.columnconfigure(1,weight=1)
ventana.columnconfigure(2,weight=1)
ventana.columnconfigure(3,weight=1)
ventana.rowconfigure(1,weight=1)
ventana.rowconfigure(2,weight=1)
ventana.rowconfigure(3,weight=1)
ventana.rowconfigure(4,weight=1)
ventana.rowconfigure(5,weight=1)
ventana.rowconfigure(6,weight=1)

etiqueta_informacion = tk.Label(
    text = "Reglamento del Aula de Cómputo\n\n\n"
"1. Registrar la salida y apagar el equipo al momento de desocuparlo.\n\n"
"2. El usuario es responsable del equipo que se le haya asignado, por lo que se"
" recomienda verificar las condiciones en que lo recibe y reportar a los "
"auxiliares de laboratorio cualquier anomalía que detecte.\n\n"
"3. No introducir ninguna clase de alimentos o bebidas.\n\n"
"4. El empleo del equipo es exclusivamente para uso académico.\n\n",
    wraplength = 500,
    font = ("Arial",20),
    bg = "#A0F572"
)
etiqueta_informacion.grid(
    row = 1,
    column = 0,
    columnspan = 2,
    rowspan = 6,
)

etiqueta_titulo = tk.Label(
                    text="Registro",
                    font=("Arial",30,"bold"),
                    bg="#A0F572"
                  )
etiqueta_titulo.grid(row = 0,column = 0,columnspan = 4)

etiqueta_nombre = tk.Label(text = "Nombre",font = ("Arial",20),bg = "#A0F572")
etiqueta_nombre.grid(row = 1,column = 2)

etiqueta_fecha = tk.Label(text = "Fecha",font = ("Arial",20),bg = "#A0F572")
etiqueta_fecha.grid(row = 2,column = 2)

etiqueta_entrada = tk.Label(
                        text = "Horario de entrada",
                        font = ("Arial",20),
                        bg = "#A0F572"
                   )
etiqueta_entrada.grid(row = 3,column = 2)

etiqueta_responsable = tk.Label(
                            text = "Responsable",
                            font = ("Arial",20),
                            bg = "#A0F572"
                       )
etiqueta_responsable.grid(row = 4,column = 2)

etiqueta_actividad = tk.Label(
                        text = "Actividad que realiza",
                        font = ("Arial",20),
                        bg = "#A0F572"
                     )
etiqueta_actividad.grid(row = 5,column = 2)

boton_registrar = tk.Button(
                        text = "Registrar",
                        width = 50,
                        command = registrar,
                        font = ("Arial",20),
                        bg = "#72F5B2"
                  )
boton_registrar.grid(row = 6,column = 2,columnspan = 2,sticky="ew")

caja_nombre = ttk.Entry(font = ("Arial",20))
caja_nombre.grid(row = 1,column = 3)

today = date.today()
entrada_fecha = tk.StringVar()
caja_fecha = ttk.Entry(font = ("Arial",20),textvariable = entrada_fecha)
entrada_fecha.set(today)
caja_fecha.grid(row = 2,column = 3)

now = datetime.now()
hora = str(now.hour)+":"+str(now.minute)
entrada_entrada = tk.StringVar()
caja_entrada = ttk.Entry(font = ("Arial",20),textvariable = entrada_entrada)
entrada_entrada.set(hora)
caja_entrada.grid(row = 3,column = 3)

caja_responsable = ttk.Entry(font = ("Arial",20))
caja_responsable.grid(row = 4,column = 3)

caja_actividad = ttk.Entry(font = ("Arial",20))
caja_actividad.grid(row = 5,column = 3)

ventana.mainloop()
