from utilities import gotoxy, borrarPantalla, mensaje
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
import time
import sys
import shutil


class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        gotoxy(self.col,self.fil);print(self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 
        return opc   

class Valida:
    def solo_numeros(self,mensajeError,col,fil):
        while True: 
            gotoxy(col,fil)            
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor
    

    def solo_letras(self,mensaje,mensajeError): 
        while True:
            valor = str(input("          ------>   | {} ".format(mensaje)))
            if valor.isalpha():
                break
            else:
                print("          ------><  | {} ".format(mensajeError))
        return valor
    

    def solo_decimales(self,mensaje,mensajeError):
        while True:
            valor = str(input("          ------>   | {} ".format(mensaje)))
            try:
                valor = float(valor)
                if valor > float(0):
                    break
            except:
                print("          ------><  | {} ".format(mensajeError))
        return valor
    
    def validar_letras(frase,col1, fil1, col2, fil2,):
        while True:
            gotoxy(col1, fil1)
            print(blue_color + f"{frase}")
            gotoxy(col2, fil2)
            nombre = input(purple_color)
            if nombre.isalpha():
                return nombre.capitalize()
            else:
                gotoxy(col2, fil2)
                print(purple_color + "El campo solo puede contener letras.")
                time.sleep(1)
                gotoxy(col2, fil2)
                print(" "*40)
            
    def validar_numeros(frase, col1, fil1, col2, fil2):
        while True:
            gotoxy(col1, fil1)
            print(blue_color + f"{frase}")
            gotoxy(col2, fil2)
            numero = input(purple_color)
            if numero.isdigit():
                return numero
            else:
                gotoxy(col2, fil2)
                print(purple_color + "El campo solo puede contener números.")
                time.sleep(1)
                gotoxy(col2, fil2)
                print(" " * 40)


    def validar_dni(mensaje, col1, fil1, col2, fil2):
        while True:
            gotoxy(col1, fil1)
            print(blue_color + f"{mensaje}")
            gotoxy(col2, fil2)
            cedula = input(purple_color)
            
            if len(cedula) == 10 and cedula.isdigit():
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
                
                
                if total == int(cedula[9]):
                    return cedula
            
            gotoxy(col2, fil2)
            print(purple_color + "El formato del DNI es incorrecto.")
            time.sleep(1)
            gotoxy(col2, fil2)
            print(" "*60)


    def validar_numeros_decimales(frase, col1, fil1, col2, fil2):
        while True:
            gotoxy(col1, fil1)
            print(blue_color + f"{frase}")
            gotoxy(col2, fil2)
            numero = input(purple_color)
            try:
                numero = float(numero)
                return numero
            except ValueError:
                gotoxy(col2, fil2)
                print(purple_color + "El campo debe ser un número decimal.")
                time.sleep(1)
                gotoxy(col2, fil2)
                print(" " * 40)
            
            
        #jordy
        
                

    
class otra:
    pass    

if __name__ == '__main__':
    # instanciar el menu
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    # llamada al menu
    opcion_elegida = menu.menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if(opciones_menu==1):
      numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
      print("Número validado:", numero_validado)
    
    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)
    
    letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
    print("Letra validada:", letra_validada)
    
    decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
    print("Decimal validado:", decimal_validado)