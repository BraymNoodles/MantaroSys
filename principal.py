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
import proveedores
from proveedores import Proveedores
from proveedores import *
import productos
from productos import Categoria_Productos
from productos import *
import clientes
from clientes import Clientes
from clientes import *
import colaboradores
from colaboradores import Colaboradores
from colaboradores import *
import herramientas
from herramientas import Roles
from herramientas import Usuarios
from herramientas import *
import recepciondoc
from recepciondoc import Recepcion
from recepciondoc import *
import ventas
from ventas import Ventas
from ventas import *
import ingresos
from ingresos import *
import movimientos
from movimientos import *
import excel_ingresos
from excel_ingresos import *
import excel_venta
from excel_venta import *
#=================FIN DE IMPORTACION DE PAQUETE=================#
appdir=getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
class PantallaPrincipal:

    data_base="mantaro2.db"
    

    def __init__(self, window):
        self.wind=window
        self.wind.geometry("1368x700")
        self.wind.title("Aplicación Mantaro")        
        self.menu_bar=Menu(self.wind)
        self.wind.configure(background="lightgreen")
        self.wind.config(menu=self.menu_bar)
        
        #AGREGAR CONTENIDO AL MENU
        #1
        file_menu=Menu(self.wind, tearoff=0)
        file_menu.add_command(label="Detalles")
        file_menu.add_separator()
        file_menu.add_command(label="Información", command=self._mensaje)
        file_menu.add_command(label="Roles del Sistema", command=self._new_window5)
        file_menu.add_command(label="Configuracion Usuarios", command=self._new_window6)
        file_menu.add_command(label="Salir", command=self._salir)
        #2 MENUS DE GESTION TIENDA
        file_menu1=Menu(self.wind, tearoff=0)
        file_menu1.add_command(label="Proveedores", command=self._new_window)
        file_menu1.add_command(label="Registro de Documentos", command=self._new_window7)
        file_menu1.add_command(label="Gestion Productos", command=self._new_window2)
        #3 MENU DE GESTION DE CLIENTES
        file_menu2=Menu(self.wind, tearoff=0)
        file_menu2.add_command(label="Clientes", command=self._new_window3)
        #4 MENU DE GESTION DE CLIENTES
        file_menu3=Menu(self.wind, tearoff=0)
        file_menu3.add_command(label="Colaboradores", command=self._new_window4)
        #5 MENU DE VENTAS
        file_menu4=Menu(self.wind, tearoff=0)
        file_menu4.add_command(label="Generar Ventas", command=self._new_window8)
        #RELLENAR MENU
        self.menu_bar.add_cascade(label="Archivo", menu=file_menu)
        self.menu_bar.add_cascade(label="Gestión Tienda", menu=file_menu1)
        self.menu_bar.add_cascade(label="Gestion Clientes", menu=file_menu2)
        self.menu_bar.add_cascade(label="Gestion Colaboradores", menu=file_menu3)
        self.menu_bar.add_cascade(label="Gestion Caja", menu=file_menu4)     
        
        
        
     #______COMANDOS__________________

    def _new_window(self):
        self.newWindow=tk.Toplevel(self.wind)
        self.app=proveedores.Proveedores(self.newWindow)

    def _new_window2(self):
        self.newWindow=tk.Toplevel(self.wind)
        self.app=productos.Categoria_Productos(self.newWindow)

    def _new_window3(self):
        self.newWindow=tk.Toplevel(self.wind)
        self.app=clientes.Clientes(self.newWindow)
    
    def _new_window4(self):
        self.newWindow=tk.Toplevel(self.wind)
        self.app=colaboradores.Colaboradores(self.newWindow)

    def _new_window5(self):
        self.newWindow=tk.Toplevel(self.wind)
        self.app=herramientas.Roles(self.newWindow)

    def _new_window6(self):
        self.newWindow=tk.Toplevel(self.wind)
        self.app=herramientas.Usuarios(self.newWindow)

    def _new_window7(self):
        self.newWindow=tk.Toplevel(self.wind)
        self.app=recepciondoc.Recepcion(self.newWindow)
 
    def _new_window8(self):
        self.newWindow=tk.Toplevel(self.wind)
        self.app=ventas.Ventas(self.newWindow)

    def _mensaje(self):
        msg.showinfo("Mantaro Sys", "Es un sistema piloto para la gestión de los principales activos de la empresa; productos, personal, clientes entre otros.")

    def _salir(self):
        self.wind.destroy() 
 
      

if __name__=="__main__":
    window=tk.Tk()
    app=PantallaPrincipal(window)
    window.mainloop()