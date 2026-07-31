import os
import shutil

# Variables globales: Colores en formato ANSI escape code
reset_color = "\033[0m"
red_color = "\033[91m"
green_color = "\033[92m"
yellow_color = "\033[93m"
blue_color = "\033[94m"
purple_color = "\033[95m"
cyan_color = "\033[96m"

# funciones de usuario

def gotoxy(x, y):
    print("%c[%d;%df" % (0x1B, y, x), end="")

def borrarPantalla():
    os.system("cls" if os.name == "nt" else "clear")

def mensaje(msg, f=1, c=1):
    gotoxy(c, f)
    print(msg)

def dibujar_cuadro():
    terminal_size = shutil.get_terminal_size(fallback=(100, 30))
    ancho = max(40, terminal_size.columns - 2)
    alto = max(10, terminal_size.lines - 2)
    print(green_color + '+' + '-' * ancho + '+' + reset_color)
    for _ in range(alto):
        print(green_color + '|' + ' ' * ancho + '|' + reset_color)
    print(green_color + '+' + '-' * ancho + '+' + reset_color)

def mostrar_linea(ancho=70):
    print(green_color + "=" * ancho + reset_color)

def mostrar_titulo(titulo, ancho=70):
    mostrar_linea(ancho)
    print(blue_color + titulo.center(ancho) + reset_color)
    mostrar_linea(ancho)

def mostrar_cabecera(titulo, empresa="Corporacion el Rosado", ruc="1790097870001", ancho=90):
    borrarPantalla()
    mostrar_linea(ancho)
    print(blue_color + titulo.center(ancho) + reset_color)
    mostrar_linea(ancho)
    print(f"Empresa: {empresa}")
    print(f"RUC:     {ruc}")
    mostrar_linea(ancho)

def mostrar_exito(texto):
    print(green_color + texto + reset_color)

def mostrar_error(texto):
    print(red_color + texto + reset_color)

def mostrar_advertencia(texto):
    print(yellow_color + texto + reset_color)

def imprimir_fila(columnas, anchos):
    valores = []
    for texto, ancho in zip(columnas, anchos):
        valores.append(str(texto)[:ancho].ljust(ancho))
    print("  ".join(valores))

def imprimir_tabla(encabezados, filas, anchos):
    imprimir_fila(encabezados, anchos)
    print("-" * (sum(anchos) + (len(anchos) - 1) * 2))
    for fila in filas:
        imprimir_fila(fila, anchos)

def ancho_terminal(default=78):
    return shutil.get_terminal_size(fallback=(default, 30)).columns

def panel(titulo, subtitulo="", ancho=76):
    borrarPantalla()
    print(cyan_color + "+" + "-" * (ancho - 2) + "+" + reset_color)
    print(cyan_color + "|" + reset_color + titulo.center(ancho - 2) + cyan_color + "|" + reset_color)
    if subtitulo:
        print(cyan_color + "|" + reset_color + subtitulo.center(ancho - 2) + cyan_color + "|" + reset_color)
    print(cyan_color + "+" + "-" * (ancho - 2) + "+" + reset_color)
    print()

def seccion(titulo, ancho=76):
    print()
    print(blue_color + titulo.upper() + reset_color)
    print(green_color + "-" * min(ancho, max(20, len(titulo) + 8)) + reset_color)

def input_texto(etiqueta, requerido=True):
    while True:
        valor = input(yellow_color + f"{etiqueta}: " + reset_color).strip()
        if valor or not requerido:
            return valor
        mostrar_error("Este campo es obligatorio.")

def input_entero(etiqueta, minimo=1, requerido=True):
    while True:
        valor = input_texto(etiqueta, requerido=requerido)
        if not valor and not requerido:
            return None
        if valor.isdigit() and int(valor) >= minimo:
            return int(valor)
        mostrar_error(f"Ingrese un numero entero mayor o igual a {minimo}.")

def input_decimal(etiqueta, minimo=0.01, requerido=True):
    while True:
        valor = input_texto(etiqueta, requerido=requerido)
        if not valor and not requerido:
            return None
        try:
            numero = float(valor)
            if numero >= minimo:
                return numero
        except ValueError:
            pass
        mostrar_error(f"Ingrese un numero decimal mayor o igual a {minimo}.")

def confirmar(pregunta):
    respuesta = input(yellow_color + f"{pregunta} (s/n): " + reset_color).strip().lower()
    return respuesta == "s"

def tabla(encabezados, filas, anchos):
    if not filas:
        mostrar_advertencia("No hay registros para mostrar.")
        return
    imprimir_tabla(encabezados, filas, anchos)

def formatear_dinero(valor):
    return f"${float(valor):,.2f}"

def pausar(texto="Presione Enter para continuar..."):
    input(blue_color + texto + reset_color)
