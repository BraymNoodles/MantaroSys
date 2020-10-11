#===========IMPORTAR PAQUETES=============
import sqlite3
from sqlite3 import Error
import os
import sys


#=================FIN DE IMPORTACION DE PAQUETE=================#
appdir=getattr(sys,'_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

def conexion(base_datos):
    conn= None
    try:
        conn=sqlite3.connect(os.path.join(appdir, base_datos))
        return conn
    except Error as e:
        print (e)
    return conn