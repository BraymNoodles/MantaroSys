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
class Roles:
    db_name="mantaro2.db"
    def __init__(self, master):
        self.master=master
        self.master.title("Herramienta Rol")
        tabControl1=ttk.Notebook(self.master)
        tab1=ttk.Frame(tabControl1)
        tabControl1.add(tab1, text="Configuración Roles")
        tabControl1.pack(expand=1, fill="both")

        self.frame1=tk.LabelFrame(tab1, text="Registrar Roles", width=30)
        self.frame1.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame1, text="Codigo Rol").grid(row=0, column=0, padx=3, pady=3, sticky=tk.E)
        self.cod_Rol=ttk.Entry(self.frame1)
        self.cod_Rol.grid(row=0, column=1, pady=3, padx=3, sticky=tk.W)
        tk.Label(self.frame1, text="Nombre Rol").grid(row=1, column=0, padx=3, pady=3, sticky=tk.E)
        self.nomb_rol=ttk.Entry(self.frame1)
        self.nomb_rol.grid(row=1, column=1, pady=3, padx=3, sticky=tk.W)
        tk.Label(self.frame1, text="Descripcion Rol ").grid(row=2, column=0, padx=3, pady=3, sticky=tk.E)
        self.scrolled1=scrolledtext.ScrolledText(self.frame1, width=30, height=10, wrap=tk.WORD)
        self.scrolled1.grid(row=2, column=1, pady=3, padx=3, sticky=tk.W)
        ttk.Button(self.frame1, text="Agregar", command=self._insertRol).grid(row=3, column=1, pady=3, padx=3, sticky=tk.W+tk.E)

        self.frame2=tk.LabelFrame(tab1, text="Roles Registrados", width=30)
        self.frame2.grid(row=1, column=2, pady=5, padx=5, sticky=tk.E)
        self.tabla1=ttk.Treeview(self.frame2, height=10,column=('#1', '#2', '#3'))
        self.tabla1.grid(row=1, column=1, columnspan=2)
        self.tabla1.column('#1', width=100, minwidth=90)
        self.tabla1.column('#2', width=100, minwidth=90)
        self.tabla1.column('#3', width=300, minwidth=90)
        self.tabla1['show']='headings'
        self.tabla1.heading('#1', text="Id Rol", anchor=tk.W)
        self.tabla1.heading('#2', text="Nombre Rol", anchor=tk.CENTER)
        self.tabla1.heading('#3', text="Descripcion Rol", anchor=tk.W)
        ttk.Button(self.frame2, text="Editar", command=self._editRol).grid(row=2, column=1, padx=3, pady=3, sticky=tk.W+tk.E)
        ttk.Button(self.frame2, text="Eliminar", command=self._deleteRol).grid(row=2, column=2, padx=3, pady=3, sticky=tk.W+tk.E)

        self._getRol2()

