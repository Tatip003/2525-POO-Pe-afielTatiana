import tkinter as tk
from tkinter import messagebox



# Aplicación GUI con Tkinter


class AplicacionLista:
    def __init__(self, root):
        # Configuración de la ventana principal
        self.root = root
        self.root.title("Aplicación de Lista de Datos")
        self.root.geometry("400x300")

        # Etiqueta
        self.label = tk.Label(root, text="Ingrese un dato:")
        self.label.pack(pady=5)

        # Campo de texto
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        # Botón para agregar datos
        self.boton_agregar = tk.Button(root, text="Agregar", command=self.agregar_dato)
        self.boton_agregar.pack(pady=5)

        # Listbox para mostrar datos
        self.lista = tk.Listbox(root, width=40, height=10)
        self.lista.pack(pady=5)

        # Botón para limpiar datos
        self.boton_limpiar = tk.Button(root, text="Limpiar", command=self.limpiar_datos)
        self.boton_limpiar.pack(pady=5)

    # Función para agregar datos
    def agregar_dato(self):
        dato = self.entry.get().strip()  # Obtener el texto ingresado
        if dato:
            self.lista.insert(tk.END, dato)  # Agregar a la lista
            self.entry.delete(0, tk.END)  # Limpiar campo de texto
        else:
            messagebox.showwarning("Advertencia", "Debe ingresar un dato antes de agregarlo.")

    # Función para limpiar datos
    def limpiar_datos(self):
        seleccion = self.lista.curselection()  # Obtener selección
        if seleccion:
            for index in reversed(seleccion):  # Eliminar seleccionados
                self.lista.delete(index)
        else:
            # Confirmar si quiere borrar todo
            if messagebox.askyesno("Confirmar", "¿Desea borrar toda la lista?"):
                self.lista.delete(0, tk.END)



# Ejecutar aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionLista(root)
    root.mainloop()
