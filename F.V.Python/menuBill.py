from components import Menu,Valida
from utilities import borrarPantalla,gotoxy,dibujar_cuadro
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient,VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce
import platform

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create():
        borrarPantalla()
        dibujar_cuadro()
        gotoxy(2, 1)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(70, 2)
        print(blue_color + "Registro de Cliente")
        gotoxy(2, 3)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(2, 4)
        print(blue_color + "Empresa:"+ purple_color +" Corporación el Rosado ")
        gotoxy(60, 4)
        print( blue_color + "RUC:" + purple_color + "1790097870001")
        gotoxy(2, 5)
        print(blue_color + "Seleccione el tipo de cliente:")
        gotoxy(2, 6)
        print(blue_color + "1)" + purple_color +" Cliente Regular")
        gotoxy(2, 7)
        print(blue_color + "2)" + purple_color + " Cliente VIP")
        gotoxy(2, 8)
        print(blue_color + "Seleccione una opción: ")
        gotoxy(25, 8)
        tipo_cliente = input( purple_color)
        gotoxy(2, 9)
        print(green_color + "=" * 166 + reset_color)
        if tipo_cliente not in {"1", "2"}:
            print("Opción inválida")
            return

        cliente_tipo = "Regular" if tipo_cliente == "1" else "VIP"
        gotoxy(2, 10)
        print(purple_color + f"Cliente {cliente_tipo}")
        nombre = Valida.validar_letras("Ingresa el nombre del cliente: ",2,10,33,10)
        apellido = Valida.validar_letras("Ingresa el apellido del cliente: ",2,11,35,11)
        dni = Valida.validar_dni("Ingrese el DNI del cliente: ",2,12,30,12)

        if tipo_cliente == "1":
            gotoxy(2, 13)
            print(blue_color + "¿El cliente tiene tarjeta de descuento? (s/n): ")
            gotoxy(49, 13)
            card = input(purple_color).lower() == "s"
            cliente = RegularClient(nombre, apellido, dni, card)
        else:
            cliente = VipClient(nombre, apellido, dni)

        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()
        clients.append(cliente.getJson())
        json_file.save(clients)
        gotoxy(2, 14)
        gotoxy(2, 15)
        print( blue_color + "Cliente registrado exitosamente!")
        gotoxy(2, 16)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(2, 17)
        # Agregar una pausa antes de salir del programa
        gotoxy(2, 18)
        if platform.system() == 'Windows':
            input(blue_color + "Presiona Enter para salir...")
        else:
            time.sleep(3)

    def update():
        borrarPantalla()
        dibujar_cuadro()
        gotoxy(2, 1)
        print(green_color + "=" * 166)
        gotoxy(70, 2)
        print(blue_color + "Actualización de Cliente")
        gotoxy(2, 3)
        print(green_color + "=" * 166)
        gotoxy(2, 4)
        print(blue_color + "Empresa: " + purple_color + "Corporación el Rosado")
        gotoxy(60, 4)
        print(blue_color + "RUC:" + purple_color + "1790097870001")
        gotoxy(2, 5)
        gotoxy(2, 6)
        dni = Valida.validar_dni("Ingrese el DNI del cliente: ", 2, 6, 30, 6)
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()

        found = False
        updated_clients = []
        for client in clients:
            if client['dni'] == dni:
                found = True
                gotoxy(2, 7)
                print(green_color + "=" * 166)
                gotoxy(2, 8)
                print(blue_color + f"Cliente encontrado:")
                gotoxy(2, 9)
                print(blue_color + f" Nombre: " + purple_color + f"{client['nombre']}")
                print(blue_color + f" Apellido:" + purple_color + f"{client['apellido']}")
                print(blue_color + f" DNI:" + purple_color + f"{client['dni']}\n")
                gotoxy(2, 12)
                print(green_color + "=" * 166)

                new_nombre = input(blue_color + f"Ingrese el nuevo nombre del cliente (deje en blanco para mantener el mismo): " + purple_color)
                new_apellido = input(blue_color + f"Ingrese el nuevo apellido del cliente (deje en blanco para mantener el mismo): " + purple_color)

                if new_nombre:
                    client['nombre'] = new_nombre
                if new_apellido:
                    client['apellido'] = new_apellido
            updated_clients.append(client)

        if found:
            # Guardar los cambios en el archivo JSON
            json_file.save(updated_clients)
            gotoxy(2, 15)
            print(green_color + "=" * 166)
            gotoxy(2, 16)
            print(blue_color + "Cliente actualizado exitosamente!")
        else:
            gotoxy(2, 9)
            print(green_color + "=" * 166)
            gotoxy(2, 10)
            print(blue_color + "Cliente no encontrado.")
        
        gotoxy(2, 17)
        # Agregar una pausa antes de salir del programa
        if platform.system() == 'Windows':
            input(blue_color + f"  Presiona Enter para salir...")
        else:
            time.sleep(3)
            
    def delete():
        borrarPantalla()
        dibujar_cuadro()
        gotoxy(2, 1)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(70, 2)
        print(blue_color + "Eliminación de Cliente")
        gotoxy(2, 3)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(2, 4)
        print(blue_color + "Empresa: " + purple_color + "Corporación el Rosado")
        gotoxy(60, 4)
        print(blue_color + "RUC:" + purple_color + "1790097870001")
        gotoxy(2, 5)
        gotoxy(2, 6)
        dni = Valida.validar_dni("Ingrese el DNI del cliente que desea eliminar: ", 2, 6, 49, 6)
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()

        # Buscar el cliente por su DNI
        found = False
        client_to_delete = None
        for client in clients:
            if client['dni'] == dni:
                found = True
                client_to_delete = client
                break

        if found:
            gotoxy(2, 8)
            print(blue_color + "Información del cliente a eliminar:")
            print(reset_color)
            gotoxy(2, 11)
            print(blue_color + "Nombre:" + purple_color + f"{client_to_delete['nombre']}")
            gotoxy(2, 12)
            print(blue_color + "Apellido:" + purple_color + f"{client_to_delete['apellido']}")
            gotoxy(2, 13)
            print(blue_color + "DNI:" + purple_color + f"{client_to_delete['dni']}")
            gotoxy(2, 14)
            print(green_color + "=" * 166 + reset_color)

            # Confirmar la eliminación
            confirmacion = input(blue_color + "¿Estás seguro de que deseas eliminar este cliente? (s/n): " + purple_color)
            if confirmacion.lower() == 's':
                # Filtrar clientes
                filtered_clients = [client for client in clients if client['dni'] != dni]
                json_file.save(filtered_clients)
                gotoxy(2, 18)
                print(green_color + "=" * 90)
                gotoxy(2, 19)
                print(blue_color + "Cliente eliminado exitosamente!")
            else:
                gotoxy(2, 14)
                print(green_color + "=" * 166 + reset_color)
                print(reset_color)
                gotoxy(2, 15)
                print(blue_color + "Operación cancelada.")
        else:
            gotoxy(2, 8)
            print(green_color + "=" * 166 + reset_color)
            print(reset_color)
            gotoxy(2, 9)
            print(blue_color +"Cliente no encontrado.")

        # Agregar una pausa antes de salir del programa
        if platform.system() == 'Windows':
            input(blue_color + "Presiona Enter para salir...")
        else:
            time.sleep(3)

    def consult():
        borrarPantalla()
        dibujar_cuadro()
        gotoxy(2, 1)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(70, 2)
        print(blue_color + "Consulta de Cliente")
        gotoxy(2, 3)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(2, 4)
        print(blue_color + "Empresa: " + purple_color + "Corporación el Rosado")
        gotoxy(60, 4)
        print(blue_color + "RUC:" + purple_color + "1790097870001")
        gotoxy(2, 6)
        dni = Valida.validar_dni("Ingrese el DNI del cliente que desea consultar: ", 2, 6, 49, 6)
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.find("dni", dni)

        if clients:
            client = clients[0]
            gotoxy(2, 8)
            print(green_color + "=" * 166 + reset_color)
            gotoxy(2, 9)
            print(blue_color + "Información del cliente:")
            gotoxy(2, 10)
            print(blue_color + "Nombre: "+ purple_color +f"{client['nombre']}")
            gotoxy(2, 11)
            print(blue_color + "Apellido: "+ purple_color +f"{client['apellido']}")
            gotoxy(2, 12)
            print(blue_color + "DNI: "+ purple_color +f"{client['dni']}")
            gotoxy(2, 13)
            print(green_color + "=" * 166 + reset_color)
        else:
            gotoxy(2, 8)
            print(green_color + "=" * 166 + reset_color)
            gotoxy(2, 9)
            print("Cliente no encontrado.")
        gotoxy(3, 15)
        input(blue_color + "Presione una tecla para continuar...")