#===================================================================================================================================

    def _consultas(self, query, parametros=()):
        inicio=cnx.conexion(self.db_name)
        cursor=inicio.cursor()
        resultado=cursor.execute(query,parametros)
        inicio.commit()
        return resultado   

    
    
    def _getRol2(self):
        records=self.tabla1.get_children()
        for record in records:
            self.tabla1.delete(record)
        query="select * from Roles"
        db_rows=self._consultas(query)
        for row in db_rows:
            self.tabla1.insert('',0,text=row[0],values=(row[0],row[1],row[2]))
        


    def _insertRol(self):
        query="insert into Roles values(?,?,?)"
        parametros=(self.cod_Rol.get(),self.nomb_rol.get(), self.scrolled1.get('1.0', 'end-1c'))
        self._consultas(query, parametros)
        msg.showinfo("Mantaro SYS","El rol {} ha sido registrado".format(self.nomb_rol.get()))
        self.cod_Rol.delete(0, END)
        self.nomb_rol.delete(0,END)
        self._getRol2()

    def _deleteRol(self):
        try:
            self.tabla1.item(self.tabla1.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro SYS", "Por favor seleccione un item")
            return
        codRol=self.tabla1.item(self.tabla1.selection())['text']
        nomrol=self.tabla1.item(self.tabla1.selection())['values'][1]
        query="delete from Roles where IdRol=?"
        self._consultas(query,(codRol, ))
        msg.showinfo("Mantaro SYS", "El rol {} ha sido eliminado".format(nomrol))
        self._getRol2()

    def _editRol(self):
        try:
            self.tabla1.item(self.tabla1.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro SYS", "Por favor seleccione un item")
            return
        codRol=self.tabla1.item(self.tabla1.selection())['text']
        self.edit_wind1=tk.Toplevel()
        self.edit_wind1.title("Editar el Rol")
        self.frameEdicion=tk.LabelFrame(self.edit_wind1, text="Editar Rol", width=100)
        self.frameEdicion.grid(row=0, column=0, padx=3, pady=3, sticky=tk.W)
        tk.Label(self.frameEdicion, text="Nombre Rol").grid(row=1, column=0, padx=3, pady=3, sticky=tk.E)
        nomb_rol=ttk.Entry(self.frameEdicion)
        nomb_rol.grid(row=1, column=1, pady=3, padx=3, sticky=tk.W)
        tk.Label(self.frameEdicion, text="Descripcion Rol ").grid(row=2, column=0, padx=3, pady=3, sticky=tk.E)
        scrolled1=scrolledtext.ScrolledText(self.frameEdicion, width=30, height=10, wrap=tk.WORD)
        scrolled1.grid(row=2, column=1, pady=3, padx=3, sticky=tk.W)
        ttk.Button(self.frameEdicion, text="Actualizar", command=lambda: self._edicion(codRol, nomb_rol.get(), scrolled1.get('1.0', 'end-1c'))).grid(row=3, column=1, sticky=tk.E+tk.W)

    def _edicion(self, codigo, nombre, descripcion):
        query="update Roles set NombRol=?, DescRol=? where IdRol=?"
        parametros=(nombre, descripcion, codigo)
        self._consultas(query, parametros)
        msg.showinfo("Mantaro SYS", "El Rol {} ha sido actualizado".format(codigo))
        self.edit_wind1.destroy()
        self._getRol2()
        


       



class Usuarios:
    db_name="mantaro2.db"
    def __init__(self, master):
        self.master=master
        self.master.title("Configuracion Usuarios")
        
        tabControl1=ttk.Notebook(self.master)
        tab1=ttk.Frame(tabControl1)
        tabControl1.add(tab1, text="Configuración Usuarios")
        tabControl1.pack(expan=1, fill="both")

        self.frame1=ttk.Labelframe(tab1, text="Registro de Usuarios", width=30)
        self.frame1.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        tk.Label(self.frame1, text="Id Usuario").grid(row=0, column=0, pady=3, padx=3, sticky=tk.E)
        self.cmb1=ttk.Combobox(self.frame1, width=25)
        
        self.cmb1.grid(row=0, column=1, padx=3, pady=3, sticky=tk.W)
        tk.Label(self.frame1, text="Id Rol").grid(row=1, column=0, pady=3, padx=3, sticky=tk.E)
        self.cmb2=ttk.Combobox(self.frame1, width=25)
        
        self.cmb2.grid(row=1, column=1, padx=3, pady=3, sticky=tk.W)
        tk.Label(self.frame1, text="Password").grid(row=2, column=0, pady=3, padx=3, sticky=tk.E) 
        self.Password=tk.Entry(self.frame1, show="*", width=15)
        self.Password.grid(row=2, column=1, pady=3, padx=3, sticky=tk.W)
        ttk.Button(self.frame1, text="Registrar", command=self._registrarT).grid(row=3, column=1, padx=2, pady=2, sticky=tk.W+tk.E)

        self._carga2()
        self._carga1()

#===================================================================================================================================

    def _consultas(self, query, parametros=()):
        inicio=cnx.conexion(self.db_name)
        cursor=inicio.cursor()
        resultado=cursor.execute(query,parametros)
        inicio.commit()
        return resultado   

    def _carga1(self):
        listaR=list()
        query="select IdRol from Roles"
        rows=self._consultas(query)
        for row in rows:
            listaR.append(row[0])
        self.cmb2['values']=listaR

    def _carga2(self):
        listaT=list()
        query="select IdColaborador from Colaboradores"
        rows=self._consultas(query)
        for row in rows:
            listaT.append(row[0])
        self.cmb1['values']=listaT
        

    def _registrarT(self):
        query="insert into Usuarios values(?,?,?)"
        parametros=(self.cmb1.get(), self.cmb2.get(), self.Password.get())
        self._consultas(query,parametros)
        msg.showinfo("Mantaro SYS", "Se registro al usuario {}".format(self.cmb1.get()))
        self.Password.delete(0, END)
        




