import sqlite3
from sqlite3 import Error
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as msg
import tkcalendar
from tkcalendar import *
import conexion as cnx

#===============================================================================================================================
class Colaboradores:
    db_name="mantaro2.db"
    def __init__(self, master):
        self.master=master
        self.master.title("Gestión de Colaboradores")
        self.master.geometry("400x400")
        tabControl_trabajador=ttk.Notebook(self.master)
        tab1=ttk.Frame(tabControl_trabajador)
        tabControl_trabajador.add(tab1, text="Registrar Colaboradores")
        tabControl_trabajador.pack(expand=1, fill="both")
        #=========================================================================================================================
        
        self.contenedorNuevoRegistro=tk.LabelFrame(tab1, text="Registrar Nuevo Colaborador", width=30)
        self.contenedorNuevoRegistro.grid(row=1,column=1, pady=5, padx=5, sticky=tk.W)
        #agregando labels y entradas
        tk.Label(self.contenedorNuevoRegistro, text="DNI").grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        self.DNI_C=tk.Entry(self.contenedorNuevoRegistro)
        self.DNI_C.grid(row=0, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.contenedorNuevoRegistro, text="Nombres").grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
        self.NOMBRES_C=tk.Entry(self.contenedorNuevoRegistro)
        self.NOMBRES_C.grid(row=1, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.contenedorNuevoRegistro, text="Apellido Paterno").grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)
        self.AppPaterno_C=tk.Entry(self.contenedorNuevoRegistro)
        self.AppPaterno_C.grid(row=2, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.contenedorNuevoRegistro, text="Apellido Materno").grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)
        self.AppMaterno_C=tk.Entry(self.contenedorNuevoRegistro)
        self.AppMaterno_C.grid(row=3, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.contenedorNuevoRegistro, text="Telefono").grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)
        self.Tel_Colab=tk.Entry(self.contenedorNuevoRegistro)
        self.Tel_Colab.grid(row=4, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.contenedorNuevoRegistro, text="Direccion").grid(row=5, column=0, pady=5, padx=5, sticky=tk.W)
        self.Dir_C=tk.Entry(self.contenedorNuevoRegistro)
        self.Dir_C.grid(row=5, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.contenedorNuevoRegistro, text="Email").grid(row=6, column=0, pady=5, padx=5, sticky=tk.W)
        self.Email_C=tk.Entry(self.contenedorNuevoRegistro)
        self.Email_C.grid(row=6, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.contenedorNuevoRegistro, text="Fecha Registro").grid(row=7, column=0, pady=5, padx=5, sticky=tk.W)
        self.FechaRegistro=tkcalendar.DateEntry(self.contenedorNuevoRegistro)
        self.FechaRegistro.grid(row=7, column=1, pady=5, padx=5, sticky=tk.E)
        ttk.Button(self.contenedorNuevoRegistro, text="Agregar", command=self._addcolaboradores).grid(column=1, row=8, sticky=tk.W+tk.E, padx=5, pady=5)
        

        #un frame para visualizar data
        self.visualizar_trabajador=tk.LabelFrame(tab1, text="Datos", width=200)
        self.visualizar_trabajador.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        self.tabla=ttk.Treeview(self.visualizar_trabajador,height=10, columns=('#1','#2','#3','#4','#5','#6','#7', '#8'))
        self.tabla.grid(row=0, column=0, columnspan=2)
        self.tabla.column('#1', width=90, minwidth=50)
        self.tabla.column('#2', width=150, minwidth=50)
        self.tabla.column('#3', width=150, minwidth=50)
        self.tabla.column('#4', width=150, minwidth=50)
        self.tabla.column('#5', width=90, minwidth=50)
        self.tabla.column('#6', width=150, minwidth=50)
        self.tabla.column('#7', width=150, minwidth=50)
        self.tabla.column('#8', width=120, minwidth=80)
        self.tabla['show']='headings'
        self.tabla.heading('#1', text="DNI", anchor=tk.CENTER)
        self.tabla.heading('#2', text="Nombres", anchor=tk.W)
        self.tabla.heading('#3', text="Apellido Paterno", anchor=tk.W)
        self.tabla.heading('#4', text="Apellido Materno", anchor=tk.W)
        self.tabla.heading('#5', text="Contacto", anchor=tk.W)
        self.tabla.heading('#6', text="Direccion", anchor=tk.CENTER)
        self.tabla.heading('#7', text="Email", anchor=tk.W)
        self.tabla.heading('#8', text="Fecha Registro", anchor=tk.W)
        ttk.Button(self.visualizar_trabajador, text="Editar", command=self._editcolaboradores).grid(row=1, column=0, padx=2, pady=2, sticky=tk.W+tk.E)
        ttk.Button(self.visualizar_trabajador, text="Eliminar", command=self._deletecolaboradores).grid(row=1, column=1, padx=2, pady=2, sticky=tk.W+tk.E)

        self._getColab()
