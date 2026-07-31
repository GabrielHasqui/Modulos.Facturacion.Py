from datetime import date

from services.cliente_service import ICrud
from storage.file_manager import data_path
from storage.json_storage import JsonFile
from utils.formatters import (
    borrarPantalla,
    blue_color,
    confirmar,
    cyan_color,
    formatear_dinero,
    green_color,
    input_entero,
    input_texto,
    mostrar_advertencia,
    mostrar_error,
    mostrar_exito,
    panel,
    purple_color,
    pausar,
    red_color,
    reset_color,
    seccion,
    tabla,
    yellow_color,
)


IVA = 0.12


class CrudSales(ICrud):
    clientes_file = JsonFile(data_path("clientes.json"))
    productos_file = JsonFile(data_path("productos.json"))
    facturas_file = JsonFile(data_path("facturas.json"))

    @staticmethod
    def _clientes():
        return CrudSales.clientes_file.read()

    @staticmethod
    def _productos():
        return CrudSales.productos_file.read()

    @staticmethod
    def _facturas():
        return CrudSales.facturas_file.read()

    @staticmethod
    def _guardar_facturas(facturas):
        CrudSales.facturas_file.save(facturas)

    @staticmethod
    def _buscar_cliente(dni):
        return next((cliente for cliente in CrudSales._clientes() if cliente.get("dni") == dni), None)

    @staticmethod
    def _buscar_producto(producto_id):
        return next((producto for producto in CrudSales._productos() if producto.get("id") == producto_id), None)

    @staticmethod
    def _buscar_factura(numero):
        return next((factura for factura in CrudSales._facturas() if factura.get("factura") == numero), None)

    @staticmethod
    def _mostrar_productos():
        productos = CrudSales._productos()
        filas = [
            [p.get("id"), p.get("descripcion"), formatear_dinero(p.get("precio", 0)), p.get("stock", 0)]
            for p in productos
        ]
        tabla(["ID", "Producto", "Precio", "Stock"], filas, [6, 28, 12, 8])

    @staticmethod
    def _mostrar_facturas(facturas):
        filas = [
            [
                factura.get("factura"),
                factura.get("Fecha"),
                factura.get("cliente"),
                formatear_dinero(factura.get("total", 0)),
            ]
            for factura in facturas
        ]
        tabla(["Factura", "Fecha", "Cliente", "Total"], filas, [10, 14, 28, 14])

    @staticmethod
    def _linea(ancho=86):
        print(cyan_color + "-" * ancho + reset_color)

    @staticmethod
    def _caja(titulo, subtitulo="", ancho=86):
        print(cyan_color + "+" + "-" * (ancho - 2) + "+" + reset_color)
        print(cyan_color + "|" + reset_color + blue_color + titulo.center(ancho - 2) + reset_color + cyan_color + "|" + reset_color)
        if subtitulo:
            print(cyan_color + "|" + reset_color + purple_color + subtitulo.center(ancho - 2) + reset_color + cyan_color + "|" + reset_color)
        print(cyan_color + "+" + "-" * (ancho - 2) + "+" + reset_color)

    @staticmethod
    def _mostrar_productos_facturacion(productos):
        print(blue_color + "PRODUCTOS DISPONIBLES" + reset_color)
        CrudSales._linea()
        print(yellow_color + f"{'ID':<6}{'Producto':<30}{'Precio':>12}{'Stock':>10}" + reset_color)
        CrudSales._linea()
        for producto in productos:
            print(
                green_color + f"{producto.get('id', ''):<6}" + reset_color
                + f"{producto.get('descripcion', ''):<30}"
                + purple_color + f"{formatear_dinero(producto.get('precio', 0)):>12}" + reset_color
                + f"{producto.get('stock', 0):>10}"
            )
        CrudSales._linea()

    @staticmethod
    def _mostrar_detalle_facturacion(detalles):
        print(blue_color + "DETALLE ACTUAL" + reset_color)
        CrudSales._linea()
        print(yellow_color + f"{'#':<4}{'Producto':<30}{'Cant.':>8}{'Precio':>12}{'Total':>14}" + reset_color)
        CrudSales._linea()
        if not detalles:
            print(yellow_color + "No hay productos agregados." + reset_color)
        else:
            for indice, detalle in enumerate(detalles, start=1):
                nombre = detalle.get("producto", detalle.get("poducto", ""))
                precio = detalle.get("precio", 0)
                cantidad = detalle.get("cantidad", 0)
                print(
                    green_color + f"{indice:<4}" + reset_color
                    + f"{nombre:<30}"
                    + f"{cantidad:>8}"
                    + purple_color + f"{formatear_dinero(precio):>12}" + reset_color
                    + green_color + f"{formatear_dinero(precio * cantidad):>14}" + reset_color
                )
        CrudSales._linea()

    @staticmethod
    def _mostrar_resumen_facturacion(detalles, descuento_porcentaje):
        subtotal, descuento, iva, total = CrudSales._calcular_totales(detalles, descuento_porcentaje)
        print(blue_color + "RESUMEN" + reset_color)
        CrudSales._linea(42)
        print(f"{'Subtotal':<18}{purple_color}{formatear_dinero(subtotal):>20}{reset_color}")
        print(f"{'Descuento':<18}{purple_color}{formatear_dinero(descuento):>20}{reset_color}")
        print(f"{'IVA 12%':<18}{purple_color}{formatear_dinero(iva):>20}{reset_color}")
        CrudSales._linea(42)
        print(green_color + f"{'TOTAL':<18}{formatear_dinero(total):>20}" + reset_color)
        CrudSales._linea(42)

    @staticmethod
    def _input_en_caja(etiqueta, ancho=86, requerido=False):
        print(cyan_color + "+" + "-" * (ancho - 2) + "+" + reset_color)
        texto = f" {etiqueta}: "
        valor = input(cyan_color + "|" + reset_color + yellow_color + texto + reset_color).strip()
        print(cyan_color + "+" + "-" * (ancho - 2) + "+" + reset_color)
        if requerido and not valor:
            mostrar_error("Este campo es obligatorio.")
        return valor

    @staticmethod
    def _render_facturacion(nombre_cliente, detalles, descuento_porcentaje, mensaje=""):
        borrarPantalla()
        CrudSales._caja("NUEVA FACTURA", f"Cliente: {nombre_cliente}")
        print(f"Fecha: {date.today().strftime('%Y-%m-%d')}")
        print()
        CrudSales._mostrar_productos_facturacion(CrudSales._productos())
        print()
        CrudSales._mostrar_resumen_facturacion(detalles, descuento_porcentaje)
        print()
        CrudSales._mostrar_detalle_facturacion(detalles)
        print()
        print(blue_color + "AGREGAR PRODUCTO" + reset_color)
        CrudSales._linea(42)
        print("Ingrese el ID del producto para agregarlo.")
        print("Presione Enter sin escribir nada para terminar.")
        if mensaje:
            color = red_color if "no encontrado" in mensaje.lower() or "insuficiente" in mensaje.lower() else green_color
            print(color + f"Mensaje: {mensaje}" + reset_color)
        print()

    @staticmethod
    def _mostrar_detalle(factura):
        panel("FACTURA", f"Documento #{factura.get('factura')}")
        print(f"Fecha:   {factura.get('Fecha')}")
        print(f"Cliente: {factura.get('cliente')}")
        seccion("Detalle")

        filas = []
        for detalle in factura.get("detalle", []):
            nombre = detalle.get("producto", detalle.get("poducto", ""))
            precio = detalle.get("precio", 0)
            cantidad = detalle.get("cantidad", 0)
            filas.append([nombre, cantidad, formatear_dinero(precio), formatear_dinero(precio * cantidad)])
        tabla(["Producto", "Cant.", "Precio", "Subtotal"], filas, [28, 8, 12, 12])

        seccion("Resumen")
        print(f"Subtotal:  {formatear_dinero(factura.get('subtotal', 0))}")
        print(f"Descuento: {formatear_dinero(factura.get('descuento', 0))}")
        print(f"IVA:       {formatear_dinero(factura.get('iva', 0))}")
        print(f"TOTAL:     {formatear_dinero(factura.get('total', 0))}")

    @staticmethod
    def _calcular_totales(detalles, descuento_porcentaje):
        subtotal = round(sum(item["precio"] * item["cantidad"] for item in detalles), 2)
        descuento = round(subtotal * descuento_porcentaje, 2)
        iva = round((subtotal - descuento) * IVA, 2)
        total = round(subtotal - descuento + iva, 2)
        return subtotal, descuento, iva, total

    @staticmethod
    def _nueva_factura_numero():
        facturas = CrudSales._facturas()
        return max([factura.get("factura", 0) for factura in facturas], default=0) + 1

    def create(self):
        panel("VENTAS", "Nueva factura")
        seccion("Cliente")

        dni = input_texto("DNI del cliente")
        cliente = CrudSales._buscar_cliente(dni)
        if not cliente:
            mostrar_error("Cliente no encontrado. Registre el cliente antes de facturar.")
            pausar()
            return

        nombre_cliente = f"{cliente.get('nombre', '')} {cliente.get('apellido', '')}".strip()
        valor_cliente = cliente.get("valor", 0)
        descuento_porcentaje = valor_cliente if isinstance(valor_cliente, (int, float)) and 0 < valor_cliente <= 1 else 0

        detalles = []
        mensaje = ""
        while True:
            CrudSales._render_facturacion(nombre_cliente, detalles, descuento_porcentaje, mensaje)
            mensaje = ""
            producto_id_texto = CrudSales._input_en_caja("ID del producto o Enter para terminar")
            if not producto_id_texto:
                break
            if not producto_id_texto.isdigit():
                mensaje = "Ingrese un ID numerico."
                continue

            producto_id = int(producto_id_texto)

            producto = CrudSales._buscar_producto(producto_id)
            if not producto:
                mensaje = "Producto no encontrado."
                continue

            cantidad_texto = CrudSales._input_en_caja("Cantidad", requerido=True)
            if not cantidad_texto.isdigit() or int(cantidad_texto) <= 0:
                mensaje = "Ingrese una cantidad valida."
                continue
            cantidad = int(cantidad_texto)
            cantidad_actual = sum(
                item.get("cantidad", 0)
                for item in detalles
                if item.get("poducto") == producto.get("descripcion")
            )
            if cantidad + cantidad_actual > producto.get("stock", 0):
                mensaje = "Stock insuficiente para ese producto."
                continue

            detalle_existente = next(
                (item for item in detalles if item.get("poducto") == producto.get("descripcion")),
                None,
            )
            if detalle_existente:
                detalle_existente["cantidad"] += cantidad
                mensaje = "Cantidad actualizada en el detalle."
            else:
                detalles.append(
                    {
                        "poducto": producto.get("descripcion"),
                        "precio": producto.get("precio", 0),
                        "cantidad": cantidad,
                    }
                )
                mensaje = "Producto agregado a la factura."

        if not detalles:
            mostrar_advertencia("No se agregaron productos. Venta cancelada.")
            pausar()
            return

        subtotal, descuento, iva, total = CrudSales._calcular_totales(detalles, descuento_porcentaje)
        factura = {
            "factura": CrudSales._nueva_factura_numero(),
            "Fecha": date.today().strftime("%Y-%m-%d"),
            "cliente": nombre_cliente,
            "subtotal": subtotal,
            "descuento": descuento,
            "iva": iva,
            "total": total,
            "detalle": detalles,
        }

        CrudSales._mostrar_detalle(factura)
        if confirmar("Desea guardar esta factura"):
            facturas = CrudSales._facturas()
            facturas.append(factura)
            CrudSales._guardar_facturas(facturas)
            mostrar_exito("Factura guardada correctamente.")
        else:
            mostrar_advertencia("Venta cancelada.")
        pausar()

    def consult(self):
        panel("VENTAS", "Consulta de facturas")
        facturas = CrudSales._facturas()
        CrudSales._mostrar_facturas(facturas)
        seccion("Busqueda")

        numero = input_entero("Numero de factura o Enter para volver", requerido=False)
        if numero is None:
            return

        factura = next((item for item in facturas if item.get("factura") == numero), None)
        if factura:
            CrudSales._mostrar_detalle(factura)
        else:
            mostrar_error("Factura no encontrada.")
        pausar()

    def update(self):
        panel("VENTAS", "Modificar factura")
        facturas = CrudSales._facturas()
        CrudSales._mostrar_facturas(facturas)
        seccion("Busqueda")

        numero = input_entero("Numero de factura")
        factura = next((item for item in facturas if item.get("factura") == numero), None)
        if not factura:
            mostrar_error("Factura no encontrada.")
            pausar()
            return

        while True:
            CrudSales._mostrar_detalle(factura)
            seccion("Opciones")
            print("1) Cambiar cantidad")
            print("2) Eliminar producto")
            print("3) Agregar producto")
            print("4) Guardar y volver")
            opcion = input_texto("Seleccione")

            detalles = factura.get("detalle", [])
            if opcion == "1":
                linea = input_entero("Linea del producto") - 1
                if 0 <= linea < len(detalles):
                    detalles[linea]["cantidad"] = input_entero("Nueva cantidad")
                else:
                    mostrar_error("Linea no valida.")
                    pausar()
            elif opcion == "2":
                linea = input_entero("Linea del producto") - 1
                if 0 <= linea < len(detalles):
                    detalles.pop(linea)
                else:
                    mostrar_error("Linea no valida.")
                    pausar()
            elif opcion == "3":
                panel("VENTAS", "Agregar producto")
                CrudSales._mostrar_productos()
                producto_id = input_entero("ID del producto")
                producto = CrudSales._buscar_producto(producto_id)
                if producto:
                    detalles.append(
                        {
                            "poducto": producto.get("descripcion"),
                            "precio": producto.get("precio", 0),
                            "cantidad": input_entero("Cantidad"),
                        }
                    )
                else:
                    mostrar_error("Producto no encontrado.")
                    pausar()
            elif opcion == "4":
                subtotal, descuento, iva, total = CrudSales._calcular_totales(detalles, 0)
                factura["detalle"] = detalles
                factura["subtotal"] = subtotal
                factura["descuento"] = descuento
                factura["iva"] = iva
                factura["total"] = total
                CrudSales._guardar_facturas(facturas)
                mostrar_exito("Factura actualizada correctamente.")
                pausar()
                return
            else:
                mostrar_error("Opcion no valida.")
                pausar()

    def delete(self):
        panel("VENTAS", "Eliminar factura")
        facturas = CrudSales._facturas()
        CrudSales._mostrar_facturas(facturas)
        seccion("Busqueda")

        numero = input_entero("Numero de factura")
        factura = next((item for item in facturas if item.get("factura") == numero), None)
        if not factura:
            mostrar_error("Factura no encontrada.")
            pausar()
            return

        CrudSales._mostrar_detalle(factura)
        if confirmar("Desea eliminar esta factura"):
            facturas = [item for item in facturas if item.get("factura") != numero]
            CrudSales._guardar_facturas(facturas)
            mostrar_exito("Factura eliminada correctamente.")
        else:
            mostrar_advertencia("Operacion cancelada.")
        pausar()
