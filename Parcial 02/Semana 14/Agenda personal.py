import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

# Intentamos importar DateEntry de tkcalendar; si no está, usaremos Entry simple
try:
    from tkcalendar import DateEntry
    HAS_TKCALENDAR = True
except Exception:
    HAS_TKCALENDAR = False

DATA_FILE = "events.json"


class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("700x450")

        # Lista interna de eventos (cada evento es dict con id, date, time, desc)
        self.events = []

        # Configuramos la interfaz en frames
        self._create_widgets()
        self._load_events()

    def _create_widgets(self):
        # Frame superior: Treeview (visualización de eventos)
        frame_view = ttk.Frame(self.root, padding=(10, 8))
        frame_view.pack(fill=tk.BOTH, expand=True)

        # Treeview con columnas: Fecha, Hora, Descripción
        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(frame_view, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.column("fecha", width=100, anchor="center")
        self.tree.column("hora", width=80, anchor="center")
        self.tree.column("descripcion", width=400, anchor="w")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical para Treeview
        vsb = ttk.Scrollbar(frame_view, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.LEFT, fill=tk.Y)

        # Frame inferior: entradas y botones
        frame_bottom = ttk.Frame(self.root, padding=(10, 8))
        frame_bottom.pack(fill=tk.X)

        # Subframe para campos de entrada
        frame_inputs = ttk.Frame(frame_bottom)
        frame_inputs.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Etiqueta y DatePicker/Entry para la fecha
        lbl_fecha = ttk.Label(frame_inputs, text="Fecha (YYYY-MM-DD):")
        lbl_fecha.grid(row=0, column=0, padx=5, pady=4, sticky="w")
        if HAS_TKCALENDAR:
            self.entry_fecha = DateEntry(frame_inputs, date_pattern="yyyy-MM-dd")
        else:
            # Fallback: Entry con hint
            self.entry_fecha = ttk.Entry(frame_inputs)
            self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_fecha.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        # Etiqueta y Entry para la hora
        lbl_hora = ttk.Label(frame_inputs, text="Hora (HH:MM, 24h):")
        lbl_hora.grid(row=0, column=1, padx=5, pady=4, sticky="w")
        self.entry_hora = ttk.Entry(frame_inputs, width=12)
        self.entry_hora.insert(0, "09:00")
        self.entry_hora.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Etiqueta y Entry para la descripción
        lbl_desc = ttk.Label(frame_inputs, text="Descripción:")
        lbl_desc.grid(row=0, column=2, padx=5, pady=4, sticky="w")
        self.entry_desc = ttk.Entry(frame_inputs, width=40)
        self.entry_desc.grid(row=1, column=2, padx=5, pady=2, sticky="w")

        # Subframe para botones
        frame_buttons = ttk.Frame(frame_bottom)
        frame_buttons.pack(side=tk.RIGHT, fill=tk.Y)

        btn_agregar = ttk.Button(frame_buttons, text="Agregar Evento", command=self.add_event)
        btn_agregar.pack(fill=tk.X, padx=5, pady=4)

        btn_eliminar = ttk.Button(frame_buttons, text="Eliminar Evento Seleccionado", command=self.delete_selected_event)
        btn_eliminar.pack(fill=tk.X, padx=5, pady=4)

        btn_salir = ttk.Button(frame_buttons, text="Salir", command=self.on_exit)
        btn_salir.pack(fill=tk.X, padx=5, pady=4)

        # Bind doble click en el tree para editar/ver (a modo de extensión)
        self.tree.bind("<Double-1>", self.on_double_click)

    # --- Manejo de eventos ---
    def add_event(self):
        """Agregar un evento desde los campos de entrada al Treeview y a la lista interna."""
        fecha_raw = self.entry_fecha.get().strip()
        hora_raw = self.entry_hora.get().strip()
        desc = self.entry_desc.get().strip()

        # Validaciones básicas
        if not fecha_raw or not hora_raw or not desc:
            messagebox.showwarning("Campos incompletos", "Por favor completa fecha, hora y descripción.")
            return

        # Validar fecha
        try:
            fecha_obj = datetime.strptime(fecha_raw, "%Y-%m-%d")
            fecha_text = fecha_obj.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Formato de fecha inválido", "La fecha debe tener el formato YYYY-MM-DD.")
            return

        # Validar hora
        try:
            hora_obj = datetime.strptime(hora_raw, "%H:%M")
            hora_text = hora_obj.strftime("%H:%M")
        except ValueError:
            messagebox.showerror("Formato de hora inválido", "La hora debe tener el formato HH:MM (24 horas).")
            return

        # Generar ID único simple (timestamp)
        event_id = str(int(datetime.now().timestamp() * 1000))

        event = {"id": event_id, "fecha": fecha_text, "hora": hora_text, "descripcion": desc}
        self.events.append(event)
        self._insert_tree_event(event)

        # Limpiar campos (opcional)
        if not HAS_TKCALENDAR:
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, "09:00")
        self.entry_desc.delete(0, tk.END)

        # Guardar en archivo
        self._save_events()

    def _insert_tree_event(self, event):
        """Insertar un evento (dict) en el Treeview. El iid será el id del evento."""
        self.tree.insert("", tk.END, iid=event["id"], values=(event["fecha"], event["hora"], event["descripcion"]))

    def delete_selected_event(self):
        """Eliminar el evento seleccionado con confirmación."""
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selecciona un evento", "Por favor selecciona un evento para eliminar.")
            return
        iid = sel[0]
        # Confirmación
        if messagebox.askyesno("Confirmar eliminación", "¿Seguro que deseas eliminar el evento seleccionado?"):
            # Eliminar de Treeview
            self.tree.delete(iid)
            # Eliminar de la lista interna
            self.events = [e for e in self.events if e["id"] != iid]
            # Guardar cambios
            self._save_events()

    def on_double_click(self, event):
        """Al hacer doble click podríamos mostrar detalle; aquí mostramos info en un messagebox."""
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        ev = next((e for e in self.events if e["id"] == iid), None)
        if ev:
            messagebox.showinfo("Detalle del evento", f"Fecha: {ev['fecha']}\nHora: {ev['hora']}\nDescripción: {ev['descripcion']}")

    def _save_events(self):
        """Guardar la lista de eventos en un archivo JSON."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.events, f, ensure_ascii=False, indent=2)
        except Exception as ex:
            messagebox.showerror("Error al guardar", f"No se pudo guardar en {DATA_FILE}:\n{ex}")

    def _load_events(self):
        """Cargar eventos desde el archivo JSON (si existe) y poblar el Treeview."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Validar que sea lista de dicts
                    if isinstance(data, list):
                        self.events = data
                        for e in self.events:
                            # Asegurarse que tengan id, fecha, hora, descripcion
                            if all(k in e for k in ("id", "fecha", "hora", "descripcion")):
                                self._insert_tree_event(e)
                    else:
                        self.events = []
            except Exception as ex:
                messagebox.showwarning("No se pudo cargar datos", f"Error leyendo {DATA_FILE}: {ex}")
                self.events = []
        else:
            # Archivo no existe => lista vacía
            self.events = []

    def on_exit(self):
        """Acción al salir: guardar y cerrar la ventana."""
        self._save_events()
        self.root.quit()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
