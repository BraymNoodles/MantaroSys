class Movimiento:

    def __init__(self, lista):
        
        self.IdDetalle = lista[0]
        self.ProductoId = lista[1]
        self.NroRecibo = lista[2]
        self.NombreProducto = lista[3]
        self.Cantidad = lista[4]
        self.Precio = lista[5]
        self.Total = lista[6]

    def listar(self):
        print(self.IdDetalle, self.ProductoId, self.NroRecibo,
              self.NombreProducto, self.Cantidad, self.Precio, self.Total)
