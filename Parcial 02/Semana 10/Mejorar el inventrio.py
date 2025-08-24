import os
import json

# ================================
# Clase Producto
# ================================
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # Getters
    def get_id(self): return self.__id_producto
    def get_nombre(self): return self.__nombre
    def get_cantidad(self): return self.__cantidad
    def get_precio(self): return self.__precio

    # Setters
    def set_nombre(self, nuevo_nombre): self.__nombre = nuevo_nombre
    def set_cantidad(self, nueva_cantidad): self.__cantidad = nueva_cantidad
    def set_precio(self, nuevo_precio): self.__precio = nuevo_precio

    def __str__(self):
        return f"ID: {self.__id_producto} | Nombre: {self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"

    # ---- Métodos para JSON ----
    def to_dict(self):
        """Convierte producto a diccionario"""
        return {
            "id": self.__id_producto,
            "nombre": self.__nombre,
            "cantidad": self.__cantidad,
            "precio": self.__precio
        }

    @staticmethod
    def from_dict(data):
        """Reconstruye un producto desde un diccionario"""
        return Producto(data["id"], data["nombre"], data["cantidad"], data["precio"])


# ================================
# Clase Inventario
# ================================
class Inventario:
    def __init__(self, archivo="inventario.json"):
        self.productos = {}   # dict con clave = ID
        self.archivo = archivo
        self.cargar_desde_json()

    # ---- Persistencia con JSON ----
    def cargar_desde_json(self):
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w") as f:
                json.dump({}, f, indent=4)  # archivo vacío
            return

        try:
            with open(self.archivo, "r") as f:
                data = json.load(f)
                self.productos = {id_: Producto.from_dict(prod) for id_, prod in data.items()}
        except json.JSONDecodeError:
            print(" Archivo JSON corrupto. Se reiniciará vacío.")
            self.productos = {}
        except Exception as e:
            print(f" Error al cargar: {e}")

    def guardar_en_json(self):
        try:
            with open(self.archivo, "w") as f:
                data = {id_: p.to_dict() for id_, p in self.productos.items()}
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error al guardar: {e}")

    # ---- Operaciones de inventario ----
    def agregar_producto(self, producto):
        if producto.get_id() in self.productos:
            print("Error: El ID ya existe.")
            return
        self.productos[producto.get_id()] = producto
        self.guardar_en_json()
        print(" Producto agregado y guardado en JSON.")

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_en_json()
            print(" Producto eliminado y archivo actualizado.")
        else:
            print(" Producto no encontrado.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        if id_producto in self.productos:
            p = self.productos[id_producto]
            if nueva_cantidad is not None:
                p.set_cantidad(nueva_cantidad)
            if nuevo_precio is not None:
                p.set_precio(nuevo_precio)
            self.guardar_en_json()
            print(" Producto actualizado y archivo modificado.")
        else:
            print(" Producto no encontrado.")

    def buscar_producto_por_nombre(self, nombre):
        return [p for p in self.productos.values() if nombre.lower() in p.get_nombre().lower()]

    def mostrar_productos(self):
        if not self.productos:
            print("Inventario vacío.")
            return
        for p in self.productos.values():
            print(p)


# ================================
# Menú en consola
# ================================
def menu():
    inventario = Inventario()

    while True:
        print("\n=== GESTIÓN DE INVENTARIOS (JSON) ===")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar productos")
        print("6. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            id_prod = input("ID: ")
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            nuevo_producto = Producto(id_prod, nombre, cantidad, precio)
            inventario.agregar_producto(nuevo_producto)

        elif opcion == "2":
            id_prod = input("ID a eliminar: ")
            inventario.eliminar_producto(id_prod)

        elif opcion == "3":
            id_prod = input("ID a actualizar: ")
            cantidad = input("Nueva cantidad (vacío = igual): ")
            precio = input("Nuevo precio (vacío = igual): ")
            nueva_cantidad = int(cantidad) if cantidad else None
            nuevo_precio = float(precio) if precio else None
            inventario.actualizar_producto(id_prod, nueva_cantidad, nuevo_precio)

        elif opcion == "4":
            nombre_buscar = input("Nombre a buscar: ")
            resultados = inventario.buscar_producto_por_nombre(nombre_buscar)
            if resultados:
                for p in resultados:
                    print(p)
            else:
                print("Sin resultados.")

        elif opcion == "5":
            inventario.mostrar_productos()

        elif opcion == "6":
            print("Saliendo y guardando cambios.")
            break

        else:
            print(" Opción inválida.")


# ================================
# Programa principal
# ================================
if __name__ == "__main__":
    menu()

