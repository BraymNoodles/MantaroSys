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


class Categoria_Productos:
    db_name="mantaro2.db"
    def __init__(self, master):
        self.master=master
        self.master.title("Mantaro Sys Productos")
        self.master.geometry("400x400")
        control_productos=ttk.Notebook(self.master)
        tab_productos=ttk.Frame(control_productos)
        control_productos.add(tab_productos, text="Productos")
        tab_categorias=ttk.Frame(control_productos)
        control_productos.add(tab_categorias, text="Visualizar Categorias")
        control_productos.pack(expan=1, fill="both")
        #RELLENAR VISUALIZAR CATEGORIAS
        self.ContenedorCateogrias=ttk.Labelframe(tab_categorias, text="Categoria Productos", width=30)
        self.ContenedorCateogrias.grid(row=1, column=1, pady=8, padx=8, sticky=tk.W)
        tk.Label(self.ContenedorCateogrias, text="ID CATEGORIA").grid(row=0, column=0, pady=8, padx=8, sticky=tk.E)
        self.ID_ENTRADA=ttk.Entry(self.ContenedorCateogrias)
        self.ID_ENTRADA.grid(row=0, column=1, pady=8, padx=8, sticky=tk.W)
        tk.Label(self.ContenedorCateogrias, text="NOMBRE CATEGORIA").grid(row=1, column=0, pady=8, padx=8, sticky=tk.E)
        self.Nombre_Cate=ttk.Entry(self.ContenedorCateogrias)
        self.Nombre_Cate.grid(row=1, column=1, pady=8, padx=8, sticky=tk.W)
        tk.Label(self.ContenedorCateogrias, text="DESCRIPCION CATEGORIA").grid(row=2, column=0, pady=8, padx=8, sticky=tk.E)
        self.scr_desc=scrolledtext.ScrolledText(self.ContenedorCateogrias, width=30, height=10, wrap=tk.WORD)
        self.scr_desc.grid(row=2, column=1, columnspan=3, sticky=tk.W)
        tk.Label(self.ContenedorCateogrias, text="ESTADO CATEGORIA").grid(row=3, column=0, pady=8, padx=8, sticky=tk.E)
        self.combo=ttk.Combobox(self.ContenedorCateogrias, width=10)
        self.combo['values']=("Activo", "Inactivo")
        self.combo.grid(row=3, column=1, pady=8, padx=8, sticky=tk.W)
        self.combo.current(0)
        tk.Button(self.ContenedorCateogrias, text="GUARDAR", command=self._addcat).grid(row=4, column=1, pady=5, padx=5, stick=tk.E+tk.W)
        
        #label frame para ver lo que se agrega
        self.VisorCategoria=ttk.Labelframe(tab_categorias, text="Categorias", width=30)
        self.VisorCategoria.grid(row=3, column=1, padx=8, pady=8, sticky=tk.E)
        #agregar tabla
        self.tablaCat=ttk.Treeview(self.VisorCategoria, height=8, columns=('#1','#2','#3','#4'))
        self.tablaCat.grid(row=1, column=1, columnspan=2)
        self.tablaCat['show']='headings'
        self.tablaCat.heading('#1', text="ID CATEGORIA", anchor="w")
        self.tablaCat.heading('#2', text="NOMBRE CATEGORIA", anchor="w")
        self.tablaCat.heading('#3', text="DESCRIPCION CATEGORIA", anchor="w")
        self.tablaCat.heading('#4', text="ESTADO CATEGORIA", anchor="w")
        ttk.Button(self.VisorCategoria, text="EDITAR", command=self._editcat).grid(row=3, column=1, padx=2, pady=2, sticky=tk.W+tk.E)
        ttk.Button(self.VisorCategoria, text="ELIMINAR", command=self._deletecat).grid(row=3, column=2, padx=2, pady=2, sticky=tk.W+tk.E)
        self._cargarcat()

        #RELLENANDO TAB  PRODUCTOS
        self.ContenedorProductos=ttk.Labelframe(tab_productos, text="DATOS PRODUCTOS", width=30)
        self.ContenedorProductos.grid(row=1, column=1, pady=5, padx=5, sticky=tk.E)
        ttk.Label(self.ContenedorProductos, text="Codigo Producto").grid(row=0, column=0, padx=4, pady=4, sticky=tk.W)
        self.Cod_Prod=ttk.Entry(self.ContenedorProductos)
        self.Cod_Prod.grid(row=0, column=1, padx=4, pady=4, sticky=tk.E)
        ttk.Label(self.ContenedorProductos, text="Codigo Categoria").grid(row=1, column=0, padx=4, pady=4, sticky=tk.W)
        self.Cmb_Categoria=ttk.Combobox(self.ContenedorProductos, width=15)
        self.Cmb_Categoria.grid(row=1, column=1, padx=4, pady=4, sticky=tk.E)
        ttk.Label(self.ContenedorProductos, text="Nombre Producto").grid(row=2, column=0, padx=4, pady=4, sticky=tk.W)
        self.Nomb_Prod=ttk.Entry(self.ContenedorProductos)
        self.Nomb_Prod.grid(row=2, column=1, padx=4, pady=4, sticky=tk.E)
        ttk.Label(self.ContenedorProductos, text="Descripcion Producto").grid(row=3, column=0, padx=4, pady=4, sticky=tk.W)
        self.scr_descripcion_producto=scrolledtext.ScrolledText(self.ContenedorProductos, width=30, height=10, wrap=tk.WORD)
        self.scr_descripcion_producto.grid(row=3, column=1, columnspan=2, sticky=tk.W)       
        ttk.Label(self.ContenedorProductos, text="Precio Producto").grid(row=4, column=0, padx=4, pady=4, sticky=tk.W)
        self.Precio_Prod=ttk.Entry(self.ContenedorProductos)
        self.Precio_Prod.grid(row=4, column=1, padx=4, pady=4, sticky=tk.E)        
        ttk.Label(self.ContenedorProductos, text="Stock").grid(row=5, column=0, padx=4, pady=4, sticky=tk.W)
        self.Stock_Prod=ttk.Entry(self.ContenedorProductos)
        self.Stock_Prod.grid(row=5, column=1, padx=4, pady=4, sticky=tk.E)
        ttk.Label(self.ContenedorProductos, text="Estado").grid(row=6, column=0, padx=4, pady=4, sticky=tk.W)
        self.cmb_estado=ttk.Combobox(self.ContenedorProductos, width=20)
        self.cmb_estado['values']=("Disponible", "No Disponible")
        self.cmb_estado.grid(row=6, column=1, padx=4, pady=4, sticky=tk.E)
        self.botonRegisProd=ttk.Button(self.ContenedorProductos, text="Registrar Producto", command=self._addProductos).grid(row=7, column=1, padx=4, pady=4, sticky=tk.W+tk.E)
        #actualizar stock
        self.contenededoractualizacion1=ttk.Labelframe(tab_productos, text="Actualizar Stock", width=30)
        self.contenededoractualizacion1.grid(row=1, column=2, pady=5, padx=5, sticky=tk.N)
        self.tablaActualizacion=ttk.Treeview(self.contenededoractualizacion1, height=10, columns=('#1', '#2', '#3', '#4','#5','#6','#7'))
        self.tablaActualizacion.grid(row=1, column=1, columnspan=2)
        self.tablaActualizacion.column('#1',width=100, minwidth=10)
        self.tablaActualizacion.column('#2',width=150, minwidth=10)
        self.tablaActualizacion.column('#3',width=100, minwidth=10)
        self.tablaActualizacion.column('#4',width=150, minwidth=10)
        self.tablaActualizacion.column('#5',width=150, minwidth=10)
        self.tablaActualizacion.column('#6',width=150, minwidth=10)
        self.tablaActualizacion.column('#7',width=150, minwidth=10)               
        self.tablaActualizacion['show']='headings'
        self.tablaActualizacion.heading('#1', text="Cod Producto", anchor=tk.CENTER)
        self.tablaActualizacion.heading('#2', text="Cod Categoria", anchor=tk.W)
        self.tablaActualizacion.heading('#3', text="Nombre Producto", anchor=tk.W)
        self.tablaActualizacion.heading('#4', text="Descripcion", anchor=tk.CENTER)
        self.tablaActualizacion.heading('#5', text="Precio Producto", anchor=tk.CENTER)
        self.tablaActualizacion.heading('#6', text="Stock", anchor=tk.CENTER)
        self.tablaActualizacion.heading('#7', text="Estado", anchor=tk.CENTER)        
        self.botonEditar=ttk.Button(self.contenededoractualizacion1, text="Editar", command=self._editarProductos).grid(row=3,column=1,sticky=tk.W+tk.E)
        self.botonEliminar=ttk.Button(self.contenededoractualizacion1, text="Eliminar", command=self._deleteProductos).grid(row=3,column=2,sticky=tk.W+tk.E)
        self._cargarcategorias()
        self._getProductos()
