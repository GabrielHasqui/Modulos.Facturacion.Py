from utils.formatters import blue_color, cyan_color, green_color, reset_color, yellow_color


class Menu:
    def __init__(self, titulo="", opciones=None, col=6, fil=1):
        self.titulo = titulo
        self.opciones = opciones or []

    def menu(self):
        ancho = 64
        print(cyan_color + "+" + "-" * (ancho - 2) + "+" + reset_color)
        print(cyan_color + "|" + reset_color + self.titulo.center(ancho - 2) + cyan_color + "|" + reset_color)
        print(cyan_color + "+" + "-" * (ancho - 2) + "+" + reset_color)
        for opcion in self.opciones:
            print("  " + blue_color + opcion + reset_color)
        print(green_color + "-" * ancho + reset_color)
        return input(yellow_color + f"Seleccione una opcion [1-{len(self.opciones)}]: " + reset_color).strip()
