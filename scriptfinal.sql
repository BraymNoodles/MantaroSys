create table "Tipo_Prov"(
	"IdTipProv" TEXT not null,
	"DescrTipProv" text null,
	primary key("IdTipProv")
);
create table "Proveedor"(
	"IdProv" text not null,
	"TipProv" text not null,
	"RazonProv" text not null,
	"NombProv" text not null,
	"ApellProv" text not null,
	"TelProv" text not null,
	"DirProv" text not null,
	"EmailProv" text not null,
	primary key("IdProv"),
	FOREIGN KEY ("TipProv") REFERENCES Tipo_Prov("IdTipProv")
);
create table "Tipo_Doc"(
	"IdTipDoc" text not null,
	"DescrpTipDoc" text not null,
	PRIMARY KEY("IdTipDoc"));
create table "Tipo_Cliente"(
	"IdTipCli" text not null,
	"DescTipCli" text not null,
	PRIMARY KEY ("IdTipCLi"));
create table "Cliente"(
	"IdCliente" TEXT not null,
	"TipCliente" text not null,
	"RazCliente" text not null,
	"NombCliente" text not null,
	"ApelCliente" text not null,
	"TelCliente" text not null,
	"DirCliente" text not null,
	"EmailCliente" text not null,
	PRIMARY KEY("IdCliente"),
	FOREIGN KEY("TipCliente") REFERENCES Tipo_Cliente("IdTipCli"));
create table "Categoria_Producto"(
	"IdCatProd" text not null,
	"NomCatProd" text not null,
	"EstadoCatProd" text not null,
	PRIMARY KEY("IdCatProd"));
create table "Productos"(
	"IdProd" text not null,
	"CatProd" text not null,
	"NombProd" text not null,
	"DescrProd" text null,
	"PrecProd" real not null,
	"StockProd" INTEGER not null,
	"EstadoProd" text not null,
	primary key ("IdProd"),
	FOREIGN KEY("CatProd") REFERENCES Categoria_Producto("IdCatProd"));
create table "Colaboradores"(
	"IdColaborador" text not null,
	"NombColaborador" text not null,
	"ApePatColab" text not null,
	"ApeMatColab" text not null,
	"NroColab" text not null,
	"DirColab" text not null,
	"EmailColab" text not null,
	"FechaRegistro" text not null,
	primary key ("IdColaborador")
);
create table "Roles"(
	"IdRol" INTEGER not null primary key AUTOINCREMENT,
	"NombRol" text not null,
	"DescRol" text not null);
create table "Usuarios"(
	"IdTrabajador" text not null,
	"RolId" INTEGER not null,
	"pass" text not null,
	PRIMARY KEY("IdTrabajador"),
	FOREIGN KEY ("IdTrabajador") REFERENCES Colaboradores("IdColaborador"),
	FOREIGN KEY("RolId") REFERENCES Roles("IdRol"));
create table "Documento_Venta"(
	"IdDocVenta" text not null,
	"TrabajadorId" text not null,
	"ClienteId" text not null,
	"TipoDoc" text not null,
	"FechaVenta" text not null,
	"SubTotal" real not null,
	"IGV" real not null,
	"TotalVenta" real not null,
	PRIMARY KEY("IdDocVenta"),
	FOREIGN KEY("TrabajadorId") REFERENCES Usuarios("IdTrabajador"),
	FOREIGN KEY("ClienteId") REFERENCES Cliente("IdCliente"),
	FOREIGN KEY("TipoDoc") REFERENCES Tipo_Doc("IdTipDoc"));
create table "Detalle_Venta"(
	"IdDetalVenta" text not null,
	"ProductoId" text not null,
	"DocVentaId" text not null,
	"PrecioDetalVenta" real not null,
	"CantidadDetalVenta" INTEGER not null,
	"Descuento" real null,
	"ParcialTotal" real not null,
	PRIMARY KEY("IdDetalVenta", "ProductoId"),
	FOREIGN KEY("ProductoId") REFERENCES Productos("IdProd"),
	FOREIGN KEY("DocVentaId") REFERENCES Documento_Venta("IdDocVenta")
);
create table "Documento_Recepcion"(
	"IdDocRec" text not null,
	"UsuarioId" text not null,
	"ProvId" text not null,
	"TipoDoc" text not null,
	"FechaRecepcion" text not null,
	"SUBTOTAL" real not null,
	"IGV" real not NULL,
	"TOTAL" real not null,
	primary key("IdDocRec"),
	FOREIGN KEY("UsuarioId") REFERENCES Usuarios("IdTrabajador"),
	FOREIGN KEY("ProvId") REFERENCES Proveedor("IdProv"),
	FOREIGN KEY("TipoDoc") REFERENCES Tipo_Doc("IdTipDoc")
);
create table "Detalle_Ingreso"(
	"IdIngreso" text not null,
	"ProductoId" text not null,
	"IdRecDoc" text not null,
	"PrecioIng" real not null,
	"CantidadIng" INTEGER not null,
	PRIMARY KEY("IdIngreso", "ProductoId"),
	FOREIGN KEY("ProductoId") REFERENCES Productos("IdProd"),
	FOREIGN KEY("IdRecDoc") REFERENCES Documento_Recepcion("IdDocRec")
);

