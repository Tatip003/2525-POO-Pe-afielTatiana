import json
import os

# ================================
# Clase Producto
# ================================
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        # Atributos directos (sin property)
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        """Convierte el producto en un diccionario (para guardar en JSON)."""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data):
        """Crea un producto a partir de un diccionario (al cargar JSON)."""
        return Producto(
            data["id"],
            data["nombre"],
            data["cantidad"],
            data["precio"]
        )

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: {self.precio:.2f}"


# ================================
# Clase Inventario
# ================================
class Inventario:
    def __init__(self):
        self.productos = {}  # Diccionario: ID -> Producto

    def agregar(self, producto):
        if producto.id in self.productos:
            raise KeyError(f"Ya existe un producto con ID {producto.id}")
        self.productos[producto.id] = producto

    def eliminar(self, id_producto):
        if id_producto not in self.productos:
            raise KeyError(f"No existe el producto con ID {id_producto}")
        return self.productos.pop(id_producto)

    def actualizar(self, id_producto, nombre=None, cantidad=None, precio=None):
        if id_producto not in self.productos:
            raise KeyError(f"No existe el producto con ID {id_producto}")
        p = self.productos[id_producto]
        if nombre is not None:
            p.nombre = nombre
        if cantidad is not None:
            p.cantidad = cantidad
        if precio is not None:
            p.precio = precio
        return p

    def buscar_por_nombre(self, consulta):
        consulta = consulta.lower()
        return [p for p in self.productos.values() if consulta in p.nombre.lower()]

    def listar_todos(self):
        return list(self.productos.values())

    def to_dict(self):
        return {"productos": [p.to_dict() for p in self.productos.values()]}

    @staticmethod
    def from_dict(data):
        inv = Inventario()
        for d in data.get("productos", []):
            p = Producto.from_dict(d)
            inv.agregar(p)
        return inv


# ================================
# Funciones para archivos
# ================================
RUTA_JSON = "inventario.json"

def guardar_json(inventario, ruta=RUTA_JSON):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(inventario.to_dict(), f, ensure_ascii=False, indent=2)

def cargar_json(ruta=RUTA_JSON):
    if not os.path.exists(ruta):
        return Inventario()
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Inventario.from_dict(data)


# ================================
# Menú de consola
# ================================
def menu():
    inv = cargar_json()
    print("📦 Inventario cargado.")

    while True:
        print("\n===== MENÚ INVENTARIO =====")
        print("1) Añadir producto")
        print("2) Eliminar producto")
        print("3) Actualizar producto")
        print("4) Buscar por nombre")
        print("5) Mostrar todos")
        print("6) Guardar inventario")
        print("0) Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            try:
                id_p = int(input("ID: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                inv.agregar(Producto(id_p, nombre, cantidad, precio))
                print("✓ Producto añadido.")
            except Exception as e:
                print("✗ Error:", e)

        elif opcion == "2":
            try:
                id_p = int(input("ID a eliminar: "))
                eliminado = inv.eliminar(id_p)
                print("✓ Eliminado:", eliminado)
            except Exception as e:
                print("✗ Error:", e)

        elif opcion == "3":
            try:
                id_p = int(input("ID a actualizar: "))
                nombre = input("Nuevo nombre (enter para no cambiar): ")
                cantidad = input("Nueva cantidad (enter para no cambiar): ")
                precio = input("Nuevo precio (enter para no cambiar): ")

                kwargs = {}
                if nombre: kwargs["nombre"] = nombre
                if cantidad: kwargs["cantidad"] = int(cantidad)
                if precio: kwargs["precio"] = float(precio)

                actualizado = inv.actualizar(id_p, **kwargs)
                print("✓ Actualizado:", actualizado)
            except Exception as e:
                print("✗ Error:", e)

        elif opcion == "4":
            consulta = input("Buscar por nombre: ")
            resultados = inv.buscar_por_nombre(consulta)
            if resultados:
                for p in resultados:
                    print(p)
            else:
                print("– No se encontraron productos –")

        elif opcion == "5":
            for p in inv.listar_todos():
                print(p)

        elif opcion == "6":
            guardar_json(inv)
            print("✓ Inventario guardado.")

        elif opcion == "0":
            print("👋 Hasta pronto")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
