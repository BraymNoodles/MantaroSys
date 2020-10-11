
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
#====================================================================================================================================

class Clientes:
    db_name="mantaro2.db"
    def __init__(self, master):
        self.master=master
        self.master.title("Mantaro Sys Clientes")
        self.master.geometry("750x750")
        #tk.Label(self.master, text="Hola").grid(row=0, column=0)
        tabControl=ttk.Notebook(self.master)
        tab1=ttk.Frame(tabControl)
        tabControl.add(tab1, text="Clientes")
        tabControl.pack(expand=1, fill="both")
        #=======================================================
       
        self.frame1=tk.LabelFrame(tab1, text="REGISTRAR CLIENTE", width=30)
        self.frame1.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Codigo Cliente").grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        self.cod_entry=ttk.Entry(self.frame1, width=20)
        self.cod_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Tipo Cliente").grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
        self.cmb_tip=ttk.Combobox(self.frame1, width=20)
        self.cmb_tip['values']=("Persona Juridica", "Persona Natural")
        self.cmb_tip.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame1, text="Razon Cliente").grid(column=0, row=2, padx=5, pady=5, sticky=tk.E)
        self.raz_cliente=ttk.Entry(self.frame1)
        self.raz_cliente.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Nombre Cliente").grid(column=0, row=3, padx=5, pady=5, sticky=tk.E)
        self.nomb_cliente=ttk.Entry(self.frame1)
        self.nomb_cliente.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Apellido Cliente").grid(column=0, row=4, padx=5, pady=5, sticky=tk.E)
        self.apell_cliente=ttk.Entry(self.frame1)
        self.apell_cliente.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Telefono Cliente").grid(column=0, row=5, padx=5, pady=5, sticky=tk.E)
        self.tel_cliente=ttk.Entry(self.frame1)
        self.tel_cliente.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Direccion Cliente").grid(column=0, row=6, padx=5, pady=5, sticky=tk.E)
        self.dir_cliente=ttk.Entry(self.frame1)
        self.dir_cliente.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Email Cliente").grid(column=0, row=7, padx=5, pady=5, sticky=tk.E)
        self.email_cliente=ttk.Entry(self.frame1)
        self.email_cliente.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Button(self.frame1, text="Agregar", command=self._addclientes).grid(row=8, column=1, padx=3, pady=3, sticky=tk.W+tk.E)
      
        #========================================================================================================================
        self.frame2=tk.LabelFrame(tab1, text="CLIENTES", width=30)
        self.frame2.grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        self.data1=ttk.Treeview(self.frame2, height=10, columns=("#1","#2","#3","#4","#5","#6","#7","#8"))
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
        self.data1.heading('#2', text="Tipo", anchor=tk.W)
        self.data1.heading('#3', text="Razón", anchor=tk.W)
        self.data1.heading('#4', text="Nombre", anchor=tk.W)
        self.data1.heading('#5', text="Apellido", anchor=tk.W)
        self.data1.heading('#6', text="Telefono", anchor=tk.W)
        self.data1.heading('#7', text="Direccion", anchor=tk.W)
        self.data1.heading('#8', text="Email", anchor=tk.W)
        ttk.Button(self.frame2, text="Editar", command=self._editcliente).grid(row=2, column=0, padx=5, pady=5, sticky=tk.E+tk.W)
        ttk.Button(self.frame2, text="Eliminar", command=self._deletecliente).grid(row=2, column=1, padx=5, pady=5, sticky=tk.E+tk.W)

        self._getclientes()
    #========================================================================================================================
    def _consultas(self, query, parametros=()):
        inicio=cnx.conexion(self.db_name)
        cursor=inicio.cursor()
        resultado=cursor.execute(query,parametros)
        inicio.commit()
        return resultado

    def _getclientes(self):
        records=self.data1.get_children()
        for record in records:
            self.data1.delete(record)
        query="select * from Cliente"
        db_rows=self._consultas(query)
        for i in db_rows:
            #print(i[1])
            self.data1.insert('', 0, text=i[0],values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))

    def _addclientes(self):
        query='insert into Cliente values(?,?,?,?,?,?,?,?)'
        parametros=(self.cod_entry.get(),self.cmb_tip.get(),self.raz_cliente.get(),self.nomb_cliente.get(),self.apell_cliente.get(), self.tel_cliente.get(), self.dir_cliente.get(), self.email_cliente.get())
        self._consultas(query,parametros)
        msg.showinfo("Mantaro SYS","Proveedor {} se ha registrado".format(self.cod_entry.get()))
        self.cod_entry.delete(0,END)
        self.raz_cliente.delete(0,END)
        self.nomb_cliente.delete(0,END)
        self.apell_cliente.delete(0,END)
        self.tel_cliente.delete(0,END)
        self.dir_cliente.delete(0,END)
        self.email_cliente.delete(0,END)
        self._getclientes()

    def _deletecliente(self):
        try:
            self.data1.item(self.data1.selection())['text'][0]
        except IndexError as e:
            msg.showwarning('Mantaro SYS', 'Por Favor Selecciona Un Registro')
            return
        cod_cliente=self.data1.item(self.data1.selection())['text']
        query="delete from Cliente where IdCliente =?"
        self._consultas(query,(cod_cliente,))
        msg.showinfo('Mantaro SYS', "El Proveedor {} ha sido eliminado".format(cod_cliente))
        self._getclientes()

    def _editcliente(self):
        try:
            self.data1.item(self.data1.selection())['text'][0]
        except IndexError as e:
            msg.showwarning('Mantaro SYS', 'Por Favor Selecciona Un Registro')
            return
        #print(self.data1.item(self.data1.selection())['text'])
        codigocliente=self.data1.item(self.data1.selection())['text']
        self.edit_wind=tk.Toplevel()
        self.edit_wind.title("Editar Cliente")
        self.frame3=ttk.LabelFrame(self.edit_wind,text="Editar Cliente", width=50)
        self.frame3.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame3, text="Tipo Cliente").grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
        cmb_tip=ttk.Combobox(self.frame3, width=20)
        cmb_tip['values']=("Persona Juridica", "Persona Natural")
        cmb_tip.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame3, text="Razon Cliente").grid(column=0, row=2, padx=5, pady=5, sticky=tk.E)
        raz_cliente=ttk.Entry(self.frame3)
        raz_cliente.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame3, text="Nombre Cliente").grid(column=0, row=3, padx=5, pady=5, sticky=tk.E)
        nomb_cliente=ttk.Entry(self.frame3)
        nomb_cliente.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame3, text="Apellido Cliente").grid(column=0, row=4, padx=5, pady=5, sticky=tk.E)
        apell_cliente=ttk.Entry(self.frame3)
        apell_cliente.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame3, text="Telefono Cliente").grid(column=0, row=5, padx=5, pady=5, sticky=tk.E)
        tel_cliente=ttk.Entry(self.frame3)
        tel_cliente.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame3, text="Direccion Cliente").grid(column=0, row=6, padx=5, pady=5, sticky=tk.E)
        dir_cliente=ttk.Entry(self.frame3)
        dir_cliente.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame3, text="Email Cliente").grid(column=0, row=7, padx=5, pady=5, sticky=tk.E)
        email_cliente=ttk.Entry(self.frame3)
        email_cliente.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Button(self.frame3, text="Actualizar", command=lambda:self._editar(codigocliente, cmb_tip.get(),raz_cliente.get(), nomb_cliente.get(), apell_cliente.get(), tel_cliente.get(), dir_cliente.get(), email_cliente.get())).grid(row=8, column=1, padx=3, pady=3, sticky=tk.E+tk.W)

    def _editar(self, cod_cliente, tipo,razon,nombres,apellidos,telefono,direccion,email):
        query='update Cliente set TipCliente=?, RazCliente=?, NombCliente=?, ApelCliente=?, TelCliente=?, DirCliente=?, EmailCliente=? where IdCliente=?'
        parametros=(tipo, razon, nombres,apellidos,telefono,direccion,email,cod_cliente)
        self._consultas(query, parametros)
        self.edit_wind.destroy()
        msg.showinfo("Mantaro SYS", "El cliente con codigo {} ha sido actualizado".format(cod_cliente))
        self._getclientes()

        
      