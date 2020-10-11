import xlwt


class Ingreso:


    def __init__(self,name):
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet(name,cell_overwrite_ok=True)
        self.ws.write(0,0, name)
        
        columnas = ["Codigo de Ingreso",
                    "Codigo de Producto",
                    "Nro de Recibo",
                    "Nombre de Producto",
                    "Cantidad"
                    "Precio"
                    "Total"]

        c = 0
        for columna in columnas:
            self.ws.write(1,c,columna)
            c = c + 1

        self.fila = 2


    def agregarItem(self, item):
        self.ws.write(self.fila, 0, item.IdIngreso)
        self.ws.write(self.fila, 1, item.ProductoId)
        self.ws.write(self.fila, 2, item.NroRecibo)
        self.ws.write(self.fila, 3, item.NombreProducto)
        self.ws.write(self.fila, 4, item.Cantidad)
        self.ws.write(self.fila, 5, item.Precio)
        self.ws.write(self.fila, 6, item.Total)


        self.fila=self.fila + 1


    def guardarPlanilla(self, archivo):
        self.wb.save(archivo)
        print("Generado")