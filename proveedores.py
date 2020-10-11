#===========IMPORTAR PAQUETES=============
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
#===========================================================================
class Proveedores:
    db_name="mantaro2.db"
    
    def __init__(self, master):
        self.master=master
        self.master.title("Mantaro Sys Proveedores")
        self.master.geometry("400x400")
        #agregar tabs de registro y ver proveedores
        tabcontrol_proveedor=ttk.Notebook(self.master)
        ventana1=ttk.Frame(tabcontrol_proveedor)
        tabcontrol_proveedor.add(ventana1, text="Ver Proveedores")
        ventana2=ttk.Frame(tabcontrol_proveedor)
        tabcontrol_proveedor.add(ventana2, text="Registrar Proveedor")
        tabcontrol_proveedor.pack(expand=1, fill="both")
        #rellenar ventana Ver Proveedores y Registrar Nuevo
        self.frame1=ttk.Labelframe(ventana1, text="Consulta Proveedores", width=30)
        self.frame1.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        self.data1=ttk.Treeview(self.frame1, height=10, columns=("#1","#2","#3","#4","#5","#6","#7","#8"))
        self.data1.grid(row=0, column=0, columnspan=2)
        self.data1.column("#1", width=85, minwidth=20)
        self.data1.column("#2", width=120, minwidth=20)
        self.data1.column("#3", width=130, minwidth=20)
        self.data1.column("#4", width=130, minwidth=20)
        self.data1.column("#5", width=130, minwidth=20)
        self.data1.column("#6", width=100, minwidth=20)
        self.data1.column("#7", width=130, minwidth=20)
        self.data1.column("#8", width=120, minwidth=20)
        self.data1['show']='headings'
        self.data1.heading('#1', text="Código", anchor=tk.W)
        self.data1.heading('#2', text="Tipo Proveedor", anchor=tk.W)
        self.data1.heading('#3', text="Razón", anchor=tk.W)
        self.data1.heading('#4', text="Nombre", anchor=tk.W)
        self.data1.heading('#5', text="Apellido", anchor=tk.W)
        self.data1.heading('#6', text="Telefono", anchor=tk.W)
        self.data1.heading('#7', text="Direccion", anchor=tk.W)
        self.data1.heading('#8', text="Email", anchor=tk.W)
        ttk.Button(self.frame1, text="Editar", command=self._editprov).grid(row=2, column=0, padx=5, pady=5, sticky=tk.E+tk.W)
        ttk.Button(self.frame1, text="Eliminar", command=self._eliprov).grid(row=2, column=1, padx=5, pady=5, sticky=tk.E+tk.W)
        self._getprov()
        self.frame2=ttk.Labelframe(ventana2, text="Registrar Proveedores", width=30)
        self.frame2.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame2, text="Código Proveedor").grid(row=0, column=0, pady=5, padx=5, sticky=tk.E)
        self.cod_entry=ttk.Entry(self.frame2)
        self.cod_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame2, text="Tipo Proveedor").grid(row=1, column=0, pady=5, padx=5, sticky=tk.E)
        self.cmb_tip=ttk.Combobox(self.frame2, width=20)
        self.cmb_tip['values']=("Persona Juridica", "Persona Natural")
        self.cmb_tip.grid(row=1, column=1, pady=5, padx=5, sticky=tk.E)
        tk.Label(self.frame2, text="Razón Social").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.raz=ttk.Entry(self.frame2)
        self.raz.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame2, text="Nombres").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.nombres=ttk.Entry(self.frame2)
        self.nombres.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame2, text="Apellidos").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.apel=ttk.Entry(self.frame2)
        self.apel.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame2, text="Nro Telefonico").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.nro=ttk.Entry(self.frame2)
        self.nro.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame2, text="Direccion").grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.dir=ttk.Entry(self.frame2)
        self.dir.grid(row=6, column=1, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame2, text="Email").grid(row=7, column=0, pady=5, padx=5, sticky=tk.E)
        self.email=ttk.Entry(self.frame2)
        self.email.grid(row=7, column=1, pady=5, padx=5, sticky=tk.W)
        ttk.Button(self.frame2, text="Registrar", command=self._addprov).grid(row=8, column=0, pady=3, padx=3, sticky=tk.W)
        ttk.Button(self.frame2, text="Actualizar", command=self._getprov).grid(row=8, column=1, pady=3, padx=3, sticky=tk.E)
        
    def _consulta2(self, query, parametros=()):
        inicio=cnx.conexion(self.db_name)
        cursor=inicio.cursor()
        resultado=cursor.execute(query,parametros)
        inicio.commit()
        return resultado    

    def _getprov(self):
        records=self.data1.get_children()
        for record in records:
            self.data1.delete(record)
        query="select * from Proveedor"
        db_rows=self._consulta2(query)
        for i in db_rows:            
            self.data1.insert('', 0, text=i[0],values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))

    def _addprov(self):
        query='insert into Proveedor values(?,?,?,?,?,?,?,?)'
        parametros=(self.cod_entry.get(),self.cmb_tip.get(),self.raz.get(),self.nombres.get(),self.apel.get(), self.nro.get(), self.dir.get(), self.email.get())
        self._consulta2(query,parametros)
        msg.showinfo("Mantaro SYS","Proveedor {} se ha registrado".format(self.raz.get()))
        self.cod_entry.delete(0,END)
        self.raz.delete(0,END)
        self.nombres.delete(0,END)
        self.apel.delete(0,END)
        self.nro.delete(0,END)
        self.dir.delete(0,END)
        self.email.delete(0,END)
        self._getprov()

    def _eliprov(self):        
        try:
            self.data1.item(self.data1.selection())['text'][0]
        except IndexError as e:
            msg.showwarning('Mantaro SYS', 'Por Favor Selecciona Un Registro')
            return
        cod_prov=self.data1.item(self.data1.selection())['text']
        query="delete from Proveedor where IdProv =?"
        self._consulta2(query,(cod_prov,))
        msg.showinfo('Mantaro SYS', "El Proveedor {} ha sido eliminado".format(cod_prov))
        self._getprov()
        
    def _editprov(self):
        try:
            self.data1.item(self.data1.selection())['text'][0]
        except IndexError as e:
            msg.showwarning('Mantaro SYS', 'Por Favor Selecciona Un Registro')
            return
        codigo=self.data1.item(self.data1.selection())['text']
        tipo_prov=self.data1.item(self.data1.selection())['values'][1]
        razon_prov=self.data1.item(self.data1.selection())['values'][2]
        nom_prov=self.data1.item(self.data1.selection())['values'][3]
        apel_prov=self.data1.item(self.data1.selection())['values'][4]
        nro_prov=self.data1.item(self.data1.selection())['values'][5]
        dir_prov=self.data1.item(self.data1.selection())['values'][6]
        email_prov=self.data1.item(self.data1.selection())['values'][7]
        self.edit_wind=tk.Toplevel()
        self.edit_wind.title("Editar Proveedor")
        self.frame3=ttk.LabelFrame(self.edit_wind,text="Editar Proveedor", width=50)
        self.frame3.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame3, text='Tipo Proveedor: ').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Entry(self.frame3, textvariable=StringVar(self.frame3, value=(tipo_prov)), state='readonly').grid(row=0, column=1, sticky=tk.W)
        tk.Label(self.frame3, text="Nuevo Tipo Proveedor: ").grid(row=1, column=0, padx=5,pady=5, sticky=tk.W)
        cmb_nuevo_tipo_proveedor=ttk.Combobox(self.frame3, width=20)
        cmb_nuevo_tipo_proveedor['values']=("Persona Juridica", "Persona Natural")
        cmb_nuevo_tipo_proveedor.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W )
        tk.Label(self.frame3, text="Razon Proveedor: ").grid(row=2, column=0, pady=5, padx=5, sticky=tk.E)
        tk.Entry(self.frame3, textvariable=StringVar(self.frame3, value=(razon_prov)), state='readonly').grid(row=2, column=1, sticky=tk.W)
        tk.Label(self.frame3, text="Nueva Razon Proveedor: ").grid(row=3, column=0, pady=5, padx=5, sticky=tk.E)
        nueva_razon=ttk.Entry(self.frame3)
        nueva_razon.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame3, text="Nombre Proveedor: ").grid(row=4, column=0, pady=5, padx=5, sticky=tk.E)
        tk.Entry(self.frame3, textvariable=StringVar(self.frame3, value=(nom_prov)), state='readonly').grid(row=4, column=1, sticky=tk.W)
        tk.Label(self.frame3, text="Nuevo Nombre Proveedor: ").grid(row=5, column=0, pady=5, padx=5, sticky=tk.E)
        nuevo_nombre=ttk.Entry(self.frame3)
        nuevo_nombre.grid(row=5, column=1, sticky=tk.W)
        tk.Label(self.frame3, text="Apellido Proveedor: ").grid(row=6, column=0, pady=5, padx=5, sticky=tk.E)
        tk.Entry(self.frame3, textvariable=StringVar(self.frame3, value=(apel_prov)), state='readonly').grid(row=6, column=1, sticky=tk.W)
        tk.Label(self.frame3, text="Nuevo Apellido Proveedor: ").grid(row=7, column=0, pady=5, padx=5, sticky=tk.E)
        nuevo_apellido=ttk.Entry(self.frame3)
        nuevo_apellido.grid(row=7, column=1, sticky=tk.W)
        tk.Label(self.frame3, text="Nro Proveedor: ").grid(row=8, column=0, pady=5, padx=5, sticky=tk.E)
        tk.Entry(self.frame3, textvariable=StringVar(self.frame3, value=(nro_prov)), state='readonly').grid(row=8, column=1, sticky=tk.W)
        tk.Label(self.frame3, text="Nuevo Nro Proveedor: ").grid(row=9, column=0, pady=5, padx=5, sticky=tk.E)
        nuevo_nro=ttk.Entry(self.frame3)
        nuevo_nro.grid(column=1, row=9, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame3, text="Direccion Proveedor: ").grid(row=10, column=0, pady=5, padx=5, sticky=tk.E)
        tk.Entry(self.frame3, textvariable=StringVar(self.frame3, value=(dir_prov)), state='readonly').grid(row=10, column=1, sticky=tk.W)
        tk.Label(self.frame3, text="Nueva Direccion Proveedor: ").grid(row=11, column=0, pady=5, padx=5, sticky=tk.E)
        nueva_dir=ttk.Entry(self.frame3)
        nueva_dir.grid(column=1, row=11, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame3, text="Email Proveedor: ").grid(row=12, column=0, pady=5, padx=5, sticky=tk.E)
        tk.Entry(self.frame3, textvariable=StringVar(self.frame3, value=(email_prov)), state='readonly').grid(row=12, column=1, sticky=tk.W)
        tk.Label(self.frame3, text="Nuevo Email Proveedor: ").grid(row=13, column=0, pady=5, padx=5, sticky=tk.E)
        nuevo_email=ttk.Entry(self.frame3)
        nuevo_email.grid(column=1, row=13, pady=5, padx=5, sticky=tk.W)
        ttk.Button(self.frame3, text="Editar", command=lambda:self._edidatos(razon_prov,cmb_nuevo_tipo_proveedor.get(),nueva_razon.get(),nuevo_nombre.get(),nuevo_apellido.get(),nuevo_nro.get(),nueva_dir.get(),nuevo_email.get())).grid(row=14, column=1, pady=3, padx=3, sticky=tk.E+tk.W)

    def _edidatos(self, razon_prov, nuevo_tipo_proveedor, nueva_razon,nuevo_nombre,nuevo_apellido,nuevo_nro,nueva_dir,nuevo_email):
        query="update Proveedor set TipProv=?, RazonProv=?, NombProv=?, ApellProv=?, TelProv=?, DirProv=?, EmailProv=? where RazonProv=?"
        parametros=(nuevo_tipo_proveedor,nueva_razon,nuevo_nombre,nuevo_apellido,nuevo_nro,nueva_dir,nuevo_email, razon_prov)
        self._consulta2(query, parametros)
        self.edit_wind.destroy()
        msg.showinfo('Mantaro SYS', 'El Proveedor {} se actualizo'.format(razon_prov))
        self._getprov()