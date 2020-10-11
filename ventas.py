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
import random
import string
import movimientos
from movimientos import Movimiento
import excel_venta
from excel_venta import DetalleVenta
#===========================================================================

class Ventas:
    db_name="mantaro2.db"
    def __init__(self, master):
        self.master=master
        self.master.title("Mantaro SYS")
        self.master.geometry("400x400")
        pestañas=ttk.Notebook(self.master)
        tab1=ttk.Frame(pestañas)
        tab2=ttk.Frame(pestañas)
        pestañas.add(tab1, text="Ventas")
        pestañas.add(tab2, text="Registro de Documentos")
        pestañas.pack(expan=1, fill="both")
#======================================================================================
        self.frame1=ttk.Labelframe(tab1, text="Registro de Ventas", width=100)
        self.frame1.grid(row=1, column=1, padx=3, pady=3, sticky=tk.NW)
        tk.Label(self.frame1, text="Nro Recibo").grid(row=1, column=1, padx=3, pady=3)
        self.NroRecibo=ttk.Entry(self.frame1, width=20)
        self.NroRecibo.grid(row=1, column=2, padx=3, pady=3)
        tk.Label(self.frame1, text="Recibo").grid(row=1, column=3, padx=3, pady=3)
        self.cmbTipoDoc=ttk.Combobox(self.frame1, width=20)
        self.cmbTipoDoc['values']=("Factura", "Boleta")
        self.cmbTipoDoc.grid(row=1, column=4, padx=3, pady=3)
        tk.Label(self.frame1, text="Usuario").grid(row=2, column=1, padx=3, pady=3)
        self.cmbIdUsuario=ttk.Combobox(self.frame1, width=25)
        self.cmbIdUsuario.grid(row=2, column=2, padx=3, pady=3)
        tk.Label(self.frame1, text="Cliente").grid(row=2, column=3, padx=3, pady=3)
        self.IdCliente=ttk.Entry(self.frame1)
        self.IdCliente.grid(row=2, column=4, padx=3, pady=3)
        tk.Label(self.frame1, text="Fecha de Venta").grid(row=3, column=1, padx=3, pady=3)
        self.FechaVenta=tkcalendar.DateEntry(self.frame1)
        self.FechaVenta.grid(row=3, column=2, padx=3, pady=3, sticky=tk.W)
        tk.Label(self.frame1, text="Codigo Venta").grid(row=3, column=3, padx=3, pady=3, sticky=tk.W)
        self.varCodigo=StringVar()
        self.CodVenta=ttk.Entry(self.frame1, textvariable=self.varCodigo, width=15, state='disabled')
        self.CodVenta.grid(row=3, column=4, padx=3, pady=3, sticky=tk.W)
        ttk.Button(self.frame1, text="Generar Codigo", command=self._generarcod).grid(row=4, column=4, padx=3, pady=3, sticky=tk.W) 
     
        self.frame3=ttk.Labelframe(tab1, text="Productos", width=80)
        self.frame3.grid(row=2, column=1, padx=3, pady=3, sticky=tk.NW)
        tk.Label(self.frame3, text="Codigo Producto").grid(row=0, column=0, padx=3, pady=3, sticky=tk.W)
        self.codProducto=ttk.Combobox(self.frame3, width=25)
        self.codProducto.grid(row=0, column=1)
        tk.Label(self.frame3, text="Nombre Producto").grid(row=1, column=0, padx=3, pady=3, sticky=tk.W)
        self.nombProducto=ttk.Entry(self.frame3)
        self.nombProducto.grid(row=1, column=1)
        tk.Label(self.frame3, text="Cantidad").grid(row=2, column=0, padx=3, pady=3, sticky=tk.W)
        self.spin_variable=DoubleVar()
        self.spin=ttk.Spinbox(self.frame3, from_=0, to=20, width=5, textvariable=self.spin_variable)
        self.spin.grid(row=2, column=1)
        tk.Label(self.frame3, text="Precio").grid(row=3, column=0, padx=3, pady=3, sticky=tk.W)
        self.precio=DoubleVar()
        self.precioProducto=ttk.Entry(self.frame3, textvariable=self.precio)
        self.precioProducto.grid(row=3, column=1)
        tk.Label(self.frame3, text="Total").grid(row=4, column=0, padx=3, pady=3, sticky=tk.W)
        self.total_precio_variable=DoubleVar()
        self.totalPrecio=ttk.Entry(self.frame3, textvariable=self.total_precio_variable)
        self.totalPrecio.grid(row=4, column=1)
        ttk.Button(self.frame3, text="Calcular", command=lambda: self._calcular1(self.spin_variable.get(), self.precio.get())).grid(row=5, column=1, padx=3, pady=3)
        ttk.Button(self.frame3, text="Agregar", command=self._carrito).grid(row=5, column=0, padx=3, pady=3)


        self.frame4=ttk.Labelframe(tab1, text="Detalles", width=100)
        self.frame4.grid(row=3, column=1, padx=3, pady=3, sticky=tk.NW)
        self.tabla_detalles=ttk.Treeview(self.frame4, height=8, column=('#1', '#2', '#3', '#4', '#5', '#6', '#7'))
        self.tabla_detalles.grid(row=1, column=0)
        self.tabla_detalles.column("#1", width=100, minwidth=85)
        self.tabla_detalles.column("#2", width=100, minwidth=85)
        self.tabla_detalles.column("#3", width=100, minwidth=85)
        self.tabla_detalles.column("#4", width=100, minwidth=85)
        self.tabla_detalles.column("#5", width=100, minwidth=85)
        self.tabla_detalles.column("#6", width=100, minwidth=85)
        self.tabla_detalles.column("#7", width=100, minwidth=85)
        self.tabla_detalles['show']='headings'
        self.tabla_detalles.heading('#1', text="Id Venta ", anchor=tk.W)
        self.tabla_detalles.heading('#2', text="Id Producto ", anchor=tk.W)
        self.tabla_detalles.heading('#3', text="Recibo ", anchor=tk.W)
        self.tabla_detalles.heading('#4', text="Nombre ", anchor=tk.W)
        self.tabla_detalles.heading('#5', text="Cantidad ", anchor=tk.W)
        self.tabla_detalles.heading('#6', text="Precio ", anchor=tk.W)
        self.tabla_detalles.heading('#7', text="Total ", anchor=tk.W)


        self.frame5=tk.LabelFrame(self.frame4, width=100)
        self.frame5.grid(row=2, column=0, sticky=tk.E)
        tk.Label(self.frame5, text="Sub Total").grid(row=1, column=1, sticky=tk.W)
        self.subtotal_variable=StringVar()
        self.SubTotalEntry=ttk.Entry(self.frame5, width=10, textvariable=self.subtotal_variable)
        self.SubTotalEntry.grid(row=1, column=2, sticky=tk.W)
        tk.Label(self.frame5, text="IGV").grid(row=2, column=1, sticky=tk.W)
        self.igv_variable=StringVar()
        self.IGVEntry=ttk.Entry(self.frame5, width=10, textvariable=self.igv_variable)
        self.IGVEntry.grid(row=2, column=2, sticky=tk.W)
        tk.Label(self.frame5, text="Total").grid(row=3, column=1, sticky=tk.W)
        self.total_variable=DoubleVar()
        self.TotalEntry=ttk.Entry(self.frame5, width=10, textvariable=self.total_variable)
        self.TotalEntry.grid(row=3, column=2, sticky=tk.W)

        self.frame6=tk.LabelFrame(self.frame4)
        self.frame6.grid(row=3, column=0, sticky=tk.E)      
        ttk.Button(self.frame6, text="Agregar", command=self._prueba1).grid(row=0, column=0)
        ttk.Button(self.frame6, text="Eliminar", command=self._deleteseletion).grid(row=0, column=1)
        ttk.Button(self.frame6, text="Registrar", command=self._generarDocVenta).grid(row=0, column=3)
        ttk.Button(self.frame6, text="Actualizar", command=self._prueba2).grid(row=0, column=4)
        ttk.Button(self.frame6, text="Limpiar", command=self._limpiar).grid(row=0, column=5)
        ttk.Button(self.frame6, text="Informe", command=self._generarInforme).grid(row=0, column=6)


