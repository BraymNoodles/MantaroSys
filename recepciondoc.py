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
import ingresos
from ingresos import Movimiento
import excel_ingresos
from excel_ingresos import Ingreso
#===========================================================================
class Recepcion:
    db_name="mantaro2.db"
    def __init__(self, master):
        self.master=master
        self.master.title("Mantaro SYS")
        self.master.geometry("400x400")
        pestañas=ttk.Notebook(self.master)
        tab1=ttk.Frame(pestañas)
        tab2=ttk.Frame(pestañas)
        pestañas.add(tab1, text="Recepcion Productos")
        pestañas.add(tab2, text="Detalle de Recepcion")
        pestañas.pack(expan=1, fill="both")
        #====================================
        self.frame1=ttk.Labelframe(tab1, text="Registro de Documentos", width=50)
        self.frame1.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Nro Documento").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.Id_Recepcion=ttk.Entry(self.frame1)
        self.Id_Recepcion.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Id Usuario").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.cmb_usuario=ttk.Combobox(self.frame1, width=25)
        self.cmb_usuario.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Proveedor").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.cmb_prov=ttk.Combobox(self.frame1, width=25)
        self.cmb_prov.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Tipo Documentos").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.cmb_tipo_doc=ttk.Combobox(self.frame1, width=15)
        self.cmb_tipo_doc['values']=("Factura", "Boleta")
        self.cmb_tipo_doc.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Elegir Fecha").grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.fechaR=tkcalendar.DateEntry(self.frame1)
        self.fechaR.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="SubTotal").grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.subtotal=ttk.Entry(self.frame1)
        self.subtotal.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="IGV").grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.igv=ttk.Entry(self.frame1)
        self.igv.grid(row=6,column=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(self.frame1, text="Total").grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.total=ttk.Entry(self.frame1)
        self.total.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Button(self.frame1, text="Agregar", command=self._AddDocs).grid(row=8, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        #=================================================  
       
        self.frame2=ttk.Labelframe(tab1, text="Ver Datos", width=200)
        self.frame2.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.tabla1=ttk.Treeview(self.frame2, height=10, column=('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8'))
        self.tabla1.grid(row=1, column=1, columnspan=2)
        self.tabla1.column('#1', width=100, minwidth=90)
        self.tabla1.column('#2', width=100, minwidth=90)
        self.tabla1.column('#3', width=100, minwidth=90)
        self.tabla1.column('#4', width=100, minwidth=90)
        self.tabla1.column('#5', width=100, minwidth=90)
        self.tabla1.column('#6', width=100, minwidth=90)
        self.tabla1.column('#7', width=100, minwidth=90)
        self.tabla1.column('#8', width=100, minwidth=90)
        self.tabla1['show']='headings'
        self.tabla1.heading('#1', text="Id Doc", anchor=tk.W)
        self.tabla1.heading('#2', text="Usuario", anchor=tk.W)
        self.tabla1.heading('#3', text="Proveedor", anchor=tk.W)
        self.tabla1.heading('#4', text="Tipo Doc", anchor=tk.W)
        self.tabla1.heading('#5', text="Fecha", anchor=tk.W)
        self.tabla1.heading('#6', text="Subtotal", anchor=tk.W)
        self.tabla1.heading('#7', text="IGV", anchor=tk.W)
        self.tabla1.heading('#8', text="Total", anchor=tk.W)
        ttk.Button(self.frame2, text="Editar", command=self._EditDocs).grid(row=2, column=1, padx=3, pady=3, sticky=tk.W+tk.E)
        ttk.Button(self.frame2, text="Eliminar", command=self._DeleteDocs).grid(row=2, column=2, padx=3, pady=3, sticky=tk.W+tk.E)
        #======================================================
        self.frame3=ttk.Labelframe(tab2, text="Productos", width=80)
        self.frame3.grid(row=2, column=1, padx=3, pady=3, sticky=tk.NW)
        tk.Label(self.frame3, text="Codigo Ingreso").grid(row=0, column=0, padx=3, pady=3, sticky=tk.E)
        self.varCodigo=StringVar()
        self.CodVenta=ttk.Entry(self.frame3, textvariable=self.varCodigo, width=15, state='disabled')
        self.CodVenta.grid(row=0, column=1, padx=3, pady=3, sticky=tk.W)
        tk.Label(self.frame3, text="Codigo Recibo").grid(row=1, column=0, padx=3, pady=3, sticky=tk.E)
        self.cmb_nroRecibo=ttk.Combobox(self.frame3, width=25)
        self.cmb_nroRecibo.grid(row=1, column=1)#falta cargar values
        tk.Label(self.frame3, text="Codigo Producto").grid(row=2, column=0, padx=3, pady=3, sticky=tk.E)
        self.codProducto=ttk.Combobox(self.frame3, width=25)
        self.codProducto.grid(row=2, column=1)
        tk.Label(self.frame3, text="Nombre Producto").grid(row=3, column=0, padx=3, pady=3, sticky=tk.E)
        self.nombProducto=ttk.Entry(self.frame3)
        self.nombProducto.grid(row=3, column=1)
        tk.Label(self.frame3, text="Cantidad").grid(row=4, column=0, padx=3, pady=3, sticky=tk.E)
        self.spin_variable=DoubleVar()
        self.spin=ttk.Spinbox(self.frame3, from_=0, to=20, width=5, textvariable=self.spin_variable)
        self.spin.grid(row=4, column=1)
        tk.Label(self.frame3, text="Precio").grid(row=5, column=0, padx=3, pady=3, sticky=tk.E)
        self.precio=DoubleVar()
        self.precioProducto=ttk.Entry(self.frame3, textvariable=self.precio)
        self.precioProducto.grid(row=5, column=1)
        tk.Label(self.frame3, text="Total").grid(row=6, column=0, padx=3, pady=3, sticky=tk.E)
        self.total_precio_variable=DoubleVar()
        self.totalPrecio=ttk.Entry(self.frame3, textvariable=self.total_precio_variable)
        self.totalPrecio.grid(row=6, column=1)
        ttk.Button(self.frame3, text="Generar ID", command=self._codIngreso).grid(row=7, column=0, padx=3, pady=3)
        ttk.Button(self.frame3, text="Calcular", command=lambda:self._calcular(self.spin_variable.get(), self.precio.get())).grid(row=7, column=1, padx=3, pady=3)
        ttk.Button(self.frame3, text="Agregar", command=self._agregar_tabla).grid(row=7, column=2, padx=3, pady=3)
        #======================================================

        self.frame4=ttk.Labelframe(tab2, text="Detalles", width=100)
        self.frame4.grid(row=3, column=1, padx=3, pady=3, sticky=tk.NW)
        self.tabla_detalles=ttk.Treeview(self.frame4, height=10, column=('#1', '#2', '#3', '#4', '#5', '#6', '#7'))
        self.tabla_detalles.grid(row=1, column=0)
        self.tabla_detalles.column("#1", width=100, minwidth=85)
        self.tabla_detalles.column("#2", width=100, minwidth=85)
        self.tabla_detalles.column("#3", width=100, minwidth=85)
        self.tabla_detalles.column("#4", width=100, minwidth=85)
        self.tabla_detalles.column("#5", width=100, minwidth=85)
        self.tabla_detalles.column("#6", width=100, minwidth=85)
        self.tabla_detalles.column("#7", width=100, minwidth=85)
        self.tabla_detalles['show']='headings'
        self.tabla_detalles.heading('#1', text="Codigo Registro", anchor=tk.W)
        self.tabla_detalles.heading('#2', text="Id Producto ", anchor=tk.W)
        self.tabla_detalles.heading('#3', text="Recibo ", anchor=tk.W)
        self.tabla_detalles.heading('#4', text="Nombre ", anchor=tk.W)
        self.tabla_detalles.heading('#5', text="Cantidad ", anchor=tk.W)
        self.tabla_detalles.heading('#6', text="Precio ", anchor=tk.W)
        self.tabla_detalles.heading('#7', text="Total ", anchor=tk.W)

        self.frame6=tk.LabelFrame(self.frame4)
        self.frame6.grid(row=4, column=0, sticky=tk.E)
        
        ttk.Button(self.frame6, text="Eliminar", command=self._deleteselection).grid(row=0, column=0)
        ttk.Button(self.frame6, text="Actualizar", command=self._actualizar).grid(row=0, column=1)
        ttk.Button(self.frame6, text="Limpiar", command=self._limpieza).grid(row=0, column=2)
        ttk.Button(self.frame6, text="Informe", command=self._generarInforme).grid(row=0, column=3)

#===========================================================================================================================================================================
        self._cargarU()
        self._cargarP()
        self._getDocs()
        self._cargarRecibo()
        self._cargarCodProducto()
#=================================================================================
    def _consultas(self, query, parametros=()):
        inicio=cnx.conexion(self.db_name)
        cursor=inicio.cursor()
        resultado=cursor.execute(query,parametros)
        inicio.commit()
        return resultado  

    def _cargarU(self):
        listaU=list()
        query="select IdTrabajador from Usuarios"
        rows=self._consultas(query)
        for row in rows:
            listaU.append(row[0])
        self.cmb_usuario['values']=listaU

    def _cargarCodProducto(self):
        listaP=list()
        query="select IdProd from Productos"
        rows=self._consultas(query)
        for row in rows:
            listaP.append(row[0])
        self.codProducto['values']=listaP
       

    def _cargarP(self):
        listaP=list()
        query="select IdProv from Proveedor"
        rows=self._consultas(query)
        for row in rows:
            listaP.append(row[0])
        self.cmb_prov['values']=listaP

        
    def _getDocs(self):
        records=self.tabla1.get_children()
        for record in records:
            self.tabla1.delete(record)
        query="select * from Documento_Recepcion"
        db_rows=self._consultas(query)
        for i in db_rows:
            self.tabla1.insert('',0,text=i[0],values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))

    def _AddDocs(self):
        query="insert into Documento_Recepcion values(?,?,?,?,?,?,?,?)"
        parametros=(self.Id_Recepcion.get(), self.cmb_usuario.get(), self.cmb_prov.get(), self.cmb_tipo_doc.get(), self.fechaR.get_date(), self.subtotal.get(), self.igv.get(), self.total.get())
        self._consultas(query, parametros)
        msg.showinfo("Mantaro Sys","El recibo Nro {} se ha registrado".format(self.Id_Recepcion.get()))
        self.Id_Recepcion.delete(0,END)
        self.subtotal.delete(0,END)
        self.igv.delete(0, END)
        self.total.delete(0, END)
        self._getDocs()

    def _DeleteDocs(self):
        try:
            self.tabla1.item(self.tabla1.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro SYS", "Por favor seleccione un item")
            return
        cod_recibo=self.tabla1.item(self.tabla1.selection())['values'][0]
        query="delete from Documento_Recepcion where IdDocRec=?"
        self._consultas(query, (cod_recibo,))
        msg.showinfo("Mantaro SYS", "El recibo de codigo nro {} ha sido eliminado".format(cod_recibo))
        self._getDocs()        

    def _EditDocs(self):
        try:
            self.tabla1.item(self.tabla1.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro SYS", "Por favor seleccione un item")
            return
        cod_recibo=self.tabla1.item(self.tabla1.selection())['values'][0]
        self.edit_wind=tk.Toplevel()
        self.edit_wind.title("Editar Docs")
        self.frame_edicion=tk.LabelFrame(self.edit_wind, text="Editar Docs", width=100)
        self.frame_edicion.grid(row=0, column=0, padx=3, pady=3, sticky=tk.W)
        tk.Label(self.frame_edicion, text="Usuario").grid(row=1, column=0, padx=3, pady=3, sticky=tk.E)
        cmbUsuario=ttk.Combobox(self.frame_edicion, width=18)
        cmbUsuario.grid(row=1, column=1, padx=3, pady=3, sticky=tk.W)
        listaUsuarios=list()
        query="select IdTrabajador from Usuarios"
        rows=self._consultas(query)
        for row in rows:
            listaUsuarios.append(row[0])
        cmbUsuario['values']=listaUsuarios
        tk.Label(self.frame_edicion, text="Proveedor").grid(row=2, column=0, padx=3, pady=3, sticky=tk.E)
        cmbProveedor=ttk.Combobox(self.frame_edicion, width=18)
        cmbProveedor.grid(row=2, column=1, padx=3, pady=3, sticky=tk.W)
        listaProveedor=list()
        query2="select IdProv from Proveedor"
        rows2=self._consultas(query2)
        for i in rows2:
            listaProveedor.append(i[0])
        cmbProveedor['values']=listaProveedor
        tk.Label(self.frame_edicion, text="Tipo Documento").grid(row=3, column=0, padx=3, pady=3, sticky=tk.E)
        cmbTipoDoc=ttk.Combobox(self.frame_edicion, width=20)
        cmbTipoDoc.grid(row=3, column=1, padx=3, pady=3, sticky=tk.W)
        cmbTipoDoc['values']=['Factura', 'Boleta']
        tk.Label(self.frame_edicion, text="Fecha Recepcion").grid(row=4, column=0, padx=3, pady=3, sticky=tk.E)
        fechaRegisto=tkcalendar.DateEntry(self.frame_edicion)
        fechaRegisto.grid(row=4, column=1, padx=3, pady=3, sticky=tk.W)
        tk.Label(self.frame_edicion, text="Sub Total").grid(row=5, column=0, padx=3, pady=3, sticky=tk.E)
        entrada_subtotal=ttk.Entry(self.frame_edicion)
        entrada_subtotal.grid(row=5, column=1, pady=3, padx=3, sticky=tk.W)
        tk.Label(self.frame_edicion, text="IGV").grid(row=6, column=0, padx=3, pady=3, sticky=tk.E)
        entrada_IGV=ttk.Entry(self.frame_edicion)
        entrada_IGV.grid(row=6, column=1, pady=3, padx=3, sticky=tk.W)
        tk.Label(self.frame_edicion, text="Total").grid(row=7, column=0, padx=3, pady=3, sticky=tk.E)
        entrada_total=ttk.Entry(self.frame_edicion)
        entrada_total.grid(row=7, column=1, pady=3, padx=3, sticky=tk.W)
        ttk.Button(self.frame_edicion, text="Actualizar", command=lambda:self._EditarDocumento(cod_recibo, cmbUsuario.get(), cmbProveedor.get(), cmbTipoDoc.get(), fechaRegisto.get_date(), entrada_subtotal.get(),entrada_IGV.get(),entrada_total.get())).grid(row=8, column=1, pady=3, padx=3, sticky=tk.W)

    def _EditarDocumento(self, id, u, p, t, fecha, subtotal, igv, total):
        query="update Documento_Recepcion set UsuarioId=?, ProvId=?, TipoDoc=?, FechaRecepcion=?, SUBTOTAL=?, IGV=?, TOTAL=? where IdDocRec=?"
        parametros=(u,p,t,fecha,subtotal,igv,total,id)
        self._consultas(query, parametros)
        self.edit_wind.destroy()
        msg.showinfo("Mantaro SYS","El documento nro {} ha sido actualizado".format(id))
        self._getDocs()
#====================================================================================================================================================================================================================================================================================================================

    def _cargarRecibo(self):
        query="select IdDocRec from Documento_Recepcion"
        datos=list()
        rows=self._consultas(query)
        for row in rows:
            datos.append(row[0])
        self.cmb_nroRecibo['values']=datos

    def _codIngreso(self):
        s=""
        caracteres=list(string.printable)
        caracteres=caracteres[:-39]
        for i in range(5):
            s+=random.choice(caracteres)
        self.varCodigo.set(s)
        self._cargarRecibo()
        self._cargarCodProducto()

    def _calcular(self, a, b):
        c=a*b
        self.total_precio_variable.set(c)

    def _agregar_tabla(self):
        self.tabla_detalles.insert('', 'end', text=self.varCodigo.get(), values=(self.varCodigo.get(), self.codProducto.get(),self.cmb_nroRecibo.get(), self.nombProducto.get(), self.spin_variable.get(), self.precio.get(), self.total_precio_variable.get()))
        

    def _deleteselection(self):
        try:
            self.tabla_detalles.item(self.tabla_detalles.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro Sys", "Por favor selecciona un item")
            return
        item_selccionado=self.tabla_detalles.selection()
        for i in item_selccionado:
            self.tabla_detalles.delete(i)

    def _actualizar(self):
        lista1=list()
        for Parent in self.tabla_detalles.get_children():
            lista1.append(self.tabla_detalles.item(Parent)["values"])
        for i in lista1:
            query="insert into Detalle_Ingreso values(?,?,?,?,?,?,?)"
            parametros=(i[0],i[1],i[2],i[3],i[4],i[5],i[6])
            self._consultas(query, parametros)
        msg.showinfo("Mantaro Sys", "Se registro el registro actual")
        self._actulizarstock2()

    def _limpieza(self):
        self.nombProducto.delete(0, END)
        self.precioProducto.delete(0, END)
        self.totalPrecio.delete(0,END)
        records=self.tabla_detalles.get_children()
        for record in records:
            self.tabla_detalles.delete(record)

    def _generarInforme(self):
        m2e=Ingreso("Reporte Ingresos")        
        query="select * from Detalle_Ingreso"
        resultados=self._consultas(query)
        for i in resultados:
            movimiento=Movimiento(i)
            movimiento.listar()
            m2e.agregarItem(movimiento)
        m2e.guardarPlanilla("Reportes_Ingresos.xls")
        msg.showinfo("Mantaro Sys", "Informe Ingresos Generado")
        

    def _actulizarstock(self):
        query="update Productos set StockProd=StockProd+? where IdProd=?"
        parametros=(self.spin_variable.get(), self.codProducto.get())
        self._consultas(query, parametros)
        print("ok")

    def _actulizarstock2(self):
        lista1=list()
        for Parent in self.tabla_detalles.get_children():
            lista1.append(self.tabla_detalles.item(Parent)["values"])
        for i in lista1:            
            query="update Productos set StockProd=StockProd+? where IdProd=?"            
            self._consultas(query, (i[4], i[1]))
        msg.showinfo("Mantaro Sys", "Se actualizo el stock de los productos")








