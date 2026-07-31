from services.cliente_service import ICrud
from storage.file_manager import data_path
from storage.json_storage import JsonFile
from utils.formatters import (
    confirmar,
    formatear_dinero,
    input_decimal,
    input_entero,
    input_texto,
    mostrar_advertencia,
    mostrar_error,
    mostrar_exito,
    panel,
    pausar,
    seccion,
    tabla,
)


class CrudProducts(ICrud):
    archivo = JsonFile(data_path("productos.json"))

    @staticmethod
    def _listar():
        return CrudProducts.archivo.read()

    @staticmethod
    def _guardar(productos):
        CrudProducts.archivo.save(productos)

    @staticmethod
    def _buscar_por_id(productos, producto_id):
        return next((item for item in productos if item.get("id") == producto_id), None)

    @staticmethod
    def _mostrar_tabla(productos):
        filas = [
            [
                producto.get("id", ""),
                producto.get("descripcion", ""),
                formatear_dinero(producto.get("precio", 0)),
                producto.get("stock", 0),
            ]
            for producto in productos
        ]
        tabla(["ID", "Producto", "Precio", "Stock"], filas, [6, 28, 12, 8])

    @staticmethod
    def create():
        panel("PRODUCTOS", "Registro de nuevo producto")
        productos = CrudProducts._listar()
        CrudProducts._mostrar_tabla(productos)
        seccion("Datos del producto")

        descripcion = input_texto("Descripcion").title()
        existente = next(
            (item for item in productos if item.get("descripcion", "").lower() == descripcion.lower()),
            None,
        )

        if existente:
            mostrar_advertencia("El producto ya existe.")
            if not confirmar("Desea actualizarlo"):
                pausar()
                return
            producto = existente
        else:
            ultimo_id = max([item.get("id", 0) for item in productos], default=0)
            producto = {"id": ultimo_id + 1}
            productos.append(producto)

        producto["descripcion"] = descripcion
        producto["precio"] = input_decimal("Precio")
        producto["stock"] = input_entero("Stock")

        CrudProducts._guardar(productos)
        mostrar_exito("Producto guardado correctamente.")
        pausar()

    @staticmethod
    def update():
        panel("PRODUCTOS", "Actualizar producto")
        productos = CrudProducts._listar()
        CrudProducts._mostrar_tabla(productos)
        seccion("Busqueda")

        producto_id = input_entero("ID del producto")
        producto = CrudProducts._buscar_por_id(productos, producto_id)
        if not producto:
            mostrar_error("Producto no encontrado.")
            pausar()
            return

        seccion("Nuevos datos")
        descripcion = input_texto(f"Descripcion [{producto.get('descripcion')}]", requerido=False)
        precio = input_decimal(f"Precio [{producto.get('precio')}]", requerido=False)
        stock = input_entero(f"Stock [{producto.get('stock')}]", requerido=False)

        if descripcion:
            producto["descripcion"] = descripcion.title()
        if precio is not None:
            producto["precio"] = precio
        if stock is not None:
            producto["stock"] = stock

        CrudProducts._guardar(productos)
        mostrar_exito("Producto actualizado correctamente.")
        pausar()

    @staticmethod
    def delete():
        panel("PRODUCTOS", "Eliminar producto")
        productos = CrudProducts._listar()
        CrudProducts._mostrar_tabla(productos)
        seccion("Busqueda")

        producto_id = input_entero("ID del producto")
        producto = CrudProducts._buscar_por_id(productos, producto_id)
        if not producto:
            mostrar_error("Producto no encontrado.")
            pausar()
            return

        print(f"Producto: {producto.get('descripcion')} - {formatear_dinero(producto.get('precio', 0))}")
        if confirmar("Desea eliminar este producto"):
            productos = [item for item in productos if item.get("id") != producto_id]
            CrudProducts._guardar(productos)
            mostrar_exito("Producto eliminado correctamente.")
        else:
            mostrar_advertencia("Operacion cancelada.")
        pausar()

    @staticmethod
    def consult():
        panel("PRODUCTOS", "Consulta de productos")
        productos = CrudProducts._listar()
        CrudProducts._mostrar_tabla(productos)
        seccion("Filtro opcional")

        producto_id = input_entero("Buscar por ID o Enter para volver", requerido=False)
        if producto_id is not None:
            producto = CrudProducts._buscar_por_id(productos, producto_id)
            if producto:
                CrudProducts._mostrar_tabla([producto])
            else:
                mostrar_error("Producto no encontrado.")
        pausar()
