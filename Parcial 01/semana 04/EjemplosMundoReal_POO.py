# Clase Plato
class Plato:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f}"


# Guarda todos los platos que pidió una mesa.
class Pedido:
    def __init__(self):
        self.platos = []

    def agregar_plato(self, plato):
        self.platos.append(plato)
        print(f" Agregado: {plato.nombre}")

    def mostrar_pedido(self):
        print(" Pedido actual:")
        total = 0
        for plato in self.platos:
            print(f"- {plato}")
            total += plato.precio
        print(f"Total: ${total:.2f}")

    def total_pagar(self):
        return sum(plato.precio for plato in self.platos)


# Mesas del restaurante.
class Mesa:
    def __init__(self, numero):
        self.numero = numero
        self.pedido = Pedido()
        self.ocupada = False

    def ocupar(self):
        self.ocupada = True
        print(f" Mesa {self.numero} está ahora ocupada.")

    def liberar(self):
        self.ocupada = False
        print(f" Mesa {self.numero} está ahora libre.")

    def mostrar_estado(self):
        estado = "Ocupada" if self.ocupada else "Libre"
        print(f"Mesa {self.numero}: {estado}")


# Administración de todas las mesas y el menú del restaurante.
class Restaurante:
    def __init__(self, nombre, num_mesas):
        self.nombre = nombre
        self.mesas = [Mesa(i+1) for i in range(num_mesas)]
        self.menu = []

    def agregar_plato_menu(self, plato):
        self.menu.append(plato)

    def mostrar_menu(self):
        print(f" Menú de {self.nombre}")
        for i, plato in enumerate(self.menu):
            print(f"{i+1}. {plato}")

    def mostrar_mesas(self):
        for mesa in self.mesas:
            mesa.mostrar_estado()

    def tomar_pedido(self, num_mesa, indices_platos):
        mesa = self.mesas[num_mesa - 1]
        if not mesa.ocupada:
            mesa.ocupar()
        for i in indices_platos:
            if 0 <= i < len(self.menu):
                mesa.pedido.agregar_plato(self.menu[i])

    def cerrar_cuenta(self, num_mesa):
        mesa = self.mesas[num_mesa - 1]
        print(f"\n Cuenta para Mesa {mesa.numero}:")
        mesa.pedido.mostrar_pedido()
        total = mesa.pedido.total_pagar()
        mesa.liberar()
        mesa.pedido = Pedido()  # Reset pedido
        return total


# USO DEL SISTEMA
if __name__ == "__main__":
    restaurante = Restaurante("El sabor unico", 5)

    # Agregar platos al menú
    restaurante.agregar_plato_menu(Plato("Arroz con pollo", 3.5))
    restaurante.agregar_plato_menu(Plato("Encebollado", 3.0))
    restaurante.agregar_plato_menu(Plato("Juguito de naranja", 1.0))

    # Mostrar menú y estado inicial
    restaurante.mostrar_menu()
    restaurante.mostrar_mesas()

    # Tomar pedido para mesa 2
    restaurante.tomar_pedido(2, [0, 2])  # Arroz con pollo y jugo

    # Mostrar pedido y cerrar cuenta
    restaurante.cerrar_cuenta(2)

    # Estado final de las mesas
    restaurante.mostrar_mesas()