from views.cliente import CrudClients
from views.menu import Menu
from views.producto import CrudProducts
from views.venta import CrudSales
from utils.formatters import borrarPantalla, mostrar_advertencia, panel, pausar


def _menu_clientes():
    while True:
        panel("SISTEMA DE FACTURACION", "Modulo de clientes")
        opcion = Menu(
            "CLIENTES",
            [
                "1) Registrar cliente",
                "2) Actualizar cliente",
                "3) Eliminar cliente",
                "4) Consultar clientes",
                "5) Volver al inicio",
            ],
        ).menu()

        if opcion == "1":
            CrudClients.create()
        elif opcion == "2":
            CrudClients.update()
        elif opcion == "3":
            CrudClients.delete()
        elif opcion == "4":
            CrudClients.consult()
        elif opcion == "5":
            return
        else:
            mostrar_advertencia("Opcion no valida.")
            pausar()


def _menu_productos():
    while True:
        panel("SISTEMA DE FACTURACION", "Modulo de productos")
        opcion = Menu(
            "PRODUCTOS",
            [
                "1) Registrar producto",
                "2) Actualizar producto",
                "3) Eliminar producto",
                "4) Consultar productos",
                "5) Volver al inicio",
            ],
        ).menu()

        if opcion == "1":
            CrudProducts.create()
        elif opcion == "2":
            CrudProducts.update()
        elif opcion == "3":
            CrudProducts.delete()
        elif opcion == "4":
            CrudProducts.consult()
        elif opcion == "5":
            return
        else:
            mostrar_advertencia("Opcion no valida.")
            pausar()


def _menu_ventas():
    ventas = CrudSales()
    while True:
        panel("SISTEMA DE FACTURACION", "Modulo de ventas")
        opcion = Menu(
            "VENTAS Y FACTURAS",
            [
                "1) Crear factura",
                "2) Consultar facturas",
                "3) Modificar factura",
                "4) Eliminar factura",
                "5) Volver al inicio",
            ],
        ).menu()

        if opcion == "1":
            ventas.create()
        elif opcion == "2":
            ventas.consult()
        elif opcion == "3":
            ventas.update()
        elif opcion == "4":
            ventas.delete()
        elif opcion == "5":
            return
        else:
            mostrar_advertencia("Opcion no valida.")
            pausar()


def run():
    while True:
        panel("SISTEMA DE FACTURACION CLI", "Clientes | Productos | Ventas")
        opcion = Menu(
            "MENU PRINCIPAL",
            [
                "1) Gestionar clientes",
                "2) Gestionar productos",
                "3) Ventas y facturas",
                "4) Salir",
            ],
        ).menu()

        if opcion == "1":
            _menu_clientes()
        elif opcion == "2":
            _menu_productos()
        elif opcion == "3":
            _menu_ventas()
        elif opcion == "4":
            borrarPantalla()
            print("Gracias por usar el sistema de facturacion.")
            return
        else:
            mostrar_advertencia("Opcion no valida.")
            pausar()