#=================================================================================================
        self._cargarU()
        self._cargarCodProducto()
#=================================================================================================

        self.frame_final=ttk.Labelframe(tab2, text="Recibos", width=200)
        self.frame_final.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.tabla_recibos=ttk.Treeview(self.frame_final, height=20, column=('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8'))
        self.tabla_recibos.grid(row=1, column=1, padx=3, pady=3)
        self.tabla_recibos.column('#1', width=100, minwidth=90)
        self.tabla_recibos.column('#2', width=100, minwidth=90)
        self.tabla_recibos.column('#3', width=100, minwidth=90)
        self.tabla_recibos.column('#4', width=100, minwidth=90)
        self.tabla_recibos.column('#5', width=100, minwidth=90)
        self.tabla_recibos.column('#6', width=100, minwidth=90)
        self.tabla_recibos.column('#7', width=100, minwidth=90)
        self.tabla_recibos.column('#8', width=100, minwidth=90)
        self.tabla_recibos['show']='headings'
        self.tabla_recibos.heading('#1', text="Nro Recibo", anchor=tk.W)
        self.tabla_recibos.heading('#2', text="Usuario", anchor=tk.W)
        self.tabla_recibos.heading('#3', text="Cliente", anchor=tk.W)
        self.tabla_recibos.heading('#4', text="Tipo Doc", anchor=tk.W)
        self.tabla_recibos.heading('#5', text="Fecha Venta", anchor=tk.W)
        self.tabla_recibos.heading('#6', text="Sub Total", anchor=tk.W)
        self.tabla_recibos.heading('#7', text="Igv", anchor=tk.W)
        self.tabla_recibos.heading('#8', text="Total", anchor=tk.W)
        ttk.Button(self.frame_final, text="Eliminar", command=self._DeleteRecibo).grid(row=2, column=1, padx=3, pady=3, sticky=tk.E)
        self._GetReciboVenta()
