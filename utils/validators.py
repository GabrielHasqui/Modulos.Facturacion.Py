import time

from utils.formatters import blue_color, gotoxy, purple_color


class Valida:
    @staticmethod
    def solo_numeros(mensaje_error, col, fil):
        while True:
            gotoxy(col, fil)
            valor = input().strip()
            if valor.isdigit() and int(valor) > 0:
                return valor

            gotoxy(col, fil)
            print(mensaje_error)
            time.sleep(1)
            gotoxy(col, fil)
            print(" " * 40)

    @staticmethod
    def solo_letras(mensaje, mensaje_error):
        while True:
            valor = input(f"          ------>   | {mensaje} ").strip()
            if valor.replace(" ", "").isalpha() and valor:
                return valor.title()

            print(f"          ------><  | {mensaje_error} ")

    @staticmethod
    def solo_decimales(mensaje, mensaje_error):
        while True:
            valor = input(f"          ------>   | {mensaje} ").strip()
            try:
                numero = float(valor)
                if numero > 0:
                    return numero
            except ValueError:
                pass

            print(f"          ------><  | {mensaje_error} ")

    @staticmethod
    def validar_letras(frase, col1, fil1, col2, fil2):
        while True:
            gotoxy(col1, fil1)
            print(blue_color + frase)
            gotoxy(col2, fil2)
            nombre = input(purple_color).strip()
            if nombre.replace(" ", "").isalpha() and nombre:
                return nombre.title()

            gotoxy(col2, fil2)
            print(purple_color + "El campo solo puede contener letras.")
            time.sleep(1)
            gotoxy(col2, fil2)
            print(" " * 50)

    @staticmethod
    def validar_numeros(frase, col1, fil1, col2, fil2):
        while True:
            gotoxy(col1, fil1)
            print(blue_color + frase)
            gotoxy(col2, fil2)
            numero = input(purple_color).strip()
            if numero.isdigit() and int(numero) > 0:
                return numero

            gotoxy(col2, fil2)
            print(purple_color + "El campo solo puede contener numeros positivos.")
            time.sleep(1)
            gotoxy(col2, fil2)
            print(" " * 60)

    @staticmethod
    def validar_dni(mensaje, col1, fil1, col2, fil2):
        while True:
            gotoxy(col1, fil1)
            print(blue_color + mensaje)
            gotoxy(col2, fil2)
            cedula = input(purple_color).strip()

            if Valida.es_cedula_valida(cedula):
                return cedula

            gotoxy(col2, fil2)
            print(purple_color + "El formato del DNI es incorrecto.")
            time.sleep(1)
            gotoxy(col2, fil2)
            print(" " * 60)

    @staticmethod
    def validar_numeros_decimales(frase, col1, fil1, col2, fil2):
        while True:
            gotoxy(col1, fil1)
            print(blue_color + frase)
            gotoxy(col2, fil2)
            numero = input(purple_color).strip()
            try:
                numero = float(numero)
                if numero > 0:
                    return numero
            except ValueError:
                pass

            gotoxy(col2, fil2)
            print(purple_color + "El campo debe ser un numero decimal positivo.")
            time.sleep(1)
            gotoxy(col2, fil2)
            print(" " * 60)

    @staticmethod
    def es_cedula_valida(cedula):
        if len(cedula) != 10 or not cedula.isdigit():
            return False

        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        suma = 0
        for i in range(9):
            digito = int(cedula[i]) * coeficientes[i]
            if digito > 9:
                digito -= 9
            suma += digito

        total = suma % 10
        if total != 0:
            total = 10 - total

        return total == int(cedula[9])