#==============================================================================================================================
    def _consultas(self, query, parametros=()):
        inicio=cnx.conexion(self.db_name)
        cursor=inicio.cursor()
        resultado=cursor.execute(query,parametros)
        inicio.commit()
        return resultado

    def _getColab(self):
        records=self.tabla.get_children()
        for record in records:
            self.tabla.delete(record)
        query="select * from Colaboradores"
        db_rows=self._consultas(query)
        for i in db_rows:
            self.tabla.insert('', 0, text=i[0],values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))

    def _addcolaboradores(self):
        query='insert into Colaboradores values(?,?,?,?,?,?,?,?)'
        parametros=(self.DNI_C.get(), self.NOMBRES_C.get(), self.AppPaterno_C.get(), self.AppMaterno_C.get(), self.Tel_Colab.get(), self.Dir_C.get(),self.Email_C.get(),self.FechaRegistro.get_date())
        self._consultas(query, parametros)
        msg.showinfo("Mantaro SYS","El colaborador {} se ha registrado".format(self.DNI_C.get()))
        self.DNI_C.delete(0,END)
        self.NOMBRES_C.delete(0,END)
        self.AppPaterno_C.delete(0,END)
        self.AppMaterno_C.delete(0,END)
        self.Tel_Colab.delete(0,END)
        self.Dir_C.delete(0,END)
        self.Email_C.delete(0,END)
        self._getColab()

 
    def _deletecolaboradores(self):
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            msg.showwarning('Mantaro SYS', 'Por Favor Selecciona Un Registro')
            return
        cod_colab=self.tabla.item(self.tabla.selection())['text']
        query="delete from Colaboradores where IdColaborador =?"
        self._consultas(query,(cod_colab,))
        msg.showinfo('Mantaro SYS', "El Proveedor {} ha sido eliminado".format(cod_colab))
        self._getColab()

    def _editcolaboradores(self):
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            msg.showwarning('Mantaro SYS', 'Por Favor Selecciona Un Registro')
            return
        CodigoColab=self.tabla.item(self.tabla.selection())['text']
        self.edit_wind=tk.Toplevel()
        self.edit_wind.title("Editar Colaborador")
        self.frame1=ttk.LabelFrame(self.edit_wind,text="Editar Colaborador", width=50)
        self.frame1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Nombres").grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
        NOMBRES_C=tk.Entry(self.frame1)
        NOMBRES_C.grid(row=1, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.frame1, text="Apellido Paterno").grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)
        AppPaterno_C=tk.Entry(self.frame1)
        AppPaterno_C.grid(row=2, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.frame1, text="Apellido Materno").grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)
        AppMaterno_C=tk.Entry(self.frame1)
        AppMaterno_C.grid(row=3, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.frame1, text="Telefono").grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)
        Tel_Colab=tk.Entry(self.frame1)
        Tel_Colab.grid(row=4, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.frame1, text="Direccion").grid(row=5, column=0, pady=5, padx=5, sticky=tk.W)
        Dir_C=tk.Entry(self.frame1)
        Dir_C.grid(row=5, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.frame1, text="Email").grid(row=6, column=0, pady=5, padx=5, sticky=tk.W)
        Email_C=tk.Entry(self.frame1)
        Email_C.grid(row=6, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.frame1, text="Fecha Registro").grid(row=7, column=0, pady=5, padx=5, sticky=tk.W)
        FechaRegistro=tkcalendar.DateEntry(self.frame1)
        FechaRegistro.grid(row=7, column=1, pady=5, padx=5, sticky=tk.E)
        ttk.Button(self.frame1, text="Actualizar", command=lambda:self.editar(CodigoColab, NOMBRES_C.get(), AppPaterno_C.get(), AppMaterno_C.get(), Tel_Colab.get(), Dir_C.get(), Email_C.get(), FechaRegistro.get_date())).grid(row=8, column=1, sticky=tk.E+tk.W)


    def editar(self, id_colab, nombres, ap_pat, ap_mat, tel, dire, email, fecha):
        query="update Colaboradores set NombColaborador=?, ApePatColab=?, ApeMatColab=?, NroColab=?, DirColab=?, EmailColab=?, FechaRegistro=? where IdColaborador=?"
        parametros=(nombres, ap_pat, ap_mat, tel, dire, email, fecha, id_colab)
        self._consultas(query, parametros)
        self.edit_wind.destroy()
        msg.showinfo("Mantaro SYS", "El colaborador {} ha sido actualizado".format(id_colab))
        self._getColab()
