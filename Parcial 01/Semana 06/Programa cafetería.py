# Clase base: Bebida
class Bebida:
    def __init__(self, nombre, tamaño):
        self.nombre = nombre              # Atributo público
        self.__tamaño = tamaño            # Atributo privado (encapsulación)

    def get_tamaño(self):
        """Método para acceder al tamaño (encapsulado)"""
        return self.__tamaño

    def set_tamaño(self, nuevo_tamaño):
        """Método para modificar el tamaño de forma segura"""
        if nuevo_tamaño in ["Pequeño", "Mediano", "Grande"]:
            self.__tamaño = nuevo_tamaño
        else:
            print("Tamaño no válido.")

    def servir(self):
        """Este método será sobrescrito por las clases hijas (polimorfismo)"""
        return f"Sirviendo {self.nombre} tamaño {self.__tamaño}"


# Clase derivada 1: Café (hereda de Bebida)
class Cafe(Bebida):
    def __init__(self, nombre, tamaño, tipo):
        super().__init__(nombre, tamaño)
        self.tipo = tipo  # Ejemplo: Expreso, Capuchino, Americano

    def servir(self):
        """Sobrescribe el método servir (polimorfismo)"""
        return f" Sirviendo un {self.tipo} {self.nombre} tamaño {self.get_tamaño()}"


# Clase derivada 2: Té (hereda de Bebida)
class Te(Bebida):
    def __init__(self, nombre, tamaño, sabor):
        super().__init__(nombre, tamaño)
        self.sabor = sabor  # Ejemplo: Manzanilla, Verde, Negro

    def servir(self):
        """Sobrescribe el método servir (polimorfismo)"""
        return f" Sirviendo un té sabor {self.sabor} tamaño {self.get_tamaño()}"


# Programa principal
if __name__ == "__main__":
    # Crear una bebida genérica
    bebida1 = Bebida("Chocolate Caliente", "Mediano")
    print(bebida1.servir())  # Usamos método de clase base

    print("\n---\n")

    # Crear un café
    cafe1 = Cafe("Latte", "Grande", "Capuchino")
    print(cafe1.servir())  # Polimorfismo: método sobrescrito

    # Encapsulación: cambiar tamaño de forma segura
    cafe1.set_tamaño("Pequeño")
    print(cafe1.servir())

    print("\n---\n")

    # Crear un té
    te1 = Te("Té Verde", "Mediano", "Hierbabuena")
    print(te1.servir())  # Otro ejemplo de polimorfismo
