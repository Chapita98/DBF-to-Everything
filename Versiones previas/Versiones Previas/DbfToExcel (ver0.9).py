import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from funciones_conversion import convertir_basico, convertir_avanzado, convertir_total

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor DBF a Excel")
        self.root.geometry("1000x600")

        self.archivos = []
        self.opciones_formato = {
            "centrar_texto": tk.BooleanVar(),
            "inmovilizar_fila": tk.BooleanVar(),
            "colores_alternados": tk.BooleanVar(),
            "autoajustar_columnas": tk.BooleanVar(),
            "negrita_encabezado": tk.BooleanVar(),
            "tamano_encabezado": tk.IntVar(value=12),
            "tamano_datos": tk.IntVar(value=10),
        }

        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = tk.Frame(self.root)
        contenedor.pack(fill=tk.BOTH, expand=True)

        frame_izquierda = tk.Frame(contenedor)
        frame_izquierda.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        frame_derecha = tk.Frame(contenedor)
        frame_derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Opciones de formato
        tk.Label(frame_izquierda, text="Opciones de Formato", font=("Arial", 10, "bold")).pack(anchor="w")
        for texto, var in [
            ("Centrar texto", self.opciones_formato["centrar_texto"]),
            ("Inmovilizar fila de encabezado", self.opciones_formato["inmovilizar_fila"]),
            ("Colores alternados", self.opciones_formato["colores_alternados"]),
            ("Autoajustar columnas", self.opciones_formato["autoajustar_columnas"]),
            ("Negrita en encabezado", self.opciones_formato["negrita_encabezado"]),
        ]:
            tk.Checkbutton(frame_izquierda, text=texto, variable=var).pack(anchor="w")

        tk.Label(frame_izquierda, text="Tamaño encabezado").pack(anchor="w")
        tk.Entry(frame_izquierda, textvariable=self.opciones_formato["tamano_encabezado"], width=5).pack(anchor="w")

        tk.Label(frame_izquierda, text="Tamaño datos").pack(anchor="w")
        tk.Entry(frame_izquierda, textvariable=self.opciones_formato["tamano_datos"], width=5).pack(anchor="w")

        # Botones principales
        tk.Button(frame_izquierda, text="Agregar Archivos", command=self.agregar_archivos).pack(fill=tk.X, pady=2)
        tk.Button(frame_izquierda, text="Limpiar Lista", command=self.limpiar_lista).pack(fill=tk.X, pady=2)
        tk.Button(frame_izquierda, text="Seleccionar Todos (Básico)", command=self.seleccionar_todos_basico).pack(fill=tk.X, pady=2)
        tk.Button(frame_izquierda, text="Seleccionar Todos (Avanzado)", command=self.seleccionar_todos_avanzado).pack(fill=tk.X, pady=2)
        tk.Button(frame_izquierda, text="Convertir Básico", command=self.convertir_basico).pack(fill=tk.X, pady=2)
        tk.Button(frame_izquierda, text="Convertir Avanzado", command=self.convertir_avanzado).pack(fill=tk.X, pady=2)
        tk.Button(frame_izquierda, text="Convertir TODO", command=self.convertir_total).pack(fill=tk.X, pady=2)

        # Tabla de archivos
        self.tabla = ttk.Treeview(frame_derecha, columns=("archivo",), show="headings")
        self.tabla.heading("archivo", text="Archivo DBF")
        self.tabla.pack(fill=tk.BOTH, expand=True)

    def agregar_archivos(self):
        nuevos_archivos = filedialog.askopenfilenames(filetypes=[("Archivos DBF", "*.dbf")])
        for archivo in nuevos_archivos:
            if archivo not in self.archivos:
                self.archivos.append(archivo)
                self.tabla.insert("", "end", values=(archivo,))

    def limpiar_lista(self):
        self.archivos.clear()
        for item in self.tabla.get_children():
            self.tabla.delete(item)

    def seleccionar_todos_basico(self):
        self.convertir_basico()

    def seleccionar_todos_avanzado(self):
        self.convertir_avanzado()

    def convertir_basico(self):
        if not self.archivos:
            messagebox.showwarning("Atención", "No hay archivos seleccionados.")
            return
        for archivo in self.archivos:
            convertir_basico(archivo)
        messagebox.showinfo("Éxito", "Archivos convertidos en modo básico.")

    def convertir_avanzado(self):
        if not self.archivos:
            messagebox.showwarning("Atención", "No hay archivos seleccionados.")
            return
        for archivo in self.archivos:
            convertir_avanzado(archivo, self.opciones_formato)
        messagebox.showinfo("Éxito", "Archivos convertidos en modo avanzado.")

    def convertir_total(self):
        if not self.archivos:
            messagebox.showwarning("Atención", "No hay archivos seleccionados.")
            return
        convertir_total(self.archivos, self.opciones_formato)
        messagebox.showinfo("Éxito", "Todos los archivos convertidos con formato.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
