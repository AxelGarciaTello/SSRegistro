import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import sqlite3
from tkinter.filedialog import asksaveasfilename
import pandas as pd

"""Función para exportar los registros en un CSV"""
def exportar():
    filename = asksaveasfilename(
                    title = "Exportar CSV",
                    defaultextension = ".csv"
               )
    print(filename)
    if filename == ():
        print("Proceso cancelado")
    else:
        """Conexión con la BD"""
        try:
            cnx = sqlite3.connect('CMPL.db')
        except sqlite3.OperationalError as err:
            print(err)
        else:
            """Consulta de registros almacenados en la BD"""
            cursor = cnx.cursor()
            query = ("SELECT * FROM RegistroAulaComputo")
            cursor.execute(query)

            """Escritura de los registros en el archivo seleccionado"""
            f=open(filename,"w")
            f.write("ID,Nombre,Fecha,Hora de entrada,"
                "Hora de salida,Responsable,Actividad que realiza\n"
            )
            for (ID,Nombre,Fecha,Entrada,Salida,Responsable,Actividad) in cursor:
                f.write(str(ID)+","+Nombre+","+str(Fecha)+","+str(Entrada)+","+
                    str(Salida)+","+Responsable+","+Actividad+"\n"
                )

            f.close()
            messagebox.showinfo(
                "Información","El archivo se ha exportado correctamente."
            )
            cursor.close()
            cnx.close()

"""Función para exportar los registros en un archivo Excel"""
def exportarExcel():
    filename = asksaveasfilename(
                    title = "Exportar Excel",
                    defaultextension = ".xlsx"
               )
    print(filename)
    if filename == ():
        print("Proceso cancelado")
    else:
        """Conexión con la BD"""
        try:
            cnx = sqlite3.connect('CMPL.db')
        except sqlite3.OperationalError as err:
            print(err)
        else:
            """Consulta de registros almacenados en la BD"""
            cursor = cnx.cursor()
            query = ("SELECT * FROM RegistroAulaComputo")
            cursor.execute(query)

            listaNombre = []
            listaFecha = []
            listaEntrada = []
            listaSalida = []
            listaResponsable = []
            listaActividad = []
            for (ID,Nombre,Fecha,Entrada,Salida,Responsable,Actividad) in cursor:
                listaNombre.append(Nombre)
                listaFecha.append(Fecha)
                listaEntrada.append(Entrada)
                listaSalida.append(Salida)
                listaResponsable.append(Responsable)
                listaActividad.append(Actividad)

            data = {
                'Nombre' : listaNombre,
                'Fecha' : listaFecha,
                'Hora de entrada' : listaEntrada,
                'Hora de salida' : listaSalida,
                'Responsable' : listaResponsable,
                'Actividad que realiza' : listaActividad
            }
            df = pd.DataFrame(
                    data,
                    columns = ['Nombre','Fecha','Hora de entrada',
                        'Hora de salida','Responsable','Actividad que realiza']
                 )
            df.to_excel(filename,sheet_name='Datos')
            messagebox.showinfo(
                "Información","El archivo se ha exportado correctamente."
            )
            cursor.close()
            cnx.close()

"""Creación de la ventana"""
ventana = tk.Tk()
ventana.title("Registros")
ventana.config(width = 800, height = 500)

"""ventana.columnconfigure(0,weight = 1)"""
ventana.rowconfigure(1,weight = 1)

boton_exportar = ttk.Button(ventana,text = "Exportar CSV",command = exportar)
boton_exportar.grid(row = 0,column = 0,sticky = "nsew")

boton_exportar_excel = ttk.Button(ventana,text = "Exportar Excel", command = exportarExcel)
boton_exportar_excel.grid(row = 0,column = 1,sticky = "nsew")

"""Creación de la tabla con la información"""
dataCols = ("","","","","","","")
tabla = ttk.Treeview(ventana,columns = dataCols, show = 'headings')
tabla.grid(row = 1,column = 0,sticky = "nsew",columnspan = 2)
tabla.heading("#1",text = "ID",anchor = CENTER)
tabla.heading("#2",text = "Nombre",anchor = CENTER)
tabla.heading("#3",text = "Fecha",anchor = CENTER)
tabla.heading("#4",text = "Hora de entrada",anchor = CENTER)
tabla.heading("#5",text = "Hora de Salida",anchor = CENTER)
tabla.heading("#6",text = "Responsable",anchor = CENTER)
tabla.heading("#7",text = "Actividad que realiza",anchor = CENTER)

"""Conculta en la BD para el llenado de la tabla"""
try:
    cnx = sqlite3.connect('CMPL.db')
except sqlite3.OperationalError as err:
    print(err)
else:
    cursor = cnx.cursor()
    query = ("SELECT * FROM RegistroAulaComputo ORDER BY ID DESC")
    cursor.execute(query)
    for registro in cursor:
        tabla.insert('','end',values = registro)

    cursor.close()
    cnx.close()


ventana.mainloop()