#=================================================================================================
    def _consultas(self, query, parametros=()):
        inicio=cnx.conexion(self.db_name)
        cursor=inicio.cursor()
        resultado=cursor.execute(query,parametros)
        inicio.commit()
        return resultado  

    def _generarcod(self):
        s=""
        caracteres=list(string.printable)
        caracteres=caracteres[:-39]
        for i in range (5):
            s+=random.choice(caracteres)
        self.varCodigo.set(s)
        self._cargarCodProducto()

    def _calcular1(self, a, b):
        c=a*b
        self.total_precio_variable.set(c)

    def _cargarCodProducto(self):
        listaP=list()
        query="select IdProd from Productos"
        rows=self._consultas(query)
        for row in rows:
            listaP.append(row[0])
        self.codProducto['values']=listaP

    def _cargarU(self):
        listaU=list()
        query="select IdTrabajador from Usuarios"
        rows=self._consultas(query)
        for row in rows:
            listaU.append(row[0])
        self.cmbIdUsuario['values']=listaU

    def _generarDocVenta(self):
        query="insert into Documento_Venta values(?,?,?,?,?,?,?,?)"
        parametros=(self.NroRecibo.get(), self.cmbIdUsuario.get(), self.IdCliente.get(), self.cmbTipoDoc.get(), self.FechaVenta.get_date(),self.subtotal_variable.get(),self.igv_variable.get(),self.total_variable.get())
        self._consultas(query, parametros)
        msg.showinfo("Manataro SYS", "El recibo nro {} ha sido registrado".format(self.NroRecibo.get()))
        self._GetReciboVenta()

    def _carrito(self):
        self.tabla_detalles.insert('', 'end',text=self.varCodigo.get(), values=(self.varCodigo.get(), self.codProducto.get(), self.NroRecibo.get() ,self.nombProducto.get(),self.spin_variable.get(),self.precio.get(),self.total_precio_variable.get()))      


    def _subtotal(self):
        a=float(1.18)
        b=float(self.total_variable.get())
        x=b/a
        self.subtotal_variable.set('%.2f' %x)


    def _igv(self):
        a=float(0.18)
        b=float(self.subtotal_variable.get())
        x=b*a
        self.igv_variable.set('%.2f' %x)

    def _prueba1(self):
        lista_prueba=list()
        for Parent in self.tabla_detalles.get_children():
            lista_prueba.append(float(self.tabla_detalles.item(Parent)["values"][6]))
        x=sum(lista_prueba)
        self.total_variable.set(x)
        self._subtotal()
        self._igv()        
        
    def _deleteseletion(self):
        try:
            self.tabla_detalles.item(self.tabla_detalles.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro SYS", "Por favor selecciona un item")
            return
        item_seleccionado=self.tabla_detalles.selection()
        for i in item_seleccionado:
            self.tabla_detalles.delete(i)

    def _limpiar(self):
        self.NroRecibo.delete(0, END)
        self.IdCliente.delete(0, END)
        self.CodVenta.delete(0, END)
        self.codProducto.delete(0,END)
        self.nombProducto.delete(0,END)
        self.precioProducto.delete(0,END)
        self.totalPrecio.delete(0,END)
        self.SubTotalEntry.delete(0,END)
        self.IGVEntry.delete(0,END)
        self.TotalEntry.delete(0,END)
        records=self.tabla_detalles.get_children()
        for record in records:
            self.tabla_detalles.delete(record)

        
    def _prueba2(self):
        lista_prueba=list()
        lista2=list()
        for Parent in self.tabla_detalles.get_children():            
            lista_prueba.append(self.tabla_detalles.item(Parent)["values"])
        for i in lista_prueba:
            query="insert into Detalle_Venta values(?,?,?,?,?,?,?)"
            parametros=(i[0],i[1],i[2],i[3],i[4],i[5],i[6])
            self._consultas(query,parametros)
        self._actulizarstock2()

    def _generarInforme(self):
        m2e=DetalleVenta('Reporte Ventas')
        query="select * from Detalle_Venta"
        resultados=self._consultas(query)
        for i in resultados:
            movimiento=Movimiento(i)
            movimiento.listar()
            m2e.agregarItem(movimiento)
        m2e.guardarPlanilla("Reportes_Ventas.xls")
        msg.showinfo("Mantaro Sys", "Informe Ventas Generado")

    
    def _actulizarstock2(self):
        lista1=list()
        for Parent in self.tabla_detalles.get_children():
            lista1.append(self.tabla_detalles.item(Parent)["values"])
        for i in lista1:            
            query="update Productos set StockProd=StockProd-? where IdProd=?"            
            self._consultas(query, (i[4], i[1]))
        msg.showinfo("Mantaro Sys", "Se actualizo el stock de los productos")

    def _GetReciboVenta(self):
        records=self.tabla_recibos.get_children()
        for record in records:
            self.tabla_recibos.delete(record)
        query="select * from Documento_Venta"
        db_rows=self._consultas(query)
        for i in db_rows:
            self.tabla_recibos.insert('',0,text=i[0],values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))

    def _DeleteRecibo(self):
        try:
            self.tabla_recibos.item(self.tabla_recibos.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro Sys", "Por favor seleccione un item")
            return
        nro_recibo=self.tabla_recibos.item(self.tabla_recibos.selection())['values'][0]
        query="delete from Documento_Venta where IdDocVenta=?"
        self._consultas(query,(nro_recibo, ))
        msg.showinfo("Mantaro Sys", "El recibo nro {} ha sido eliminado".format(nro_recibo))
        self._GetReciboVenta()            
        
    def _prueba_error(self):
        msg.showerror("Mantaro Sys", "Esto es un error")