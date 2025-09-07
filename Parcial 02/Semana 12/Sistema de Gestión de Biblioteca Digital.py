import json
import os

# ================================
# Clase Libro
# ================================
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.info = (titulo, autor)   # tupla inmutable
        self.categoria = categoria
        self.isbn = isbn

    def to_dict(self):
        return {
            "titulo": self.info[0],
            "autor": self.info[1],
            "categoria": self.categoria,
            "isbn": self.isbn
        }

    @staticmethod
    def from_dict(data):
        return Libro(data["titulo"], data["autor"], data["categoria"], data["isbn"])

    def __str__(self):
        return f"{self.info[0]} de {self.info[1]} (Categoría: {self.categoria}, ISBN: {self.isbn})"


# ================================
# Clase Usuario
# ================================
class Usuario:
    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        self.libros_prestados = []

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "user_id": self.user_id,
            "libros_prestados": [libro.isbn for libro in self.libros_prestados]
        }

    @staticmethod
    def from_dict(data, libros_dict):
        u = Usuario(data["nombre"], data["user_id"])
        u.libros_prestados = [libros_dict[isbn] for isbn in data.get("libros_prestados", []) if isbn in libros_dict]
        return u

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.user_id})"


# ================================
# Clase Biblioteca
# ================================
class Biblioteca:
    def __init__(self):
        self.libros = {}     # isbn -> Libro
        self.usuarios = {}   # id -> Usuario

    # ---- Gestión de libros ----
    def anadir_libro(self, libro):
        if libro.isbn in self.libros:
            raise KeyError(f"Ya existe un libro con ISBN {libro.isbn}")
        self.libros[libro.isbn] = libro

    # ---- Gestión de usuarios ----
    def registrar_usuario(self, usuario):
        if usuario.user_id in self.usuarios:
            raise KeyError(f"Ya existe un usuario con ID {usuario.user_id}")
        self.usuarios[usuario.user_id] = usuario

    # ---- Préstamos ----
    def prestar_libro(self, isbn, user_id):
        if isbn not in self.libros:
            raise KeyError("Ese libro no existe")
        if user_id not in self.usuarios:
            raise KeyError("Ese usuario no existe")
        # Verificar si el libro ya está prestado
        for u in self.usuarios.values():
            if any(l.isbn == isbn for l in u.libros_prestados):
                raise ValueError("El libro ya está prestado")
        self.usuarios[user_id].libros_prestados.append(self.libros[isbn])

    def devolver_libro(self, isbn, user_id):
        if user_id not in self.usuarios:
            raise KeyError("Ese usuario no existe")
        usuario = self.usuarios[user_id]
        usuario.libros_prestados = [l for l in usuario.libros_prestados if l.isbn != isbn]

    # ---- Listar ----
    def listar_libros(self):
        return list(self.libros.values())

    def listar_usuarios(self):
        return list(self.usuarios.values())

    def listar_prestamos(self, user_id):
        if user_id not in self.usuarios:
            raise KeyError("Usuario no existe")
        return self.usuarios[user_id].libros_prestados


# ================================
# Funciones para archivos
# ================================
def guardar_json(bib):
    # Guardar libros
    with open("libros.json", "w", encoding="utf-8") as f:
        json.dump({isbn: l.to_dict() for isbn, l in bib.libros.items()}, f, indent=2, ensure_ascii=False)

    # Guardar usuarios
    with open("usuarios.json", "w", encoding="utf-8") as f:
        json.dump({uid: u.to_dict() for uid, u in bib.usuarios.items()}, f, indent=2, ensure_ascii=False)

    # Guardar préstamos
    with open("prestamos.json", "w", encoding="utf-8") as f:
        prestamos = {uid: [l.isbn for l in u.libros_prestados] for uid, u in bib.usuarios.items()}
        json.dump(prestamos, f, indent=2, ensure_ascii=False)


def cargar_json():
    bib = Biblioteca()

    # Cargar libros
    if os.path.exists("libros.json"):
        with open("libros.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            bib.libros = {isbn: Libro.from_dict(d) for isbn, d in data.items()}

    # Cargar usuarios
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            bib.usuarios = {uid: Usuario.from_dict(d, bib.libros) for uid, d in data.items()}

    # Cargar préstamos
    if os.path.exists("prestamos.json"):
        with open("prestamos.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for uid, lista in data.items():
                if uid in bib.usuarios:
                    bib.usuarios[uid].libros_prestados = [bib.libros[isbn] for isbn in lista if isbn in bib.libros]

    return bib


# ================================
# Menú de consola con guardado automático
# ================================
def menu():
    bib = cargar_json()
    print("Biblioteca cargada.")

    while True:
        print("\n===== MENÚ BIBLIOTECA =====")
        print("1) Añadir libro")
        print("2) Registrar usuario")
        print("3) Prestar libro")
        print("4) Devolver libro")
        print("5) Mostrar libros")
        print("6) Mostrar usuarios")
        print("7) Mostrar préstamos de un usuario")
        print("0) Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            try:
                titulo = input("Título: ")
                autor = input("Autor: ")
                categoria = input("Categoría: ")
                isbn = input("ISBN: ")
                bib.anadir_libro(Libro(titulo, autor, categoria, isbn))
                guardar_json(bib)
                print("Libro añadido y guardado.")
            except Exception as e:
                print("Error:", e)

        elif opcion == "2":
            try:
                nombre = input("Nombre usuario: ")
                uid = input("ID usuario: ")
                bib.registrar_usuario(Usuario(nombre, uid))
                guardar_json(bib)
                print("Usuario registrado y guardado.")
            except Exception as e:
                print("Error:", e)

        elif opcion == "3":
            try:
                isbn = input("ISBN del libro: ")
                uid = input("ID usuario: ")
                bib.prestar_libro(isbn, uid)
                guardar_json(bib)
                print("Libro prestado y guardado.")
            except Exception as e:
                print("Error:", e)

        elif opcion == "4":
            try:
                isbn = input("ISBN del libro: ")
                uid = input("ID usuario: ")
                bib.devolver_libro(isbn, uid)
                guardar_json(bib)
                print("Libro devuelto y guardado.")
            except Exception as e:
                print("Error:", e)

        elif opcion == "5":
            for l in bib.listar_libros():
                print(l)

        elif opcion == "6":
            for u in bib.listar_usuarios():
                print(u)

        elif opcion == "7":
            uid = input("ID usuario: ")
            try:
                for l in bib.listar_prestamos(uid):
                    print(l)
            except Exception as e:
                print("Error:", e)

        elif opcion == "0":
            print("Hasta pronto")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()