#=============================================================================================================================================================    
    def _consultas(self, query, parametros=()):
        inicio=cnx.conexion(self.db_name)
        cursor=inicio.cursor()
        resultado=cursor.execute(query,parametros)
        inicio.commit()
        return resultado    
    
    def _cargarcat(self):
        records=self.tablaCat.get_children()
        for record in records:
            self.tablaCat.delete(record)
        query="select * from Categoria_Producto"
        db_rows=self._consultas(query)
        for i in db_rows:
            self.tablaCat.insert('',0,text=i[0],values=(i[0],i[1],i[3],i[2]))

    def _addcat(self):
        query='insert into Categoria_Producto values(?,?,?,?)'
        parametros=(self.ID_ENTRADA.get(),self.Nombre_Cate.get(), self.combo.get(), self.scr_desc.get('1.0', 'end-1c'))
        self._consultas(query, parametros)
        msg.showinfo("Mantaro SYS","Categoria {} se ha registrado".format(self.Nombre_Cate.get()))
        self.ID_ENTRADA.delete(0,END)
        self.Nombre_Cate.delete(0, END)        
        self._cargarcat()
        self._cargarcategorias()
    
    def _deletecat(self):
        try:
            self.tablaCat.item(self.tablaCat.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro SYS", "Por Favor Seleccione una categoria")
            return
        cod_cate=self.tablaCat.item(self.tablaCat.selection())['text']
        query="delete from Categoria_Producto where IdCatProd=?"
        self._consultas(query,(cod_cate,))
        msg.showinfo("Mantaro SYS", "La categoria {} ha sido eliminada".format(cod_cate))
        self._cargarcat()
        self._cargarcategorias()

    def _editcat(self):
        try:
            self.tablaCat.item(self.tablaCat.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro SYS", "Por Favor Seleccione una categoria")
            return        
        codigoCate=self.tablaCat.item(self.tablaCat.selection())['text']
        self.edit_wind1=tk.Toplevel()
        self.edit_wind1.title("Editar Categorias")
        self.frame1=ttk.Labelframe(self.edit_wind1, text="Editar Categoria", width=50)
        self.frame1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(self.frame1, text="Nombre Categoria").grid(row=1, column=0, padx=3, pady=3, sticky=tk.E)
        nomb_cate=tk.Entry(self.frame1)
        nomb_cate.grid(row=1, column=1, sticky=tk.W)
        tk.Label(self.frame1, text="Descripcion Categoria").grid(row=2, column=0, padx=3, pady=3, sticky=tk.E)
        scrolled_nuevo=scrolledtext.ScrolledText(self.frame1, width=30, height=10, wrap=tk.WORD)
        scrolled_nuevo.grid(row=2, column=1, pady=3, padx=3, sticky=tk.W)
        tk.Label(self.frame1, text="Estado Categoria").grid(row=3, column=0, padx=3, pady=3, sticky=tk.E)
        nuevo_cmb=ttk.Combobox(self.frame1, width=20)
        nuevo_cmb['values']=("Disponible", "No Disponible")
        nuevo_cmb.grid(row=3, column=1, padx=3, pady=3, sticky=tk.W)
        ttk.Button(self.frame1, text="Actualiza", command=lambda: self._edicioncategoria(codigoCate, nomb_cate.get(), scrolled_nuevo.get('1.0', 'end-1c'), nuevo_cmb.get())).grid(row=4,column=1, padx=2, pady=2, sticky=tk.W)

    def _edicioncategoria(self, codigo_categoria,nuevo_nomb_cate, nueva_desc_cate, nuevo_estado_cate):
        query="update Categoria_Producto set NomCatProd=?, EstadoCatProd=?, DescrCategoria=? where IdCatProd=?"
        parametros=(nuevo_nomb_cate, nuevo_estado_cate, nueva_desc_cate, codigo_categoria)
        self._consultas(query, parametros)
        self.edit_wind1.destroy()
        msg.showinfo("Mantaro SYS","La categoria {} actualizada".format(codigo_categoria))
        self._cargarcat()
#-----------------------------------PRODUCTOS--------------------------------
    def _cargarcategorias(self):
        list_categorias=list()
        query="SELECT IdCatProd from Categoria_Producto"
        rows=self._consultas(query)
        for row in rows:
            list_categorias.append(row[0])
        self.Cmb_Categoria['values']=list_categorias

    def _getProductos(self):
        records=self.tablaActualizacion.get_children()
        for record in records:
            self.tablaActualizacion.delete(record)
        query="select * from Productos"
        db_rows=self._consultas(query)
        for i in db_rows:
            self.tablaActualizacion.insert('',0,text=i[0],values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))

    def _addProductos(self):
       query="insert into Productos values(?,?,?,?,?,?,?)"
       parametros=(self.Cod_Prod.get(), self.Cmb_Categoria.get(), self.Nomb_Prod.get(), self.scr_descripcion_producto.get('1.0', 'end-1c'), self.Precio_Prod.get(), self.Stock_Prod.get(),self.cmb_estado.get())
       self._consultas(query, parametros)
       msg.showinfo("Mantaro Sys","El producto {} se ha registrado".format(self.Nomb_Prod.get()))
       self.Cod_Prod.delete(0,END)
       self.Nomb_Prod.delete(0, END)
       self.Precio_Prod.delete(0, END)
       self.Stock_Prod.delete(0, END)
       self._getProductos()

    def _deleteProductos(self):
        try:
            self.tablaActualizacion.item(self.tablaActualizacion.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro SYS", "Por favor seleccione un producto")
            return
        cod_producto=self.tablaActualizacion.item(self.tablaActualizacion.selection())['text']
        query="delete from Productos where IdProd=?"
        self._consultas(query, (cod_producto, ))
        msg.showinfo("Mantaro SYS", "El codigo de producto {} ha sido eliminada".format(cod_producto))
        self._getProductos()

    def _editarProductos(self):
        try:
            self.tablaActualizacion.item(self.tablaActualizacion.selection())['text'][0]
        except IndexError as e:
            msg.showwarning("Mantaro SYS", "Por favor seleccione un producto")
            return
        cod_producto=self.tablaActualizacion.item(self.tablaActualizacion.selection())['text']
        self.edit_wind2=tk.Toplevel()
        self.edit_wind2.title("Editar Producto")
        self.frame2=tk.LabelFrame(self.edit_wind2, text="Editar Producto", width=100)
        self.frame2.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        tk.Label(self.frame2, text="Categoria Producto").grid(row=0, column=0, padx=2, pady=2, sticky=tk.E)
        cat_prod=ttk.Combobox(self.frame2, width=15)
        cat_prod.grid(row=0, column=1, pady=2, padx=2, sticky=tk.W)
        list_categorias=list()
        query="SELECT IdCatProd from Categoria_Producto"
        rows=self._consultas(query)
        for row in rows:
            list_categorias.append(row[0])
        cat_prod['values']=list_categorias
        tk.Label(self.frame2, text="Nombre Producto").grid(row=1, column=0, pady=2, padx=2, sticky=tk.E)
        nombre_producto=ttk.Entry(self.frame2)
        nombre_producto.grid(row=1, column=1, pady=2, padx=2, sticky=tk.W)
        tk.Label(self.frame2, text="Descripcion Producto").grid(row=2, column=0, pady=2, padx=2, sticky=tk.E)
        descripcion_producto=scrolledtext.ScrolledText(self.frame2, height=10, width=30, wrap=tk.WORD)
        descripcion_producto.grid(row=2, column=1, sticky=tk.W, columnspan=2, pady=2, padx=2)
        tk.Label(self.frame2, text="Precio Producto").grid(row=3, column=0, pady=2, padx=2, sticky=tk.E)
        precio_producto=ttk.Entry(self.frame2)
        precio_producto.grid(row=3, column=1, pady=2, padx=2, sticky=tk.W)
        tk.Label(self.frame2, text="Stock Producto").grid(row=4, column=0, pady=2, padx=2, sticky=tk.E)
        stock_producto=ttk.Entry(self.frame2)
        stock_producto.grid(row=4, column=1, pady=2, padx=2, sticky=tk.W)
        tk.Label(self.frame2, text="Estado Producto").grid(row=5, column=0, pady=2, padx=2, sticky=tk.E)
        combo_estado=ttk.Combobox(self.frame2, width=20)
        combo_estado['values']=("Disponible", "No Disponible")
        combo_estado.grid(row=5, column=1, pady=2, padx=2, sticky=tk.W)
        ttk.Button(self.frame2, text="Actualizar",command=lambda:self._edicionProducto(cod_producto,cat_prod.get(),nombre_producto.get(),descripcion_producto.get('1.0', 'end-1c'), precio_producto.get(),stock_producto.get(),combo_estado.get())).grid(row=6, column=1, padx=2, pady=2, sticky=tk.W+tk.E)

    def _edicionProducto(self, id, categoria, nombre, descripcion, precio, stock, estado):
        query="update Productos set CatProd=?, NombProd=?, DescrProd=?, PrecProd=?, StockProd=?, EstadoProd=? where IdProd=?"
        parametros=(categoria, nombre,descripcion,precio,stock,estado,id)
        self._consultas(query, parametros)
        self.edit_wind2.destroy()
        msg.showinfo("Mantaro SYS","El Producto {} ha sido actualizado".format(id))
        self._getProductos()














