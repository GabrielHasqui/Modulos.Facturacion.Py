from services.cliente_service import ICrud
from storage.file_manager import data_path
from storage.json_storage import JsonFile
from utils.formatters import (
    confirmar,
    input_texto,
    mostrar_advertencia,
    mostrar_error,
    mostrar_exito,
    panel,
    pausar,
    seccion,
    tabla,
)


class CrudClients(ICrud):
    archivo = JsonFile(data_path("clientes.json"))

    @staticmethod
    def _listar():
        return CrudClients.archivo.read()

    @staticmethod
    def _guardar(clientes):
        CrudClients.archivo.save(clientes)

    @staticmethod
    def _buscar_por_dni(dni):
        for cliente in CrudClients._listar():
            if cliente.get("dni") == dni:
                return cliente
        return None

    @staticmethod
    def _mostrar_tabla(clientes):
        filas = []
        for cliente in clientes:
            valor = cliente.get("valor", 0)
            tipo = "VIP" if isinstance(valor, (int, float)) and valor > 1 else "Regular"
            beneficio = f"Cupo {valor}" if tipo == "VIP" else f"{float(valor) * 100:.0f}% desc."
            filas.append([
                cliente.get("dni", ""),
                cliente.get("nombre", ""),
                cliente.get("apellido", ""),
                tipo,
                beneficio,
            ])
        tabla(["DNI", "Nombre", "Apellido", "Tipo", "Beneficio"], filas, [14, 16, 16, 10, 14])

    @staticmethod
    def create():
        panel("CLIENTES", "Registro de nuevo cliente")
        seccion("Datos del cliente")

        dni = input_texto("DNI")
        if CrudClients._buscar_por_dni(dni):
            mostrar_error("Ya existe un cliente registrado con ese DNI.")
            pausar()
            return

        nombre = input_texto("Nombre").title()
        apellido = input_texto("Apellido").title()
        tipo = input_texto("Tipo de cliente [1 Regular / 2 VIP]")

        if tipo == "2":
            valor = 10000
        else:
            tiene_descuento = confirmar("El cliente tiene tarjeta de descuento")
            valor = 0.10 if tiene_descuento else 0

        clientes = CrudClients._listar()
        clientes.append({"dni": dni, "nombre": nombre, "apellido": apellido, "valor": valor})
        CrudClients._guardar(clientes)
        mostrar_exito("Cliente registrado correctamente.")
        pausar()

    @staticmethod
    def update():
        panel("CLIENTES", "Actualizar informacion")
        clientes = CrudClients._listar()
        CrudClients._mostrar_tabla(clientes)
        seccion("Busqueda")

        dni = input_texto("DNI del cliente")
        cliente = next((item for item in clientes if item.get("dni") == dni), None)
        if not cliente:
            mostrar_error("Cliente no encontrado.")
            pausar()
            return

        seccion("Nuevos datos")
        nuevo_nombre = input_texto(f"Nombre [{cliente.get('nombre')}]", requerido=False)
        nuevo_apellido = input_texto(f"Apellido [{cliente.get('apellido')}]", requerido=False)

        if nuevo_nombre:
            cliente["nombre"] = nuevo_nombre.title()
        if nuevo_apellido:
            cliente["apellido"] = nuevo_apellido.title()

        CrudClients._guardar(clientes)
        mostrar_exito("Cliente actualizado correctamente.")
        pausar()

    @staticmethod
    def delete():
        panel("CLIENTES", "Eliminar cliente")
        clientes = CrudClients._listar()
        CrudClients._mostrar_tabla(clientes)
        seccion("Busqueda")

        dni = input_texto("DNI del cliente")
        cliente = next((item for item in clientes if item.get("dni") == dni), None)
        if not cliente:
            mostrar_error("Cliente no encontrado.")
            pausar()
            return

        print(f"Cliente: {cliente.get('nombre')} {cliente.get('apellido')}")
        if confirmar("Desea eliminar este cliente"):
            clientes = [item for item in clientes if item.get("dni") != dni]
            CrudClients._guardar(clientes)
            mostrar_exito("Cliente eliminado correctamente.")
        else:
            mostrar_advertencia("Operacion cancelada.")
        pausar()

    @staticmethod
    def consult():
        panel("CLIENTES", "Consulta de clientes")
        clientes = CrudClients._listar()
        CrudClients._mostrar_tabla(clientes)
        seccion("Filtro opcional")

        dni = input_texto("Buscar por DNI o Enter para volver", requerido=False)
        if dni:
            cliente = CrudClients._buscar_por_dni(dni)
            if cliente:
                CrudClients._mostrar_tabla([cliente])
            else:
                mostrar_error("Cliente no encontrado.")
        pausar()
