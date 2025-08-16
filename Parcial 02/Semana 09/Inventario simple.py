
# Clase Producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        # Inicializa un producto con ID, nombre, cantidad y precio
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
        # Formato de impresión del producto
        return f"ID: {self.__id_producto} | Nombre: {self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"


# Clase Inventario
class Inventario:
    def __init__(self):
        # Lista de productos
        self.productos = []

    def agregar_producto(self, producto):
        # Agrega un producto si el ID es único
        for p in self.productos:
            if p.get_id() == producto.get_id():
                print("Error: El ID ya existe.")
                return
        self.productos.append(producto)
        print("Producto agregado.")

    def eliminar_producto(self, id_producto):
        # Elimina un producto por ID
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                print("Producto eliminado.")
                return
        print("Producto no encontrado.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        # Actualiza cantidad y/o precio
        for p in self.productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                print("Producto actualizado.")
                return
        print("Producto no encontrado.")

    def buscar_producto_por_nombre(self, nombre):
        # Busca productos por coincidencia en el nombre
        return [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]

    def mostrar_productos(self):
        # Muestra todos los productos
        if not self.productos:
            print("Inventario vacío.")
            return
        for p in self.productos:
            print(p)



# Menú en consola

def menu():
    inventario = Inventario()

    while True:
        print("\n=== GESTIÓN DE INVENTARIOS ===")
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
            print("Saliendo...")
            break

        else:
            print("Opción inválida.")


# Ejecutar
if __name__ == "__main__":
    menu()
