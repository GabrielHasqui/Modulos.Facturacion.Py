# Sistema de Facturacion CLI

Sistema de facturacion por consola desarrollado en Python. Permite administrar clientes, productos y facturas usando archivos JSON como almacenamiento local.

## Caracteristicas

- Registro, consulta, actualizacion y eliminacion de clientes.
- Registro, consulta, actualizacion y eliminacion de productos.
- Creacion de ventas/facturas por consola.
- Calculo de subtotal, descuento, IVA y total.
- Persistencia de datos en archivos JSON.
- Interfaz de consola con menus, colores y formato de factura.

## Tecnologias

- Python
- JSON
- Programacion orientada a objetos
- Consola/terminal

## Estructura

```text
sistema-facturacion-cli/
|-- main.py
|-- README.md
|-- requirements.txt
|-- data/
|   |-- clientes.json
|   |-- productos.json
|   |-- facturas.json
|-- models/
|   |-- cliente.py
|   |-- producto.py
|   |-- factura.py
|-- services/
|   |-- cliente_service.py
|   |-- producto_service.py
|   |-- factura_service.py
|-- storage/
|   |-- file_manager.py
|   |-- json_storage.py
|-- utils/
|   |-- formatters.py
|   |-- validators.py
|-- views/
|   |-- menu.py
|   |-- cliente.py
|   |-- producto.py
|   |-- factura.py
|   |-- venta.py
```

## Instalacion

```bash
git clone https://github.com/GabrielHasqui/sistema-facturacion-cli.git
cd sistema-facturacion-cli
pip install -r requirements.txt
```

## Ejecucion

```bash
python main.py
```

## Datos

Los datos se almacenan en la carpeta `data/`:

- `clientes.json`
- `productos.json`
- `facturas.json`

## Objetivo del proyecto

Este proyecto busca demostrar conocimientos basicos de Python, programacion orientada a objetos, manejo de archivos, organizacion por carpetas y construccion de una aplicacion de consola con flujo de negocio real.

## Proximas mejoras

- Agregar pruebas con `pytest`.
- Exportar facturas a TXT o PDF.
- Mejorar reportes de ventas.
- Validar stock antes de facturar.