class CrudProducts(ICrud):
    def create():
        borrarPantalla()
        dibujar_cuadro()
        gotoxy(2, 1)
        print(green_color + "=" * 166)
        gotoxy(70, 2)
        print(blue_color + "Registro de Producto")
        gotoxy(2, 3)
        print(green_color + "=" * 166)
        gotoxy(2, 4)
        print(blue_color + "Empresa: " + purple_color + "Corporación el Rosado")
        gotoxy(60, 4)
        print(blue_color + "RUC:" + purple_color + "1790097870001")
        gotoxy(2, 6)
        descrip = Valida.validar_letras("Ingrese la descripción del producto: ", 2, 6, 39, 6)
        preci = float(Valida.validar_numeros_decimales("Ingrese el precio del producto: ", 2, 7, 33, 7))
        stock = int(Valida.validar_numeros("Ingrese el stock del producto: ", 2, 8, 32, 8))
        
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()
        
        last_id = max([product['id'] for product in products]) if products else 0
        
        existing_product = next((product for product in products if product['descripcion'] == descrip), None)
        
        if existing_product:
            gotoxy(2, 8)
            print(blue_color + "El producto ya existe:")
            gotoxy(2, 9)
            print(f"ID: {existing_product['id']}, Descripción: {existing_product['descripcion']}, Precio: {existing_product['precio']}, Stock: {existing_product['stock']}")
            actualizar = input(blue_color + "¿Desea actualizar este producto? (s/n): " + purple_color).lower()
            if actualizar == 's':
                # Actualizar el producto existente
                id_producto = existing_product['id']
                descrip_nueva = Valida.validar_letras(f"Ingrese la nueva descripción del producto (actual: {existing_product['descripcion']}): ", 2, 10, 64, 10)
                preci_nuevo = float(Valida.validar_numeros_decimales(f"Ingrese el nuevo precio del producto (actual: {existing_product['precio']}): ", 2, 11, 54, 11))
                stock_nuevo = int(Valida.validar_numeros(f"Ingrese el nuevo stock del producto (actual: {existing_product['stock']}): ", 2, 12, 52, 12))
                
                existing_product['descripcion'] = descrip_nueva if descrip_nueva else existing_product['descripcion']
                existing_product['precio'] = preci_nuevo if preci_nuevo else existing_product['precio']
                existing_product['stock'] = stock_nuevo if stock_nuevo else existing_product['stock']
                
                json_file.save(products)
                gotoxy(2, 16)
                print(green_color + "=" * 166)
                gotoxy(2, 17)
                print(blue_color + "Producto actualizado exitosamente!")
            else:
                gotoxy(2, 14)
                print(green_color + "=" * 166)
                gotoxy(2, 15)
                print(blue_color + "Registro cancelado.")
        else:
            new_id = last_id + 1
            new_product = Product(id=new_id, descrip=descrip, preci=preci, stock=stock)
            products.append(new_product.getJson())
            json_file.save(products)
            gotoxy(2, 10)
            print(green_color + "=" * 166)
            gotoxy(2, 11)
            print(blue_color + f"Producto registrado exitosamente!")
        if platform.system() == 'Windows':
            input(blue_color + f"Presiona Enter para salir...")
        else:
            time.sleep(3)
    
    def update():
        borrarPantalla()
        dibujar_cuadro()
        gotoxy(2, 1)
        print(green_color + "=" * 166)
        gotoxy(70, 2)
        print(blue_color + "Actualización de Producto")
        gotoxy(2, 3)
        print(green_color + "=" * 166)
        gotoxy(2, 4)
        print(blue_color + "Empresa: " + purple_color + "Corporación el Rosado")
        gotoxy(60, 4)
        print(blue_color + "RUC:" + purple_color + "1790097870001")
        gotoxy(2, 6)
        
        id_producto = int(Valida.validar_numeros("Ingrese el ID del producto que desea actualizar: ", 2, 6, 50, 6))
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()
        
        found = False
        updated_products = []
        for product in products:
            if product['id'] == id_producto:
                found = True
                gotoxy(2, 8)
                print(blue_color + "Detalles del producto a actualizar:")
                gotoxy(2, 9)
                print(blue_color + "ID:" + purple_color + f"{product['id']}, " + blue_color + "Descripción:" + purple_color + f" {product['descripcion']}, " + blue_color + "Precio:" + purple_color + f" {product['precio']}, " + blue_color + "Stock:" + purple_color + f" {product['stock']}")

                descrip = Valida.validar_letras(f"Ingrese la nueva descripción del producto (actual: {product['descripcion']}): ", 2, 11,  62, 11)
                preci = float(Valida.validar_numeros_decimales(f"Ingrese el nuevo precio del producto (actual: {product['precio']}): ", 2, 12, 54, 12))
                stock = int(Valida.validar_numeros(f"Ingrese el nuevo stock del producto (actual: {product['stock']}): ", 2, 13, 54, 13))
                # Actualizar la información si se proporcionó
                product['descripcion'] = descrip if descrip else product['descripcion']
                product['precio'] = preci if preci else product['precio']
                product['stock'] = stock if stock else product['stock']
            updated_products.append(product)

        if found:
            json_file.save(updated_products)
            gotoxy(2, 15)
            print(green_color + "=" * 166)
            gotoxy(2, 16)
            print(blue_color + "Producto actualizado exitosamente!")
        else:
            gotoxy(2, 15)
            print(green_color + "=" * 166)
            gotoxy(2, 16)
            print(blue_color + "Producto no encontrado.")
        if platform.system() == 'Windows':
            input(blue_color + "Presiona Enter para salir...")
        else:
            time.sleep(3)
            
    def delete():
        borrarPantalla()
        dibujar_cuadro()
        gotoxy(2, 1)
        print(green_color + "=" * 166)
        gotoxy(70, 2)
        print(blue_color + "Eliminación de Producto")
        gotoxy(2, 3)
        print(green_color + "=" * 166)
        gotoxy(2, 4)
        print(blue_color + "Empresa: " + purple_color + "Corporación el Rosado")
        gotoxy(60, 4)
        print(blue_color + "RUC:" + purple_color + "1790097870001")
        gotoxy(2, 6)
        
        id_producto = int(Valida.validar_numeros("Ingrese el ID del producto que desea eliminar: ", 2, 6, 48, 6))
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        found_product = None
        for product in products:
            if product['id'] == id_producto:
                found_product = product
                break

        if found_product:
            gotoxy(2, 8)
            print(green_color + "=" * 166)
            gotoxy(2, 9)
            print(blue_color + "Producto a eliminar:")
            gotoxy(2, 10)
            print(blue_color + f"ID: {purple_color}{found_product['id']}{blue_color}, Descripción: {purple_color}{found_product['descripcion']}{blue_color}, Precio: {purple_color}{found_product['precio']}{blue_color}, Stock: {purple_color}{found_product['stock']}")
            confirmacion = Valida.validar_letras(blue_color + "¿Está seguro de que desea eliminar este producto? (s/n): ", 2, 11, 58, 11).lower()
            if confirmacion == 's':
                filtered_products = [p for p in products if p['id'] != id_producto]
                json_file.save(filtered_products)
                gotoxy(2, 12)
                print(green_color + "=" * 166)
                gotoxy(2, 13)
                print(blue_color + "Producto eliminado exitosamente!")
            else:
                gotoxy(2, 12)
                print(green_color + "=" * 166)
                gotoxy(2, 13)
                print(blue_color + "Eliminación cancelada.")
        else:
            gotoxy(2, 8)
            print(green_color + "=" * 166)
            gotoxy(2, 9)
            print(blue_color + "Producto no encontrado.")
        time.sleep(2)
        
        if platform.system() == 'Windows':
            input(blue_color + "Presiona Enter para salir...")
        else:
            time.sleep(3)

    def consult():
        borrarPantalla()
        dibujar_cuadro()
        gotoxy(2, 1)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(70, 2)
        print(blue_color + "Consulta de Productos")
        gotoxy(2, 3)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(2, 4)
        print(blue_color + "Empresa:"+ purple_color + f"Corporación el Rosado" )
        gotoxy(60, 4)
        print(blue_color + "RUC:" + purple_color + "1790097870001")
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        if products:
            id_producto = Valida.validar_numeros("Ingrese el ID del producto que desea consultar: ", 2, 6, 50, 6)
            found = False
            for product in products:
                if product['id'] == int(id_producto):
                    found = True
                    gotoxy(2, 8)
                    print(green_color + "=" * 166)
                    gotoxy(2, 9)
                    print(blue_color + "Producto encontrado:")
                    gotoxy(2, 10)
                    print(blue_color + "ID: "+ purple_color + f"{product['id']}")
                    gotoxy(2, 11)
                    print(blue_color + "Descripción: "+ purple_color + f"{product['descripcion']}")
                    gotoxy(2, 12)
                    print(blue_color + "Precio: " + purple_color + f"{product['precio']}")
                    gotoxy(2, 13)
                    print(blue_color + "Stock: "+ purple_color +f"{product['stock']}")
                    gotoxy(2, 14)
                    print(green_color + "=" * 166)
                    gotoxy(2, 15)
                    break
            if not found:
                gotoxy(2, 8)
                print(blue_color + "Producto no encontrado.")
        else:
            gotoxy(2, 8)
            print(blue_color + "No hay productos registrados.")

        if platform.system() == 'Windows':
            input(blue_color + "Presiona Enter para salir...")
        else:
            time.sleep(3)

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2) 
           
    def update(self):
        path = os.path.dirname(os.path.abspath(__file__))
        while True:
            borrarPantalla()
            gotoxy(2, 1)
            print(green_color + "=" * 166 + reset_color)
            gotoxy(70, 2)
            print(blue_color + "Actualización de Venta")
            gotoxy(2, 3)
            print(green_color + "=" * 166 + reset_color)
            gotoxy(2, 4)
            print(blue_color + "Empresa: " + purple_color + "Corporación el Rosado")
            gotoxy(60, 4)
            print(blue_color + "RUC:" + purple_color + "1790097870001")
            gotoxy(2, 5)
            invoice_number = Valida.validar_numeros("Ingrese el número de factura que desea actualizar: ", 2, 6, 53, 6)
            invoice_number = int(invoice_number)
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.read()

            if invoices:
                # Buscar la factura específica
                for invoice in invoices:
                    if invoice["factura"] == invoice_number:
                        while True:
                            borrarPantalla()
                            gotoxy(2, 1)
                            print(green_color + "=" * 166 + reset_color)
                            gotoxy(70, 2)
                            print(blue_color + "Actualización de Venta")
                            gotoxy(2, 3)
                            print(green_color + "=" * 166 + reset_color)
                            gotoxy(2, 4)
                            print(blue_color + "Empresa: " + purple_color + "Corporación el Rosado")
                            gotoxy(60, 4)
                            print(blue_color + "RUC:" + purple_color + "1790097870001")
                            gotoxy(2, 5)
                            gotoxy(2, 7)
                            print(green_color + "=" * 166 + reset_color)
                            gotoxy(2, 8)
                            print(blue_color + "Número de Factura: " + purple_color + f"{invoice['factura']}")
                            print(blue_color + "Fecha:" + purple_color + f"{invoice['Fecha']}")
                            print(blue_color + "Cliente:" + purple_color + f"{invoice['cliente']}")
                            print(blue_color + "Total:" + purple_color + f"{invoice['total']}")
                            gotoxy(2, 12)
                            print("\nDetalle de la Venta:")
                            detalles = invoice['detalle']
                            print(f"{blue_color +'num'.center(5)} {blue_color + 'Producto'.center(28)} {blue_color + 'Cantidad'.center(10)} {blue_color + 'Precio'.center(10)}")
                            for i, detalle in enumerate(detalles, start=1):
                                print(purple_color + f" {i}) {detalle['poducto'].center(28)} {str(detalle['cantidad']).center(10)}  {str(detalle['precio']).center(10)}")
                            print(green_color + "=" * 166 + reset_color)
                            gotoxy(2, 20), print(blue_color + "\nOpciones:")
                            print("1. Modificar cantidad de un producto")
                            print("2. Eliminar un producto")
                            print("3. Agregar un nuevo producto")
                            print("4. Terminar actualización")
                            option = Valida.validar_numeros("Seleccione una opción: ", 2, 26, 25, 26)

                            if option == "1":
                                # Modificar cantidad de un producto en la factura
                                detalle_index = int(Valida.validar_numeros("Ingrese el número de línea del detalle que desea modificar: ", 2, 27, 62, 27)) - 1
                                if 0 <= detalle_index < len(detalles):
                                    new_quantity = int(Valida.validar_numeros("Ingrese la nueva cantidad: ", 2, 28, 29, 28))
                                    detalles[detalle_index]['cantidad'] = new_quantity
                                    # Recalcular el total de la factura
                                    invoice['total'] = sum(item['cantidad'] * item['precio'] for item in detalles)
                                    print(green_color + "=" * 166 + reset_color)
                                    gotoxy(4, 30)
                                    print(blue_color + "Cantidad modificada correctamente.")
                                    gotoxy(4, 31)
                                    input("Presione Enter para continuar...")
                                else:
                                    print("Número de línea inválido.")
                                    input("Presione Enter para continuar...")
                            elif option == "2":
                                # Eliminar un producto de la factura
                                detalle_index = int(Valida.validar_numeros("Ingrese el número de línea del detalle que desea eliminar: ",2, 27,62,27)) - 1
                                if 0 <= detalle_index < len(detalles):
                                    del detalles[detalle_index]
                                    # Recalcular el total de la factura
                                    invoice['total'] = sum(item['cantidad'] * item['precio'] for item in detalles)
                                    print(green_color + "=" * 166 + reset_color)
                                    gotoxy(3, 29)
                                    print(blue_color + "Producto eliminado correctamente.")
                                    gotoxy(4, 30)
                                    input("Presione Enter para continuar...")
                                else:
                                    print("Número de línea inválido.")
                                    input("Presione Enter para continuar...")
                            elif option == "3":
                                # Agregar un nuevo producto a la factura
                                product_id = int(Valida.validar_numeros("Ingrese el ID del nuevo producto: ", 2, 27, 35, 27))
                                product_quantity = int(Valida.validar_numeros("Ingrese la cantidad del nuevo producto: ", 2, 28, 42, 28))
                                json_file_products = JsonFile(path + '/archivos/products.json')
                                products = json_file_products.find("id", product_id)
                                if products:
                                    product = products[0]
                                    new_product = {
                                        'poducto': product['descripcion'],  # Modificar la clave aquí
                                        'precio': product['precio'],
                                        'cantidad': product_quantity
                                    }
                                    detalles.append(new_product)
                                    # Recalcular el total de la factura
                                    invoice['total'] = sum(item['cantidad'] * item['precio'] for item in detalles)
                                    print("Producto agregado correctamente.")
                                    input("Presione Enter para continuar...")
                                else:
                                    print("Producto no encontrado.")
                                    input("Presione Enter para continuar...")
                            elif option == "4":
                                print("Actualización de factura terminada.")
                                # Guardar los cambios en el archivo JSON
                                invoice['detalle'] = detalles
                                for index, inv in enumerate(invoices):
                                    if inv["factura"] == invoice_number:
                                        invoices[index] = invoice
                                        break
                                json_file.save(invoices)
                                break
                            else:
                                print("Opción inválida. Intente nuevamente.")
                                input("Presione Enter para continuar...")
            else:
                print("No hay facturas disponibles.")

            if platform.system() == 'Windows':
                input(blue_color + "Presiona Enter para salir...")
            else:
                time.sleep(3)

    def delete(self):
        borrarPantalla()
        dibujar_cuadro()
        gotoxy(2, 1)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(70, 2)
        print(blue_color + "Eliminación de Venta")
        gotoxy(2, 3)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(2, 4)
        print(blue_color + "Empresa:"+ purple_color + f"Corporación el Rosado" )
        gotoxy(60, 4)
        print(blue_color + "RUC:" + purple_color + "1790097870001")
        
        invoice_number = Valida.validar_numeros("Ingrese el número de factura que desea eliminar: ", 2, 6, 51, 6)
        invoice_number = int(invoice_number)
        
        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices = json_file.read()

        found = False
        updated_invoices = []
        for invoice in invoices:
            if invoice["factura"] == invoice_number:
                found = True

                gotoxy(2, 6)
                print("Factura encontrada:")
                gotoxy(2, 7)
                print(blue_color + "Número de Factura: "+ purple_color +f"{invoice['factura']}")
                gotoxy(2, 8)
                print(blue_color + "Fecha: " + purple_color + f"{invoice['Fecha']}")
                gotoxy(2, 9)
                print(blue_color + "Cliente: " + purple_color + f"{invoice['cliente']}")
                gotoxy(2, 10)
                print(blue_color + "Total: " + purple_color + f"{invoice['total']}")
                gotoxy(2, 12)
                print(blue_color + "Detalle de la Venta:")
                print(f" {'Producto'.center(20)}  {'Cantidad'.center(20)} {'Precio'.center(20)}")
                for i, detalle in enumerate(invoice['detalle'], start=1):
                    print(purple_color + f"{detalle['poducto'].center(20)} {str(detalle['cantidad']).center(20)}  {str(detalle['precio']).center(20)}")
                print(green_color + "=" * 90 + reset_color)

                confirmacion = input(blue_color + "¿Está seguro que desea eliminar esta factura? (s/n): " + purple_color).lower()
                if confirmacion == "s":
                    print("Factura eliminada exitosamente.")
                else:
                    print("Eliminación cancelada.")
            else:
                updated_invoices.append(invoice)

        if not found:
            print("Factura no encontrada.")

        json_file.save(updated_invoices)
        if platform.system() == 'Windows':
            input(blue_color + "Presiona Enter para salir...")
        else:
            time.sleep(3)
            
    def consult(self):
        borrarPantalla()
        dibujar_cuadro()
        gotoxy(2, 1)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(30, 2)
        print(blue_color + "Consulta de Venta")
        gotoxy(2, 3)
        print(green_color + "=" * 166 + reset_color)
        gotoxy(2, 4)
        print(blue_color + "Empresa:" + purple_color + "Corporación el Rosado")
        gotoxy(60, 4)
        print(blue_color + "RUC:" + purple_color + "1790097870001")
        gotoxy(2, 6)

        invoice_number = Valida.validar_numeros("Ingrese el número de factura: ", 2, 6, 33, 6)
        invoice_number = int(invoice_number)

        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices = json_file.read()

        found = False
        for invoice in invoices:
            if invoice["factura"] == invoice_number:
                found = True

                gotoxy(2, 8)
                print("Factura encontrada:")
                gotoxy(2, 9)
                print(blue_color + "Número de Factura: " + purple_color + f"{invoice['factura']}")
                gotoxy(2, 10)
                print(blue_color + "Fecha: " + purple_color + f"{invoice['Fecha']}")
                gotoxy(2, 11)
                print(blue_color + "Cliente: " + purple_color + f"{invoice['cliente']}")
                gotoxy(2, 12)
                print(blue_color + "Total: " + purple_color + f"{invoice['total']}")
                gotoxy(2, 14)
                print(blue_color + "Detalle de la Venta:")
                print(f" {'Producto'.center(20)}  {'Cantidad'.center(20)} {'Precio'.center(20)}")
                for detalle in invoice['detalle']:
                    print(purple_color + f"{detalle['poducto'].center(20)} {str(detalle['cantidad']).center(20)}  {str(detalle['precio']).center(20)}")
                print(green_color + "=" * 166 + reset_color)
                break

        if not found:
            gotoxy(2, 8)
            print("Factura no encontrada.")
        gotoxy(2, 16)
        input("Presione una tecla para continuar...")

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla() 
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)   
            opc1 = menu_clients.menu()
            if opc1 == "1":
                CrudClients.create()
            elif opc1 == "2":
                CrudClients.update()
            elif opc1 == "3":
                CrudClients.delete()
            elif opc1 == "4":
                CrudClients.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                CrudProducts.create()
            elif opc2 == "2":
                CrudProducts.update()
            elif opc2 == "3":
                CrudProducts.delete()
            elif opc2 == "4":
                CrudProducts.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
                
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

